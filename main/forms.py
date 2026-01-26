from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Item, Comment


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'placeholder': 'Choose a username',
                'autofocus': True,
                'style': 'max-width: 320px;',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name in ['password1', 'password2']:
            field = self.fields[name]
            classes = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = (classes + ' form-control form-control-sm').strip()
            field.widget.attrs.setdefault('style', 'max-width: 320px;')

        self.fields['password1'].widget.attrs.setdefault('placeholder', 'Password')
        self.fields['password2'].widget.attrs.setdefault('placeholder', 'Repeat password')


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['title', 'description', 'status', 'contact', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Short title, e.g. "Lost wallet near park"',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Describe the item, where and when it was lost/found…',
            }),
            'status': forms.Select(attrs={
                'class': 'form-select',
            }),
            'contact': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone number, Telegram, email…',
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
            }),
        }


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username',
            'autofocus': True,
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password',
        })
    )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Write your comment...',
            }),
        }
