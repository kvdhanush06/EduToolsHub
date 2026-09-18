from unittest.mock import Mock, patch

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

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


class LogoutViewTests(TestCase):
    """Regression tests for the broken navbar logout.

    Django >= 5.0 only allows POST on LogoutView; a plain <a> link (GET)
    returns 405 and does not log the user out. The navbar must submit a
    CSRF-protected POST form instead.
    """

    def setUp(self):
        self.password = "secret-pass-123"
        self.user = get_user_model().objects.create_user(
            username="tester", password=self.password
        )

    def test_logout_via_get_is_rejected(self):
        self.client.login(username="tester", password=self.password)
        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 405)

    def test_logout_via_post_logs_user_out(self):
        self.client.login(username="tester", password=self.password)
        response = self.client.post(reverse("logout"))
        # No next_page is configured, so LogoutView renders the template.
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "dashboard/logout.html")

        # Session must no longer hold the authenticated user id.
        self.assertNotIn("_auth_user_id", self.client.session)

        # A protected page must now redirect to login.
        protected = self.client.get(reverse("notes"))
        self.assertEqual(protected.status_code, 302)
        self.assertIn(reverse("login"), protected.url)

    def test_logout_post_requires_csrf_token(self):
        csrf_client = Client(enforce_csrf_checks=True)
        csrf_client.login(username="tester", password=self.password)
        # POST without a CSRF token must be rejected.
        response = csrf_client.post(reverse("logout"))
        self.assertEqual(response.status_code, 403)
        # And the user is still logged in.
        self.assertIn("_auth_user_id", csrf_client.session)

    def test_navbar_renders_post_form_not_get_link(self):
        self.client.login(username="tester", password=self.password)
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

        content = response.content.decode()
        # The logout control must be a POST form pointing at the logout URL.
        self.assertIn(f'action="{reverse("logout")}"', content)
        self.assertIn('method="post"', content)
        # It must carry a CSRF token.
        self.assertIn('name="csrfmiddlewaretoken"', content)
        # And there must be no plain GET link to /logout/ anymore.
        self.assertNotIn(f'href="{reverse("logout")}"', content)
