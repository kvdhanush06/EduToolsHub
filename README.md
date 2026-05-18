# EduToolsHub

EduToolsHub is a polished, student-focused web toolkit built with Django that brings essential study utilities into one lightweight application. Designed for learners who want to stay organized and discover resources quickly, EduToolsHub combines simple productivity tools (notes, todo, homework) with curated content lookup features (Wikipedia, dictionary, YouTube, books, converters) to support everyday study workflows.

## Why EduToolsHub?

- Centralize learning: keep homework, todos, and notes in one personal space.
- Discover resources: quickly search for articles, videos, dictionary definitions, and books related to your studies.
- Lightweight & local-first: built for easy local development and small deployments, ideal for students and hobby projects.

## Key Features

- Notes — create, view, and manage personal study notes. Notes consist of a title and a rich description; each note belongs to a user and can be opened in a detail view or deleted from the list.

- Homework — add homework items with subject, title, description and a due date/time. Homeworks include an "is_finished" flag you can toggle from the list or the profile; the UI displays the due date so you can keep track of deadlines.

- Todo — quick task entries with a title and a completion flag. Todos are user-scoped and can be marked complete or deleted from the UI.

- Wikipedia search — search for an article and open the matching page; results include the article title, a direct link to Wikipedia, and a short summary.

- Dictionary — lookup powered by a public dictionary API. For a queried word the app shows phonetics, an audio pronunciation (playable in-browser), a primary definition, an example usage and a list of synonyms (when available).

- YouTube search — client-side search backed by the youtube-search-python package. Results include title, channel, thumbnail, duration, views and a link to open the video on YouTube.

- Books lookup — searches Google Books (via the public API) and returns title, subtitle, description, page count, categories, rating, thumbnail and a preview link so you can preview or purchase the book.

- Unit conversion — small conversion utility supporting length (yard ↔ foot) and mass (pound ↔ kilogram). Inputs are validated as integers; the conversion returns a human-readable string.

- Profile dashboard — a focused view showing only your pending (not finished) todos and homeworks so you can quickly see what’s due.

Extra notes about UX and behavior
- Authentication: users register with a standard username/password (Django's User model). Registered users can access the dashboard features; unauthenticated visitors are prompted to register or login.
- Forms & UI: the app uses Django forms with Bootstrap 5 and django-crispy-forms for consistent, responsive layouts and a clean, mobile-friendly interface.
- Data model: the main user-scoped models are `Notes(title, description)`, `HomeWork(subject, title, description, due, is_finished)` and `Todo(title, is_finished)`.
- External APIs & resiliency: external queries (YouTube, Google Books, dictionary API, Wikipedia) are performed from a dedicated services module. The code uses request retries and local caching (lru_cache) for common lookups to improve reliability and reduce redundant network calls.
- Limitations & privacy: the site makes outbound requests to third-party APIs (Google Books, dictionaryapi.dev, Wikipedia, YouTube search client). No usage tracking is performed by the app itself, but external services may log requests. The demo includes an audio player for dictionary pronunciations.

## Demo & Live Access

- Demo video: https://youtu.be/Fe0io0Mu53A
- Live site: https://edutoolshub.onrender.com/

---

Thank you for checking out EduToolsHub — a small but thoughtful suite of tools for learners. The UI is intentionally simple so students can focus on studying: create notes, add tasks and homework, search for learning resources, or perform quick conversions without leaving one small web app.

If you'd like the live site URL updated in this README, or want short screenshots / badges added (license, Python/Django versions, or CI status), tell me what you'd like and I will update the file.
