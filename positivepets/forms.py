from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Chat, Pet, CustomUser

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'email', 'city', 'birthday')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('id','email', 'username', 'city', 'picture', 'birthday', 'color')

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = CustomUser
        fields = ['id','username', 'email', 'password']

class ChatMessageForm(forms.ModelForm):
   class Meta:
        model = Chat
        fields = ['comment']

class EmailForm(forms.Form):

    recipients = forms.ModelMultipleChoiceField(queryset=None, widget=forms.CheckboxSelectMultiple)
    subject = forms.CharField(label='Subject', max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'special', 'size': '40'}))
    message = forms.CharField(label='Message', max_length=500, widget=forms.Textarea, required=False)

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

class PictureSearchForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)

class GroupNewForm(forms.Form):
    name = forms.CharField(label='Group Name', max_length=100)
    owner = forms.ModelMultipleChoiceField(label='Group Owner', queryset=None)

class GroupAssignmentForm(forms.Form):
    owner = forms.ModelMultipleChoiceField(queryset=None)
    name = forms.CharField(label='Group Owner', max_length=100)