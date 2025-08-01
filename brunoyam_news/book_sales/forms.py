from django import forms
from .models import Message, Review

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['name', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'name': 'Ваше имя (оставьте пустым для анонимности)',
            'message': 'Ваше сообщение',
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