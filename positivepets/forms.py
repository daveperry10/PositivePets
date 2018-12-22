from django.contrib.auth.models import User
from .models import Chat, Pet, Mail

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'email', 'city', 'birthday')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'city', 'picture', 'birthday', 'color')

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']

class ChatMessageForm(forms.ModelForm):
   class Meta:
        model = Chat
        fields = ['comment']

class MailForm(forms.ModelForm):
   class Meta:
        model = Mail
        fields = ['message', 'subject']

class PetDescriptionForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['description']

class BioForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['bio']

class CustomUserChangePictureForm(forms.Form):
    file = forms.FileField()
    # class Meta:
    #     model = CustomUser
    #     fields = ['picture']

class PictureSearchForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)