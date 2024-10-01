from django.contrib.sessions.middleware import SessionMiddleware

from bp_manager.models import Like, Tag
from django.test import TestCase
from django.urls import reverse
from bp_manager.models import Blueprint, User
from django.contrib.auth.models import AnonymousUser
from django.test.client import RequestFactory
from bp_manager.views import BlueprintListView, BlueprintDetailView, ToggleLikeView

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
        request = self.factory.get(BLUEPRINTS_URL, {"query": "Test"})
        request.user = self.user

        response = BlueprintListView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.blueprint1, response.context_data["blueprint_list"])
        self.assertIn(self.blueprint2, response.context_data["blueprint_list"])

    def test_blueprint_list_view_with_tag_filter(self):
        request = self.factory.get(BLUEPRINTS_URL, {"tag": "Test Tag"})
        request.user = self.user

        response = BlueprintListView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.blueprint1, response.context_data["blueprint_list"])
        self.assertNotIn(self.blueprint2, response.context_data["blueprint_list"])

    def test_blueprint_list_view_liked_blueprints(self):
        Like.objects.create(user=self.user, blueprint=self.blueprint1)

        request = self.factory.get(BLUEPRINTS_URL, {"liked": "true"})
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


class BlueprintDetailViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.blueprint = Blueprint.objects.create(
            title="Test Blueprint", user=self.user
        )
        self.factory = RequestFactory()
        self.BLUEPRINT_DETAIL_URL = reverse(
            "bp_manager:blueprint-detail", kwargs={"pk": self.blueprint.pk}
        )

    @staticmethod
    def add_session_to_request(request):
        middleware = SessionMiddleware(lambda x: None)
        middleware.process_request(request)
        request.session.save()

    def test_blueprint_detail_view(self):
        request = self.factory.get(self.BLUEPRINT_DETAIL_URL)
        request.user = self.user
        self.add_session_to_request(request)

        response = BlueprintDetailView.as_view()(request, pk=self.blueprint.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data["blueprint"], self.blueprint)
        self.assertIsNotNone(response.context_data["commentary_form"])

    def test_blueprint_detail_view_anonymous_user(self):
        request = self.factory.get(self.BLUEPRINT_DETAIL_URL)
        request.user = AnonymousUser()
        self.add_session_to_request(request)

        response = BlueprintDetailView.as_view()(request, pk=self.blueprint.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data["blueprint"], self.blueprint)
        self.assertIsNotNone(response.context_data["commentary_form"])


class ToggleLikeViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.blueprint = Blueprint.objects.create(
            title="Test Blueprint", user=self.user
        )
        self.factory = RequestFactory()
        self.TOGGLE_LIKE_URL = reverse(
            "bp_manager:toggle-like", kwargs={"pk": self.blueprint.pk}
        )

    def test_toggle_like_view_like(self):
        request = self.factory.post(self.TOGGLE_LIKE_URL)
        request.user = self.user

        response = ToggleLikeView.as_view()(request, pk=self.blueprint.pk)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Like.objects.filter(user=self.user, blueprint=self.blueprint).exists()
        )

    def test_toggle_like_view_unlike(self):
        Like.objects.create(user=self.user, blueprint=self.blueprint)

        request = self.factory.post(self.TOGGLE_LIKE_URL)
        request.user = self.user

        response = ToggleLikeView.as_view()(request, pk=self.blueprint.pk)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            Like.objects.filter(user=self.user, blueprint=self.blueprint).exists()
        )
