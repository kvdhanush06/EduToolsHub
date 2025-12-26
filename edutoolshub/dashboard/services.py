"""Helper services for external APIs and conversion utilities used by views.

This module centralizes network calls and conversion logic to improve
testability and readability of the view layer.
"""

import functools
import logging
from typing import Any, Dict, List, Optional

import requests
import wikipedia
from requests.adapters import HTTPAdapter
from requests.sessions import Session
from urllib3.util.retry import Retry

# Some versions of `httpx` (used by `youtubesearchpython`) do not accept a
# `proxies` keyword on the top-level `httpx.post` convenience function. The
# third-party package calls `httpx.post(..., proxies=...)` which raises
# TypeError if the installed httpx version doesn't accept that kwarg. To
# remain compatible across httpx versions we monkeypatch `httpx.post` early
# so that a `proxies` kw is accepted and forwarded to a short-lived
# `httpx.Client` when provided.
try:
    import httpx

    _httpx_post_original = getattr(httpx, "post")

    def _httpx_post_compat(*args, **kwargs):
        # Pop proxies if present; if provided, use a Client that accepts
        # proxies. Otherwise call the original convenience function.
        proxies = kwargs.pop("proxies", None)
        if proxies:
            # httpx.Client accepts `proxies` and will honor the mapping.
            with httpx.Client(proxies=proxies) as _client:
                return _client.post(*args, **kwargs)
        return _httpx_post_original(*args, **kwargs)

    # Replace the top-level post function with our compatibility wrapper.
    httpx.post = _httpx_post_compat
except Exception:
    # If httpx isn't installed or monkeypatching fails for any reason, don't
    # prevent the module from loading; the downstream import may still fail
    # at runtime, but we preserve behavior for test environments.
    pass

# Import VideosSearch after the httpx monkeypatch so the patched function
# will be used by the third-party package during synchronous requests.
from youtubesearchpython import VideosSearch

logger = logging.getLogger(__name__)


# Network defaults
DEFAULT_TIMEOUT = 5

# Use a session with a retry strategy for external HTTP calls to improve
# resilience and performance (connection pooling).
_session: Session = requests.Session()
retry_strategy = Retry(
    total=2, backoff_factor=0.3, status_forcelist=[429, 500, 502, 503, 504]
)
adapter = HTTPAdapter(max_retries=retry_strategy)
_session.mount("https://", adapter)
_session.mount("http://", adapter)


@functools.lru_cache(maxsize=256)
def search_youtube(query: str, limit: int = 10) -> List[Dict[str, Any]]:
    """Return a simplified list of YouTube search results.

    The function normalizes the query, defends against invalid input and logs
    failures. It returns an empty list on error so callers can handle 'no
    results' uniformly.
    """
    if not isinstance(query, str):
        logger.debug("search_youtube called with non-str query: %r", query)
        return []

    q = query.strip()
    if not q:
        return []

    try:
        video_search = VideosSearch(q, limit=limit)
        results: List[Dict[str, Any]] = []
        raw_results = video_search.result().get("result", [])
        for item in raw_results:
            # Defensive extraction with sensible defaults
            title = item.get("title")
            duration = item.get("duration")
            thumbnails = item.get("thumbnails") or []
            thumbnail = thumbnails[0].get("url") if thumbnails else None
            channel = (item.get("channel") or {}).get("name")
            link = item.get("link")
            views = (item.get("viewCount") or {}).get("short")
            published = item.get("publishedTime")
            desc = "".join(
                s.get("text", "") for s in (item.get("descriptionSnippet") or [])
            )

            results.append(
                {
                    "input": q,
                    "title": title,
                    "duration": duration,
                    "thumbnail": thumbnail,
                    "channel": channel,
                    "link": link,
                    "views": views,
                    "published": published,
                    "description": desc,
                }
            )

        return results
    except Exception as exc:  # library may raise various runtime errors
        logger.exception("YouTube search failed for %s: %s", q, exc)
        return []


