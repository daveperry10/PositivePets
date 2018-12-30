from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from positivepets.models import CustomUser, UserState, FriendGroup, FriendGroupUser
from positivepets.forms import CustomUserCreationForm,CustomUserChangePictureForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.files import File
from django.conf import settings
import os
from positivepets.utils.colors import color_map
from positivepets.views.chat_views import chat_message_create

class UserFormView(View):
    form_class = CustomUserCreationForm
    template_name = 'positivepets/registration_form.html'

    #display a blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form':form, 'color': request.user.color})

    def post(self, request):
        """
        Create a new user
        Assign them to a default friend group
        Set their active friend group to the default friend group
        Give them a default color (light gray) - they can change it themselves

        :param request:
        :return:
        """

        # need request.FILES or image upload won't work.
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data['username'].lower()
            password = form.cleaned_data['password1'].lower()
            try:
                user.picture = request.FILES['picture']
            except:
                #if they don't put a picture, give them the star icon.
                try:
                    user.picture.save('star_icon.jpg', File(open(os.path.join(settings.STATIC_ROOT, 'star_icon.jpg'),'rb')))
                except:
                    pass
            user.set_password(password)
            user.invitedby = request.user
            user.color = 'lightgray'
            user.save()
            user = authenticate(username=user.username, password=password)

            # Assign them to a default user group
            fg = FriendGroup.objects.get(name='Unassigned')
            fgu = FriendGroupUser()
            fgu.group = fg
            fgu.user = user
            fgu.save()

            # Set user-state activegroup to the default user group
            us = UserState()
            us.name = 'ActiveGroup'
            us.user = user
            us.ref_id = fg.id
            us.value = ""
            us.save()

            if user is not None:
                if user.is_active:
                    return redirect('/')

        return render(request, self.template_name, {'form':form, 'color': request.user.color})


def color_change_view(request):
    try:
        display_name = color_map[request.user.color.lower()]['display_name']
    except:
        display_name = 'Light Gray'

    context = {'color_map': color_map, 'color': request.user.color, 'color_name':display_name}
    return render(request, 'positivepets/color_change_form.html', context)

def color_save_view(request):

    if request.POST:
        user = request.user
        color_display_name = request.POST['color']


        for k, v in color_map.items():
            if v['display_name'] == color_display_name:
                user.color = k

        user.save()

        return HttpResponseRedirect(reverse('positivepets:profile', kwargs={'friend_id':request.user.id, 'action': 'show'}))

    return HttpResponseRedirect(reverse('positivepets:profile', kwargs={'friend_id': request.user.id, 'action': 'show'}))

def about_view(request):
    return render(request, 'positivepets/about.html')


def change_active_group(request,redirect):
    if request.POST:
        try:
            active_group = request.POST['active_friend_group']
        except:
            pass

        #us = UserState.objects.filter(user=request.user).values('name')

        # get the group ids for this user
        group_ids = FriendGroupUser.objects.filter(user=request.user).values('id')

        # get the groups for those ids (this user's groups)
        groups = FriendGroup.objects.filter(pk__in=group_ids)

        # choose the group id that matches the selected name
        # save that id as ref_id in user_state

    us = UserState.objects.filter(user=request.user).get(name='ActiveGroup')
    us.ref_id = int(request.GET['active_friend_group'])
    us.save()
    if redirect == 'chat':
        return chat_message_create(request)
    elif redirect == 'email':
        #return MailCreate.as_view()
        return HttpResponseRedirect(reverse('positivepets:email_folder_show',kwargs={'folder':'inbox'}))
    if redirect == 'profile':
        return HttpResponseRedirect(reverse('positivepets:profile', kwargs={'friend_id':request.user.id, 'action':'show'}))