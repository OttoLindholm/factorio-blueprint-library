from django import forms

from bp_manager.models import Commentary, Blueprint


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
    model = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "tag"})
    )
