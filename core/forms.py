from django import forms
from .models import Commentss, Message

class CommentForm(forms.ModelForm):
    class Meta:
        model = Commentss
        fields = ('text',)

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['message']
        labels = {'message': ""}