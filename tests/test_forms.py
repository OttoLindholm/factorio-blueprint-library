from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from bp_manager.forms import (
    CommentaryForm,
    BlueprintForm,
    UserRegistrationForm,
    UserUpdateForm,
)
from bp_manager.models import Tag


class LoggedInUserTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="TestUser",
            password="TestPassword",
        )

    def setUp(self):
        self.client.force_login(self.user)
        self.tag1 = Tag.objects.create(name="Tag1")
        self.tag2 = Tag.objects.create(name="Tag2")
        self.image_file = SimpleUploadedFile(
            name="foo.gif",
            content=b"GIF87a\x01\x00\x01\x00\x80\x01\x00\x00\x00\x00ccc,"
            b"\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00",
        )


class CommentaryFormTest(LoggedInUserTestCase):

    def test_commentary_create_is_valid(self):
        form_data = {
            "content": "Test commentary",
        }
        form = CommentaryForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class BlueprintFormTest(LoggedInUserTestCase):
    def test_valid_form_with_existing_tags(self):
        form_data = {
            "title": "Test Blueprint",
            "description": "A blueprint for testing.",
            "blueprint_string": "some blueprint string",
            "existing_tags": [self.tag1.id],
            "new_tags": "",
        }
        form = BlueprintForm(data=form_data, files={"blueprint_image": self.image_file})
        form.instance.user = self.user
        self.assertTrue(form.is_valid(), msg=f"Form errors: {form.errors}")
        blueprint = form.save()
        self.assertEqual(blueprint.tags.count(), 1)
        self.assertIn(self.tag1, blueprint.tags.all())

    def test_valid_form_with_new_tags(self):
        form_data = {
            "title": "Test Blueprint",
            "description": "A blueprint for testing.",
            "blueprint_string": "some blueprint string",
            "existing_tags": [],
            "new_tags": "Tag3, Tag4",
        }
        form = BlueprintForm(data=form_data, files={"blueprint_image": self.image_file})
        form.instance.user = self.user
        self.assertTrue(form.is_valid(), msg=f"Form errors: {form.errors}")
        blueprint = form.save()
        self.assertEqual(blueprint.tags.count(), 2)
        self.assertIn(Tag.objects.get(name="Tag3"), blueprint.tags.all())
        self.assertIn(Tag.objects.get(name="Tag4"), blueprint.tags.all())

    def test_invalid_form(self):
        form_data = {
            "title": "",
            "description": "",
            "blueprint_string": "",
            "blueprint_image": None,
            "existing_tags": [],
            "new_tags": "",
        }
        form = BlueprintForm(data=form_data)
        self.assertFalse(form.is_valid())


class UserRegistrationFormTest(TestCase):
    def test_valid_registration_form(self):
        form_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password1": "Password_123",
            "password2": "Password_123",
        }
        form = UserRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertIsNotNone(get_user_model().objects.get(username="testuser"))

    def test_invalid_registration_form(self):
        form_data = {
            "username": "",
            "email": "test@example.com",
            "password1": "Password_123",
            "password2": "Password_456",
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())


class UserUpdateFormTest(LoggedInUserTestCase):

    def test_valid_update_form(self):
        form_data = {
            "username": "newusername",
            "email": "newemail@example.com",
        }
        form = UserUpdateForm(instance=self.user, data=form_data)
        self.assertTrue(form.is_valid())
        updated_user = form.save()
        self.assertEqual(updated_user.username, form_data["username"])
        self.assertEqual(updated_user.email, form_data["email"])

    def test_invalid_update_form(self):
        form_data = {
            "username": "",
            "email": "newemail@example.com",
        }
        form = UserUpdateForm(instance=self.user, data=form_data)
        self.assertFalse(form.is_valid())
