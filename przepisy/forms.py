from django.forms import ModelForm
from django import forms
from .models import Przepis, Ocena

class PrzepisFormularz(ModelForm):
    class Meta:
        model = Przepis
        fields = ['title', 'featured_image', 'description', 'tags']
        widgets = {
            'tags':forms.CheckboxSelectMultiple(),
        }
        labels = {
            'title':'Nazwa',
            'featured_image':'Zdjęcie',
            'description':'Opis',
            'tags':'Tagi',
        }
    def __init__(self, *args, **kwargs):
        super(PrzepisFormularz, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

        # self.fields['title'].widget.attrs.update(
        #     {'class':'input', 'placeholder': 'Dodaj tytuł'})

class ReviewForm(ModelForm):
    class Meta:
        model = Ocena
        fields = ['value', 'body']

        labels = {
            'value':'Zamieść komantarz',
            'body':'Dodaj komentarz/ocenę',
        }

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})
            
class ProsbaForm(ModelForm):
    class Meta:
        model = Przepis
        fields = ['was_asked']