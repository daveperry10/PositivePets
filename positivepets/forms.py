from django.contrib.auth.models import User
from .models import Chat, Pet, Mail

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'email', 'city', 'picture', 'birthday')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'city', 'picture', 'birthday')

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

class CustomUserChangePictureForm(forms.Form):
    file = forms.FileField()
    # class Meta:
    #     model = CustomUser
    #     fields = ['picture']