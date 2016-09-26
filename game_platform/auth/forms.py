__author__ = 'Navid'
from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from game_platform.models import Player, Developer
from django.contrib.auth import authenticate

class RegistrationForm(ModelForm):
    username = forms.CharField(label=(u'Username'), widget = forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(label=(u'E-mail'), widget = forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(label=(u'Password'), widget = forms.PasswordInput(render_value=False,
                                                                                 attrs={'class':'form-control'}))
    password2 = forms.CharField(label=(u'Re-type Password'), widget = forms.PasswordInput(render_value=False,
                                                                                          attrs={'class':'form-control'}))

    class Meta:
        model = Player  # because both of them has the same attributes, it is enough to implement only one
        exclude = ['user']

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError("Username already exists, please try another one.")

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError("E-mail already exists, please try another one.")

    #def save(self, commit=True):
    #    user = super(RegistrationForm, self).save(commit=False)
    #    if commit:
    #        user.is_active = False # not active until he opens activation link
    #        user.save()
    #    return user

    def clean(self):
        password = self.cleaned_data.get('password', None)
        password2 = self.cleaned_data.get('password2', None)
        if password != password2:
            raise forms.ValidationError("The passwords do not match. Please try again.")
        return self.cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(label=(u'Username'), widget = forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(label=(u'Password'), widget = forms.PasswordInput(render_value=False,
                                                                                 attrs={'class':'form-control'}))


    def clean(self):
        username = self.cleaned_data.get('username', None)
        password = self.cleaned_data.get('password', None)
        user_tmp = authenticate(username=username, password=password)
        if user_tmp is None:
            raise forms.ValidationError("Wrong username or password.")
        return self.cleaned_data
