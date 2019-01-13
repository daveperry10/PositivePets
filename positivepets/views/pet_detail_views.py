"""
The Pet model is managed through Generic Class Based Views with very little modification.

    Classes:
    - PetDetailView(generic.DetailView):

    Functions:
    - pet_description_edit(request, pet_id):
    - pet_description_save(request, pet_id):
    - pet_comment_message_create(request, action, pet_id):

"""

from datetime import datetime
from dateutil import tz
from django.views import generic
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from positivepets.models import Pet, CustomUser, Chat, FriendGroup, UserState
from positivepets.forms import PetDescriptionForm
from positivepets.utils import color_map, get_active_friendgroup, add_standard_context


class PetDetailView(generic.DetailView):
    model = Pet
    template_name = 'positivepets/pet_detail.html'
    fields = ['description']

    def get_context_data(self, **kwargs):
        context = super(PetDetailView, self).get_context_data(**kwargs)
        context = add_standard_context(self.request,context)

        pet_id = self.kwargs['pk']
        action = self.kwargs['action']
        pet = Pet.objects.get(id=pet_id)
        owner = CustomUser.objects.get(id=pet.user.id)
        description = pet.description
        context['owner'] = owner
        context['description'] = description
        context['action'] = action


        selected_friend_group = FriendGroup.objects.get(id=UserState.objects.get(user=self.request.user).ref_id)
        user_list = get_active_friendgroup(self.request.user.id)

        comment_list = Chat.objects.filter(user_id__in=user_list).filter(group=selected_friend_group.id).filter(pet_id=pet_id).order_by('-timestamp')[
                       :15]  # no neg indexing
        context['comment_list'] = comment_list
        return context

def pet_description_edit(request, pet_id):
    if request.method == 'POST':
        url = reverse('positivepets:pet_detail', kwargs={'pk': pet_id, 'action': 'edit'})
        return HttpResponseRedirect(url)


def pet_description_save(request, pet_id):
    if request.method == 'POST':
        form = PetDescriptionForm(request.POST)
        if form.is_valid():
            a = Pet.objects.get(id=pet_id)
            a.description = form.data['bigtext']
            a.save()
            url = reverse('positivepets:pet_detail', kwargs={'pk': pet_id, 'action': 'show'})
            return HttpResponseRedirect(url)
    else:
        form = PetDescriptionForm()

    return HttpResponseRedirect(reverse('positivepets:pet_detail', kwargs={'pk': pet_id, 'action': 'show'}))


def pet_comment_message_create(request, action, pet_id):
    context = add_standard_context(request,{})
    selected_friend_group = FriendGroup.objects.get(id=UserState.objects.get(user=request.user).ref_id)
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

    user_list = get_active_friendgroup(request.user.id)
    comment_list = Chat.objects.filter(user_id__in=user_list).filter(group=selected_friend_group.id).filter(pet_id=pet_id).order_by('-timestamp')[:15]  # no neg indexing

    context['comment_list'] = comment_list
    context['user'] = request.user
    context['description'] = pet.description
    context['owner'] = CustomUser.objects.get(id=pet.user.id)
    context['pet'] = pet

    return render(request, 'positivepets/pet_detail.html', context)