@functools.lru_cache(maxsize=256)
def search_books(
    query: str, limit: int = 10, timeout: int = DEFAULT_TIMEOUT
) -> List[Dict[str, Any]]:
    """Query Google Books and return simplified results.

    Uses a shared HTTP session and defensive checks to avoid raising for
    transient network failures.
    """
    if not isinstance(query, str):
        return []

    q = query.strip()
    if not q:
        return []

    url = f"https://www.googleapis.com/books/v1/volumes?q={q}"
    try:
        # Use requests.get so tests that patch `requests.get` are honored
        r = requests.get(url, timeout=timeout)
        r.raise_for_status()
        payload = r.json()
        items = payload.get("items", [])
        results: List[Dict[str, Any]] = []
        for item in items[:limit]:
            info = item.get("volumeInfo", {})
            results.append(
                {
                    "title": info.get("title"),
                    "subtitle": info.get("subtitle"),
                    "description": info.get("description"),
                    "count": info.get("pageCount"),
                    "categories": info.get("categories"),
                    "rating": info.get("averageRating"),
                    "thumbnail": (info.get("imageLinks") or {}).get("thumbnail"),
                    "preview": info.get("previewLink"),
                }
            )
        return results
    except (requests.RequestException, ValueError) as exc:
        logger.exception("Books lookup failed for %s: %s", q, exc)
        return []


@functools.lru_cache(maxsize=512)
def lookup_dictionary(word: str, timeout: int = DEFAULT_TIMEOUT) -> Dict[str, Any]:
    """Return dictionary details for `word` or an empty dict on failure."""
    if not isinstance(word, str):
        return {}

    w = word.strip()
    if not w:
        return {}

    url = f"https://api.dictionaryapi.dev/api/v2/entries/en_US/{w}"
    try:
        # Use requests.get so tests that patch `requests.get` are honored
        r = requests.get(url, timeout=timeout)
        r.raise_for_status()
        data = r.json()
        if not data:
            return {}
        first = data[0]
        phonetics = (first.get("phonetics") or [{}])[0].get("text")
        audio = (first.get("phonetics") or [{}])[0].get("audio")
        meaning = (first.get("meanings") or [{}])[0]
        definition = (meaning.get("definitions") or [{}])[0].get("definition")
        example = (meaning.get("definitions") or [{}])[0].get("example")
        synonyms = (meaning.get("definitions") or [{}])[0].get("synonyms")
        return {
            "phonetics": phonetics,
            "audio": audio,
            "definition": definition,
            "example": example,
            "synonyms": synonyms,
        }
    except (requests.RequestException, ValueError) as exc:
        logger.exception("Dictionary lookup failed for %s: %s", w, exc)
        return {}


@functools.lru_cache(maxsize=512)
def lookup_wikipedia(term: str) -> Dict[str, Optional[str]]:
    """Return basic wikipedia info (title, url, summary) or Nones on failure."""
    if not isinstance(term, str):
        return {"title": None, "link": None, "details": None}

    t = term.strip()
    if not t:
        return {"title": None, "link": None, "details": None}

    try:
        # Prefer getting the page object (tests patch wikipedia.page)
        page = wikipedia.page(t)
        return {"title": page.title, "link": page.url, "details": page.summary}
    except (
        wikipedia.exceptions.DisambiguationError,
        wikipedia.exceptions.PageError,
    ) as exc:
        logger.info("Wikipedia lookup yielded no exact page for %s: %s", t, exc)
        return {"title": None, "link": None, "details": None}
    except Exception as exc:
        logger.exception("Wikipedia lookup failed for %s: %s", t, exc)
        return {"title": None, "link": None, "details": None}


@functools.lru_cache(maxsize=1024)
def convert_length(value: int, frm: str, to: str) -> Optional[str]:
    """Convert length between yard and foot.

    Returns a human-readable string or None if conversion is unsupported.
    Inputs are validated and non-integer values are rejected.
    """
    try:
        iv = int(value)
    except (TypeError, ValueError):
        logger.debug("convert_length received non-int value: %r", value)
        return None

    if frm == "yard" and to == "foot":
        return f"{iv} yard = {iv * 3} foot"
    if frm == "foot" and to == "yard":
        return f"{iv} foot = {iv / 3} yard"
    return None


@functools.lru_cache(maxsize=1024)
def convert_mass(value: int, frm: str, to: str) -> Optional[str]:
    """Convert mass between pound and kilogram. Returns string or None."""
    try:
        iv = int(value)
    except (TypeError, ValueError):
        logger.debug("convert_mass received non-int value: %r", value)
        return None

    if frm == "pound" and to == "kilogram":
        return f"{iv} pound = {iv * 0.453592} kilogram"
    if frm == "kilogram" and to == "pound":
        return f"{iv} kilogram = {iv * 2.20462} pound"
    return None
