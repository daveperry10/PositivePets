"""
    Classes:
    - PetDetailView(generic.DetailView):
    - PetCreate(generic.CreateView):
    - PetUpdate(generic.UpdateView):
    - PetDelete(generic.DeleteView):

    Views:
    - pet_description_edit(request, pet_id):
    - pet_description_save(request, pet_id):
    - pet_comment_message_create(request, action, pet_id):
    - user_pets_show(request, friend_id):
"""

from datetime import datetime
from django.views import generic
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.urls import reverse_lazy
from positivepets.models import Pet, CustomUser, Chat, FriendGroup, UserState
from positivepets.forms import PetDescriptionForm
from positivepets.utils import get_active_friendgroup, add_standard_context

class PetCreate(generic.CreateView):
    model = Pet
    fields = ['name', 'type', 'breed', 'picture']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(PetCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(PetCreate, self).get_context_data(**kwargs)
        return add_standard_context(self.request, context)

class PetUpdate(generic.UpdateView):
    model = Pet
    fields = ['name', 'type', 'breed', 'picture']

    def get_context_data(self, **kwargs):
        context = super(PetUpdate, self).get_context_data(**kwargs)
        return add_standard_context(self.request, context)

class PetDelete(generic.DeleteView):
    model=Pet
    def get_success_url(self):
        return reverse_lazy('positivepets:user_pets_show', kwargs={'friend_id': self.request.user.id})

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

        user_friend_groups = FriendGroup.objects.filter(friendgroupuser__user__id=self.request.user.id)
        context['user_friend_groups'] = user_friend_groups.filter(friendgroupuser__user__id=pet.user.id)

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


def user_pets_show(request, friend_id):
        friend = CustomUser.objects.get(id=friend_id)
        pet_list = Pet.objects.filter(user=friend_id)
        context = add_standard_context(request, {'friend': friend, 'pet_list': pet_list})
        return render(request, 'positivepets/user_pets.html', context)