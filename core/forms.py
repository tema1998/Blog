from django import forms
from .models import PostComments, Message

class CommentForm(forms.ModelForm):
    class Meta:
        model = PostComments
        fields = ('text',)

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['message']
        labels = {'message': ""}