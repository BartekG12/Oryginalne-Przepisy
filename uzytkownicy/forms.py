from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profil, Message

class TworzenieUzytkownika(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'email', 'username', 'password1', 'password2']
        labels = {
            'first_name': 'Name',
        }

    def __init__(self, *args, **kwargs):
        super(TworzenieUzytkownika, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

class FormularzProfil(ModelForm):
    class Meta:
        model = Profil
        fields = ['name', 'email', 'username', 'bio', 'self_pitch', 'profile_image', 
        'social_youtube', 'social_instagram', 'social_facebook']

        labels = {
            'name': 'Imię i nazwisko',
            'email': 'Adres E-mail',
            'username': 'Nazwa Użytkownika',
            'bio': 'Hasło',
            'self_pitch': 'O mnie',
            'profile_image': 'Zdjęcie profilowe',
            'social_youtube': 'Link youtube',
            'social_instagram': 'Link instagram',
            'social_facebook': 'Link facebook',
        }

    def __init__(self, *args, **kwargs):
        super(FormularzProfil, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['name', 'email', 'subject', 'body']

        labels = {
            'name': 'Imię i nazwisko',
            'email': 'Adres E-mail',
            'subject': 'Temat',
            'body': 'Treść',
        }

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})