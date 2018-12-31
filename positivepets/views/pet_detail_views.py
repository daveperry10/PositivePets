from django.views import generic
from positivepets.models import Pet, CustomUser, Chat, FriendGroup, UserState
from positivepets.forms import PetDescriptionForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from datetime import datetime
from django.shortcuts import render
from positivepets.utils.colors import color_map
from positivepets.utils.utils import get_users
from dateutil import tz

class PetDetailView(generic.DetailView):
    model = Pet
    template_name = 'positivepets/pet_detail.html'
    fields = ['description']

    def get_context_data(self, **kwargs):
        context = super(PetDetailView, self).get_context_data(**kwargs)
        pet_id = self.kwargs['pk']
        edit = self.kwargs['edit']
        pet = Pet.objects.get(id=pet_id)
        owner = CustomUser.objects.get(id=pet.user.id)
        description = pet.description
        context['owner'] = owner
        context['description'] = description
        context['edit'] = edit
        context['color'] = self.request.user.color
        context['button_text_color'] = color_map[self.request.user.color.lower()]['button_text_color']
        user_friend_groups = FriendGroup.objects.filter(friendgroupuser__user__id=self.request.user.id)
        selected_friend_group = FriendGroup.objects.get(id=UserState.objects.get(user=self.request.user).ref_id)
        context['user_friend_groups'] = user_friend_groups
        context['selected_friend_group'] = selected_friend_group
        user_list = get_users(self.request.user.id)
        comment_list = Chat.objects.filter(user_id__in=user_list).filter(group=selected_friend_group.id).filter(pet_id=pet_id).order_by('-timestamp')[
                       :15]  # no neg indexing
        context['comment_list'] = comment_list
        return context

def pet_description_edit(request, pk):
    if request.method == 'POST':
        url = reverse('positivepets:pet_detail', kwargs={'pk': pk, 'edit': 1})
        return HttpResponseRedirect(url)


def pet_description_save(request, pk):
    if request.method == 'POST':
        form = PetDescriptionForm(request.POST)
        if form.is_valid():
            a = Pet.objects.get(id=pk)
            a.description = form.data['bigtext']
            a.save()
            url = reverse('positivepets:pet_detail', kwargs={'pk': pk, 'edit': 0})
            return HttpResponseRedirect(url)
    else:
        form = PetDescriptionForm()

    return HttpResponseRedirect(reverse('positivepets:pet_detail', kwargs={'pk': pk, 'edit': 0}))

def pet_comment_message_create(request, action, pet_id):
    context = {}

    # ActiveGroup DropDown List:  1.  get all groups 2. get active group
    user_friend_groups = FriendGroup.objects.filter(friendgroupuser__user__id=request.user.id)
    selected_friend_group = FriendGroup.objects.get(id=UserState.objects.get(user=request.user).ref_id)
    context['user_friend_groups'] = user_friend_groups
    context['selected_friend_group'] = selected_friend_group
    pet = Pet.objects.get(id=pet_id)
    if action == 'submit':
        if request.method == 'POST':
            msg = Chat()
            msg.timestamp = datetime.now()
            msg.user = request.user
            msg.comment = request.POST['textbox']
            msg.group = selected_friend_group
            msg.pet = pet
            msg.save()

    user_list = get_users(request.user.id)
    comment_list = Chat.objects.filter(user_id__in=user_list).filter(group=selected_friend_group.id).filter(pet_id=pet_id).order_by('-timestamp')[:15]  # no neg indexing
    context['comment_list'] = comment_list

    context['user'] = request.user
    context['color'] = request.user.color
    context['description'] = pet.description
    context['owner'] = CustomUser.objects.get(id=pet.user.id)
    context['pet'] = pet
    return render(request, 'positivepets/pet_detail.html', context)