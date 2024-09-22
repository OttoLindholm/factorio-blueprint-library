from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from bp_manager.models import Commentary, Blueprint, User


class CommentaryForm(forms.ModelForm):
    content = forms.CharField(
        label="",
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Comment here !",
                "rows": 4,
                "cols": 50,
            }
        ),
    )

    class Meta:
        model = Commentary
        fields = ["content"]


class BlueprintForm(forms.ModelForm):
    class Meta:
        model = Blueprint
        fields = "__all__"
        exclude = ["owner"]


class BlueprintSearchForm(forms.Form):
    query = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "type": "search",
                "placeholder": "Search blueprints",
                "aria-label": "Search"
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
