from django.contrib import admin
from .models import Pet
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

admin.site.register(Pet)

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username', 'city', 'picture', 'birthday']

    fieldsets = (
        (('User'), {'fields': ('username', 'email', 'picture', 'city', 'birthday')}),
    )
admin.site.register(CustomUser, CustomUserAdmin)