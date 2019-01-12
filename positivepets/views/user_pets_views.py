"""
The Pet model is managed through Generic Class Based Views with very little modification.

    Classes:
    - PetCreate(CreateView):
    - PetUpdate(UpdateView):
    - PetDelete(DeleteView):

    Functions:
    - user_pets_show(request, friend_id):

"""


from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from positivepets.models import Pet, CustomUser
from django.shortcuts import render
from positivepets.utils import color_map, add_standard_context

class PetCreate(CreateView):
    model = Pet
    fields = ['name', 'type', 'breed', 'picture']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(PetCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(PetCreate, self).get_context_data(**kwargs)
        return add_standard_context(self.request, context)

class PetUpdate(UpdateView):
    model = Pet
    fields = ['name', 'type', 'breed', 'picture']

    def get_context_data(self, **kwargs):
        context = super(PetUpdate, self).get_context_data(**kwargs)
        return add_standard_context(self.request, context)

class PetDelete(DeleteView):
    model=Pet
    def get_success_url(self):
        return reverse_lazy('positivepets:user_pets_show', kwargs={'friend_id': self.request.user.id})


def user_pets_show(request, friend_id):
        friend = CustomUser.objects.get(id=friend_id)
        pet_list = Pet.objects.filter(user=friend_id)
        context = add_standard_context(request, {'friend': friend, 'pet_list': pet_list})
        return render(request, 'positivepets/user_pets.html', context)