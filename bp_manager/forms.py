from django import forms
from django.contrib.auth.forms import UserCreationForm

from bp_manager.models import Commentary, Blueprint, User, Tag


class CommentaryForm(forms.ModelForm):
    content = forms.CharField(
        label="",
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Comment here !",
                "rows": 2,
                "cols": 50,
            }
        ),
    )

    class Meta:
        model = Commentary
        fields = ["content"]


class BlueprintForm(forms.ModelForm):
    existing_tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={"size": 5}),
    )
    new_tags = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Add new tags with commas"}),
    )

    class Meta:
        model = Blueprint
        fields = [
            "title",
            "description",
            "blueprint_string",
            "blueprint_image",
            "existing_tags",
            "new_tags",
        ]

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()

        existing_tags = self.cleaned_data["existing_tags"]
        for tag in existing_tags:
            instance.tags.add(tag)

        new_tags_str = self.cleaned_data["new_tags"]
        if new_tags_str:
            new_tags_list = [tag.strip() for tag in new_tags_str.split(",")]
            for tag_name in new_tags_list:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                instance.tags.add(tag)

        return instance


class BlueprintSearchForm(forms.Form):
    query = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "type": "search",
                "placeholder": "Search blueprints",
                "aria-label": "Search",
            }
        ),
    )


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password1",
            "password2",
        )


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
        )


class UserDeleteForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(), label="Password")
