from django.contrib import admin
from .models import Pet, CustomUser, Mail, Chat
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm


admin.site.register(Chat)
admin.site.register(Pet)

# Customized Interface for User

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['id', 'username', 'email', 'city', 'picture', 'birthday', 'invitedby']

    fieldsets = (
        (('User'), {'fields': ('id', 'username', 'email', 'picture', 'city', 'birthday', 'invitedby')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)

# class CustomUserAdmin(ModelAdmin):
#     form = CustomUserChangeForm
#     model = CustomUser
#     list_display = ['id', 'username', 'email', 'city', 'picture', 'birthday', 'invitedby']
#
#     fieldsets = (
#         (('User'), {'fields': ('id', 'username', 'email', 'picture', 'city', 'birthday', 'invitedby')}),
#     )
#
# admin.site.register(Mail, CustomMailAdmin)