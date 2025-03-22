from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from .models import Book, CustomUser

import re

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField()
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'role')

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Логин', max_length=254)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

    class Meta:
        fields = ['username', 'password']


class BookForm(forms.ModelForm):
    published_date = forms.DateField(
        required = False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Book
        fields = ['title', 'author', 'price', 'published_date']
    
    def clean_price(self):
        price = self.cleaned_data.get('price')

        if price is not None and price <= 0:
            raise forms.ValidationError("Цена не может быть отрицательной!")

        return price


    def clean_fields(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        author = cleaned_data.get('author')
        book_id = self.instance.id

        if Book.objects.filter(title=title, author=author).exclude(id=book_id).exists():
            raise forms.ValidationError("Книга с таким названием и автором уже существует.")

        return cleaned_data

class CustomUserForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not re.match(r'^[A-Za-zА-Яа-яёЁ]+$', first_name):
            raise forms.ValidationError('Имя может содержать только буквы.')
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not re.match(r'^[A-Za-zА-Яа-яёЁ]+$', last_name):
            raise forms.ValidationError('Фамилия может содержать только буквы.')
        return last_name 
