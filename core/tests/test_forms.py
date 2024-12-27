from core.forms import *
from django.test import TestCase


class CommentFormTest(TestCase):

    def test_comment_form_text_field_label(self):
        form = CommentForm()
        self.assertTrue(form.fields["text"].label == "")

    def test_comment_form_text_field_widgets(self):
        form = CommentForm()
        self.assertEqual(
            form.fields["text"].widget.attrs["class"],
            "bg-gray-100 rounded-full rounded-md max-h-10 " "shadow-none",
        )
        self.assertEqual(
            form.fields["text"].widget.attrs["placeholder"],
            "Post a comment...",
        )


class SignupFormTest(TestCase):

    def test_signup_form_field_labels(self):
        form = SignupForm()
        self.assertTrue(form.fields["password"].label == "Password")
        self.assertTrue(form.fields["password2"].label == "Repeat password")

    def test_signup_form_passwords_are_not_equal(self):
        form_data = {
            "username": "user1",
            "password": "pass123",
            "password2": "pass321",
            "email": "email@mail.ru",
        }
        form = SignupForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_signup_form_passwords_are_equal(self):
        form_data = {
            "username": "user1",
            "password": "pass123pass123",
            "password2": "pass123pass123",
            "email": "email@mail.ru",
        }
        form = SignupForm(data=form_data)
        self.assertTrue(form.is_valid())

    # def test_signup_form_passwords_are_not_equal_validation_error(self):
    #     form_data = {'username': 'user1',
    #                  'password': 'pass123',
    #                  'password2': 'pass321',
    #                  'email': 'email@mail.ru'}
    #     with self.assertRaisesMessage(forms.ValidationError, 'Passwords don\'t match.'):
    #         form = SignupForm(data=form_data)
    #         form.is_valid()


class AddPostFormTest(TestCase):

    def test_add_post_form_caption_field_widgets(self):
        form = AddPostForm()
        self.assertEqual(
            form.fields["caption"].widget.attrs["style"], "max-height: 70px;"
        )


class EditPostFormTest(TestCase):

    def test_edit_post_form_caption_field_widgets(self):
        form = EditPostForm()
        self.assertEqual(
            form.fields["caption"].widget.attrs["style"], "max-height: 70px;"
        )


class SettingsFormTest(TestCase):

    def test_settings_form_bio_field_widgets(self):
        form = SettingsForm()
        self.assertEqual(form.fields["bio"].widget.attrs["cols"], 40)
        self.assertEqual(form.fields["bio"].widget.attrs["rows"], 5)
