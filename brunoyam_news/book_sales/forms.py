from django import forms
from .models import Contact, ChatMessage, Review

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'name': 'Ваше имя',
            'email': 'Email',
            'message': 'Сообщение',
        }


class ChatMessageForm(forms.ModelForm):
    class Meta:
        model = ChatMessage
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4}),
        }
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['name', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'name': 'Ваше имя (оставьте пустым для анонимности)',
            'message': 'Ваш отзыв',
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        return name.strip() if name.strip() else "Аноним"