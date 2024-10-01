from django.contrib.auth import get_user_model
from django.contrib.sessions.middleware import SessionMiddleware

from bp_manager.models import Like, Tag, Commentary
from django.test import TestCase
from django.urls import reverse
from bp_manager.models import Blueprint
from django.contrib.auth.models import AnonymousUser
from django.test.client import RequestFactory, Client
from bp_manager.views import BlueprintListView, BlueprintDetailView, ToggleLikeView

User = get_user_model()
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


class UserRegisterViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_user_registration(self):
        data = {
            "username": "newuser",
            "password1": "strong_password123",
            "password2": "strong_password123",
            "email": "newuser@example.com",
        }
        response = self.client.post(reverse("bp_manager:user-register"), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="newuser").exists())


class UserUpdateViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.client = Client()

    def test_update_user_profile(self):
        self.client.login(username="testuser", password="password")
        data = {"username": "updateduser", "email": "updateduser@example.com"}
        response = self.client.post(
            reverse("bp_manager:user-update", kwargs={"pk": self.user.pk}), data
        )
        self.assertEqual(response.status_code, 302)
        updated_user = User.objects.get(pk=self.user.pk)
        self.assertEqual(updated_user.username, "updateduser")
        self.assertEqual(updated_user.email, "updateduser@example.com")


class UserDeleteViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.client = Client()
        self.USER_DELETE_URL = reverse(
            "bp_manager:user-delete", kwargs={"pk": self.user.pk}
        )

    def test_delete_user(self):
        self.client.login(username="testuser", password="password")
        data = {"password": "password"}
        response = self.client.post(self.USER_DELETE_URL, data)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(User.objects.filter(username="testuser").exists())

    def test_delete_user_incorrect_password(self):
        self.client.login(username="testuser", password="password")
        data = {"password": "wrong_password"}
        response = self.client.post(self.USER_DELETE_URL, data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username="testuser").exists())


class CommentaryCreateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.blueprint = Blueprint.objects.create(
            title="Test Blueprint", user=self.user
        )
        self.client.login(username="testuser", password="12345")
        session = self.client.session
        session["blueprint_id"] = self.blueprint.id
        session.save()

    def test_create_commentary(self):
        response = self.client.post(
            reverse("bp_manager:add-comment"), {"content": "Test commentary"}
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Commentary.objects.count(), 1)
        self.assertEqual(response.url, Commentary.objects.first().get_absolute_url())


class CommentaryUpdateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.blueprint = Blueprint.objects.create(
            title="Test Blueprint", user=self.user
        )
        self.commentary = Commentary.objects.create(
            content="Test commentary", blueprint=self.blueprint, user=self.user
        )
        self.client.login(username="testuser", password="12345")

    def test_update_commentary(self):
        response = self.client.post(
            reverse("bp_manager:comment-update", kwargs={"pk": self.commentary.pk}),
            {"content": "Updated commentary"},
        )
        self.commentary.refresh_from_db()
        self.assertEqual(self.commentary.content, "Updated commentary")
        self.assertEqual(response.url, Commentary.objects.first().get_absolute_url())


class CommentaryDeleteViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.blueprint = Blueprint.objects.create(
            title="Test Blueprint", user=self.user
        )
        self.commentary = Commentary.objects.create(
            content="Test commentary", blueprint=self.blueprint, user=self.user
        )
        self.client.login(username="testuser", password="12345")

    def test_delete_commentary(self):
        response = self.client.post(
            reverse("bp_manager:comment-delete", kwargs={"pk": self.commentary.pk})
        )
        self.assertEqual(Commentary.objects.count(), 0)
        self.assertEqual(
            response.url,
            reverse("bp_manager:blueprint-detail", kwargs={"pk": self.blueprint.pk})
            + "#comments",
        )
