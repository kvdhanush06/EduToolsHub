from unittest.mock import Mock, patch

from django.test import TestCase

from . import services


class ServicesTests(TestCase):
    def test_convert_length_and_mass(self):
        self.assertEqual(services.convert_length(3, "yard", "foot"), "3 yard = 9 foot")
        self.assertEqual(
            services.convert_length(6, "foot", "yard"), "6 foot = 2.0 yard"
        )
        self.assertEqual(
            services.convert_mass(10, "pound", "kilogram"),
            "10 pound = 4.53592 kilogram",
        )
        self.assertEqual(
            services.convert_mass(2, "kilogram", "pound"),
            "2 kilogram = 4.40924 pound",
        )

    @patch("dashboard.services.requests.get")
    def test_search_books(self, mock_get):
        mock_resp = Mock()
        mock_resp.raise_for_status = Mock()
        mock_resp.json.return_value = {
            "items": [
                {"volumeInfo": {"title": "T1", "imageLinks": {"thumbnail": "thumb"}}}
            ]
        }
        mock_get.return_value = mock_resp

        results = services.search_books("query", limit=1)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["title"], "T1")

    @patch("dashboard.services.requests.get")
    def test_lookup_dictionary(self, mock_get):
        mock_resp = Mock()
        mock_resp.raise_for_status = Mock()
        mock_resp.json.return_value = [
            {
                "phonetics": [{"text": "ph", "audio": "audio.mp3"}],
                "meanings": [{"definitions": [{"definition": "def", "example": "ex"}]}],
            }
        ]
        mock_get.return_value = mock_resp

        res = services.lookup_dictionary("word")
        self.assertEqual(res["definition"], "def")

    @patch("dashboard.services.wikipedia.page")
    def test_lookup_wikipedia(self, mock_page):
        class DummyPage:
            title = "T"

            url = "http://example"

            summary = "S"

        mock_page.return_value = DummyPage()
        info = services.lookup_wikipedia("term")
        self.assertEqual(info["title"], "T")

    @patch("dashboard.services.VideosSearch")
    def test_search_youtube(self, mock_vs):
        mock_instance = Mock()
        mock_instance.result.return_value = {
            "result": [
                {
                    "title": "v",
                    "duration": "1:00",
                    "thumbnails": [{"url": "t"}],
                    "channel": {"name": "c"},
                    "link": "l",
                    "viewCount": {"short": "1K"},
                    "publishedTime": "today",
                    "descriptionSnippet": [{"text": "d"}],
                }
            ]
        }
        mock_vs.return_value = mock_instance

        results = services.search_youtube("q", limit=1)
        self.assertEqual(len(results), 1)
