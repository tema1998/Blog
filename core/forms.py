from django import forms
from users.models import User

from .models import Post, PostComments, Profile


class CommentForm(forms.ModelForm):
    """
    Form for processing a new comment to the post.
    """

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields["text"].label = ""

    class Meta:
        model = PostComments
        fields = ("text",)
        widgets = {
            "text": forms.TextInput(
                attrs={
                    "class": "bg-gray-100 rounded-full rounded-md max-h-10 shadow-none",
                    "placeholder": "Post a comment...",
                }
            )
        }


class SignupForm(forms.ModelForm):
    """
    Form for processing sign up.
    """

    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Repeat password", widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ("username", "email")

    def clean_password2(self):
        cd = self.cleaned_data
        if cd["password"] != cd["password2"]:
            raise forms.ValidationError("Passwords don't match.")
        if len(cd["password"]) < 8:
            raise forms.ValidationError(
                "The length of password less than 8 symbols."
            )
        return cd["password2"]


class SigninForm(forms.Form):
    """
    Form for processing sign in.
    """

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class AddPostForm(forms.ModelForm):
    """
    Form for processing creating a new post.
    """

    class Meta:
        model = Post
        fields = ("image", "caption")
        widgets = {
            "caption": forms.Textarea(attrs={"style": "max-height: 70px;"})
        }


class EditPostForm(forms.ModelForm):
    """
    Form for processing editing of post.
    """

    class Meta:
        model = Post
        fields = ("image", "caption", "comments_status")
        widgets = {
            "caption": forms.Textarea(attrs={"style": "max-height: 70px;"})
        }


class SettingsForm(forms.ModelForm):
    """
    Form for processing user's settings data.
    """

    class Meta:
        model = Profile
        fields = ("bio", "profile_img", "location")
        widgets = {"bio": forms.Textarea(attrs={"cols": 40, "rows": 5})}
