__author__ = 'Navid'
from django import forms
from django.forms import ModelForm
from game_platform.models import Category, Game


class AddGameForm(ModelForm):
    title = forms.CharField(label=(u'Game Title'), widget = forms.TextInput(attrs={'class':'form-control'}))
    picture_url = forms.URLField(required=False, label=(u'Game Picture URL'),
                                 widget = forms.TextInput(attrs={'class':'form-control'}))
    game_url = forms.URLField(label=(u'Your Javascript Game URL'),
                              widget = forms.TextInput(attrs={'class':'form-control'}))
    price = forms.FloatField(label=(u'Game Price'), widget = forms.TextInput(attrs={'class':'form-control'}))
    description = forms.CharField(required=False, label=(u'Description'),
                                  widget = forms.TextInput(attrs={'class':'form-control'}))
    category = forms.ModelChoiceField(label=(u'Category'), queryset=Category.objects.filter(),
                                      empty_label='Choose a Category')

    class Meta:
        model = Game
        exclude = ['developer']

    def clean_title(self):
        title = self.cleaned_data['title']
        try:
            Game.objects.get(title=title)
        except Game.DoesNotExist:
            return title
        raise forms.ValidationError("Game Title already exists, please try another one.")

    def clean_price(self):
        price = self.cleaned_data['price']
        if price > 0:
            return price
        else:
            raise forms.ValidationError("Price has to be a positive number.")


class EditGameForm(ModelForm):
    picture_url = forms.URLField(required=False, label=(u'Game Picture URL'),
                                 widget = forms.TextInput(attrs={'class':'form-control'}))
    game_url = forms.URLField(label=(u'Your Javascript Game URL'),
                              widget = forms.TextInput(attrs={'class':'form-control'}))
    price = forms.FloatField(label=(u'Game Price'), widget = forms.TextInput(attrs={'class':'form-control'}))
    description = forms.CharField(required=False, label=(u'Description'),
                                  widget = forms.TextInput(attrs={'class':'form-control'}))
    category = forms.ModelChoiceField(label=(u'Category'), queryset=Category.objects.filter(),
                                      empty_label='Choose a Category')

    class Meta:
        model = Game
        exclude = ['title', 'developer']

    def clean_price(self):
        price = self.cleaned_data['price']
        if price > 0:
            return price
        else:
            raise forms.ValidationError("Price has to be a positive number.")