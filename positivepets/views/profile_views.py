from django.views import generic
from positivepets.models import CustomUser, Pet, FriendGroup, UserState
from positivepets.forms import CustomUserChangePictureForm, BioForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from positivepets.utils.colors import color_map
from positivepets.utils.utils import get_users

class ProfileView(generic.ListView):
    template_name = 'positivepets/profile.html'
    fields = ['bio']

    def get_queryset(self):
        return CustomUser.objects.all()

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)

        if (int(self.kwargs['friend_id'])==0) or self.request.user.is_anonymous:
            friend = self.request.user
            context['color'] = 'lightgray'
        else:
            friend = CustomUser.objects.get(id=self.kwargs['friend_id'])

            if friend.color:

                context['color'] = color_map[friend.color.lower()]['display_name']

                try:
                    context['button_text_color'] = color_map[friend.color.lower()]['button_text_color']
                except:
                    context['button_text_color'] = 'rgb(40,40,40)'
            else:
                context['color'] = 'lightgray'
                context['button_text_color'] = 'rgb(40,40,40)'

            context['action'] = self.kwargs['action']
            context['friend'] = friend
            context['pet_list'] = Pet.objects.filter(user=friend.id)
            context['user_list'] = CustomUser.objects.filter(id__in=get_users(self.request.user.id))

            # ActiveGroup DropDown List:  1.  get all groups 2. get active group
            user_friend_groups = FriendGroup.objects.filter(friendgroupuser__user__id=self.request.user.id)
            selected_friend_group = FriendGroup.objects.get(id=UserState.objects.get(user=self.request.user).ref_id)
            context['user_friend_groups'] = user_friend_groups
            context['selected_friend_group'] = selected_friend_group

        return context

def redirect(request):
    # bring user to his/her own profile by default, in "show" mode (not "edit")
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('positivepets:profile', kwargs={'friend_id':request.user.id, 'action':'show'}))
    else:
        return HttpResponseRedirect(reverse('positivepets:profile', kwargs={'friend_id':0, 'action': 'show'}))

def bio_edit(request, friend_id):
    if request.method == 'POST':
        url = reverse('positivepets:profile', kwargs={'friend_id': friend_id, 'action': 'edit_bio'})
        return HttpResponseRedirect(url)

def user_picture_edit(request, friend_id):
    if request.method == 'POST':
        url = reverse('positivepets:profile', kwargs={'friend_id': friend_id, 'action': 'edit_picture'})
        return HttpResponseRedirect(url)

# need to eventually figure out why form.is_valid is False
def bio_save(request, friend_id):
    if request.method == 'POST':
        form = BioForm(request.POST)
        #if form.is_valid():
        a = CustomUser.objects.get(id=friend_id)
        a.bio = form.data['bigtext']
        a.save()
        url = reverse('positivepets:profile', kwargs={'friend_id': friend_id, 'action': 'show'})
        return HttpResponseRedirect(url)
    return HttpResponseRedirect(reverse('positivepets:profile', kwargs={'friend_id': friend_id, 'action': 'show'}))

def user_picture_save(request, friend_id):
    if request.method == 'POST':
        form = CustomUserChangePictureForm(request.POST, request.FILES)
        a = CustomUser.objects.get(id=request.user.id)
        a.picture = request.FILES['picture']
        a.save()
        url = reverse('positivepets:profile', kwargs={'friend_id': request.user.id, 'action': 'show'})
        return HttpResponseRedirect(url)
    url = reverse('positivepets:profile', kwargs={'friend_id': request.user.id, 'action': 'show'})
    return HttpResponseRedirect("www.google.com")
