from django.contrib.auth.models import User
from .models import Chat, Pet
from django import forms


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

class PetDescriptionForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['description']