from django import forms
from django.core.exceptions import ValidationError
from .models import Post, User


class PostForm(forms.Form):
    class Meta:
        model = Post
        fields = ('author', 'categoryType', 'postCategory', 'title', 'text')

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['author'].label = 'Автор:'
        self.fields['categoryType'].label = 'Тип публикации:'
        self.fields['postCategory'].label = 'Категория:'
        self.fields['title'].label = 'Название публикации:'
        self.fields['text'].label = 'Текст публикации:'

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        text = cleaned_data.get('text')
        if title is not None and len(title) < 20:
            raise ValidationError({
                'title': 'Описание не может быть менее 20 символов.'
            })
        if title[0].islower():
            raise ValidationError({
                'title': 'Описание не может начинаться с маленькой буквы.'
            })
        if text == title:
            raise ValidationError(
                'Описание не должно быть идентично тексту поста.'
            )
        return cleaned_data


class ProfileUserForm(forms.Form):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name'
        ]
