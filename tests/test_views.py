from bp_manager.models import Like, Tag
from django.test import TestCase
from django.urls import reverse
from bp_manager.models import Blueprint, User
from django.contrib.auth.models import AnonymousUser
from django.test.client import RequestFactory
from bp_manager.views import BlueprintListView

BLUEPRINTS_URL = reverse("bp_manager:index")


class BlueprintListViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.blueprint1 = Blueprint.objects.create(
            title="Test Blueprint 1", user=self.user
        )
        self.blueprint2 = Blueprint.objects.create(
            title="Test Blueprint 2", user=self.user
        )

        self.tag = Tag.objects.create(name="Test Tag")
        self.blueprint1.tags.add(self.tag)

        self.factory = RequestFactory()

    def test_blueprint_list_view_no_filters(self):
        request = self.factory.get(BLUEPRINTS_URL)
        request.user = self.user

        response = BlueprintListView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.blueprint1, response.context_data["blueprint_list"])
        self.assertIn(self.blueprint2, response.context_data["blueprint_list"])

    def test_blueprint_list_view_with_query_filter(self):
        request = self.factory.get(
            BLUEPRINTS_URL, {"query": "Test"}
        )
        request.user = self.user

        response = BlueprintListView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.blueprint1, response.context_data["blueprint_list"])
        self.assertIn(self.blueprint2, response.context_data["blueprint_list"])

    def test_blueprint_list_view_with_tag_filter(self):
        request = self.factory.get(
            BLUEPRINTS_URL, {"tag": "Test Tag"}
        )
        request.user = self.user

        response = BlueprintListView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.blueprint1, response.context_data["blueprint_list"])
        self.assertNotIn(self.blueprint2, response.context_data["blueprint_list"])

    def test_blueprint_list_view_liked_blueprints(self):
        Like.objects.create(user=self.user, blueprint=self.blueprint1)

        request = self.factory.get(
            BLUEPRINTS_URL, {"liked": "true"}
        )
        request.user = self.user

        response = BlueprintListView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.blueprint1, response.context_data["blueprint_list"])
        self.assertNotIn(self.blueprint2, response.context_data["blueprint_list"])

    def test_blueprint_list_view_anonymous_user(self):
        request = self.factory.get(BLUEPRINTS_URL)
        request.user = AnonymousUser()
        response = BlueprintListView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data["liked_blueprints"], [])
