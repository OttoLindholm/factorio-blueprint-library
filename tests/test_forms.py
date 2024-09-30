from django.contrib.auth import get_user_model
from django.test import TestCase

from bp_manager.forms import CommentaryForm


class LoggedInUserTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="TestUser",
            password="TestPassword",
        )

    def setUp(self):
        self.client.force_login(self.user)


class CommentaryFormTest(LoggedInUserTestCase):

    def test_commentary_create_is_valid(self):
        form_data = {
            "content": "Test commentary",
        }
        form = CommentaryForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
