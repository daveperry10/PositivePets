from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from positivepets.models import CustomUser, UserState, FriendGroup, FriendGroupUser
from positivepets.forms import CustomUserCreationForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.files import File
from django.conf import settings
import os
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



def about_view(request):
    return render(request, 'positivepets/about.html')


def change_active_group(request,redirect, pet_id=1):
    if request.POST:
        # try:
        #     active_group = request.POST['active_friend_group']
        # except:
        #     pass

        # get the group ids for this user
        #group_ids = FriendGroupUser.objects.filter(user=request.user).values('id')

        # get the groups for those ids (this user's groups)
#        groups = FriendGroup.objects.filter(pk__in=group_ids)

        # choose the group id that matches the selected name
        # save that id as ref_id in user_state

        us = UserState.objects.filter(user=request.user).get(name='ActiveGroup')
        us.ref_id = int(request.POST['active_friend_group'])
        us.save()

        if redirect == 'chat':
            return chat_message_create(request, 'none')
        elif redirect == 'email':
            return HttpResponseRedirect(reverse('positivepets:email_folder_show', kwargs={'folder':'inbox'}))
        elif redirect == 'profile':
            return HttpResponseRedirect(reverse('positivepets:profile', kwargs={'friend_id':request.user.id, 'action':'show'}))
        elif redirect == 'pet_detail':
            return HttpResponseRedirect(reverse('positivepets:pet_detail', kwargs={'pk': pet_id, 'edit': 0}))


def group_admin_show(request):
    d = "select f. *, name, username from positivepets_friendgroupuser f, positivepets_friendgroup" + \
    "g, positivepets_customuser c where c.id = f.user_id and f.group_id = g.id order by group_id;"

    context ={}
    context['query_set'] = FriendGroupUser.objects.all().values('user__username', 'group__name').order_by('group__name')

    return render(request, 'positivepets/group_admin.html', context)


from positivepets.forms import GroupNewForm

def group_add_view(request):

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = GroupNewForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            print(form.cleaned_data['name'])
            print(form.cleaned_data['owner'])
            print("is it bound: ", form.is_bound)
            # redirect to a new URL:

        return HttpResponseRedirect(reverse('positivepets:group_admin_show'))
    # if a GET (or any other method) we'll create a blank form
    else:
        form = GroupNewForm()
        form.fields['owner'].queryset = CustomUser.objects.all()

    return render(request, 'positivepets/group_admin.html', {'form': form})