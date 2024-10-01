import os

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from bp_manager.models import Tag, Blueprint, Commentary, user_blueprint_path
from django.core.files.uploadedfile import SimpleUploadedFile

User = get_user_model()


class BaseTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )
        self.tag = Tag.objects.create(name="Test Tag")
        self.image_file = SimpleUploadedFile(
            name="foo.gif",
            content=b"GIF87a\x01\x00\x01\x00\x80\x01\x00\x00\x00\x00ccc,"
                    b"\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00",
        )

        self.blueprint = Blueprint.objects.create(
            user=self.user,
            title="Test Blueprint",
            description="A blueprint for testing.",
            blueprint_string="Blueprint data",
            blueprint_image=self.image_file,
        )
        self.commentary = Commentary.objects.create(
            user=self.user, blueprint=self.blueprint, content="This is a test comment."
        )

    def tearDown(self):
        blueprint = Blueprint.objects.filter(user=self.user).first()
        if blueprint and blueprint.blueprint_image:
            if os.path.exists(blueprint.blueprint_image.path):
                os.remove(blueprint.blueprint_image.path)


class BlueprintModelTest(BaseTestCase):
    def setUp(self):
        super().setUp()

    def test_blueprint_creation(self):
        self.assertEqual(self.blueprint.title, "Test Blueprint")
        self.assertEqual(self.blueprint.description, "A blueprint for testing.")
        self.assertEqual(self.blueprint.user.username, "testuser")
        self.assertTrue(self.blueprint.blueprint_image)

    def test_image_upload_path(self):
        expected_path = f"user_{self.user.id}/{self.image_file.name}"
        self.assertEqual(self.blueprint.blueprint_image.name, expected_path)

    def test_get_absolute_url(self):
        self.assertEqual(
            self.blueprint.get_absolute_url(),
            reverse("bp_manager:blueprint-detail", kwargs={"pk": self.blueprint.pk}),
        )


class CommentaryModelTest(BaseTestCase):
    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_commentary_creation(self):
        self.assertEqual(self.commentary.content, "This is a test comment.")
        self.assertEqual(self.commentary.user.username, "testuser")

    def test_get_absolute_url(self):
        expected_url = (
                reverse("bp_manager:blueprint-detail", kwargs={"pk": self.blueprint.pk})
                + f"#comment-{self.commentary.pk}"
        )
        self.assertEqual(self.commentary.get_absolute_url(), expected_url)
