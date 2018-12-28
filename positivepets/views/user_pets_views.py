from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from positivepets.models import Pet, CustomUser
from django.shortcuts import render
from positivepets.utils.colors import color_map


 #INVISIBLE GENERIC CBV PROCESS

# 1. 'pet_add' is called from "add pet" in the base template
# 2. url conf:  url(r'pet/add/$', views.user_pet_views.PetCreate.as_view(), name='pet_add')
# 3. pet_form is known to be associated with "Pet" because of its name <model>_form
#     there is no Form class defined
# 4. the context variable "form" is automatically set for pet_form
# 5. Inside PetCreate() it says model=Pet
# 6. the action to take when the form is submitted is automatically set as PetCreate.form_valid ????

# get_context_data will be called from PetCreate.as_view()   (i.e. someone comes to the page)
# form_valid will be called when (i.e. someone submits the form)

class PetCreate(CreateView):
    model = Pet
    fields = ['name', 'type', 'breed', 'picture']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(PetCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(PetCreate, self).get_context_data(**kwargs)
        try:
            context['color'] = self.request.user.color
            context['button_text_color'] = color_map[self.request.user.color.lower()]['button_text_color']
        except:
            context['color'] = 'lightgray'
            context['button_text_color'] = 'rgb(40,40,40)'
        return context

class PetUpdate(UpdateView):
    model = Pet
    fields = ['name', 'type', 'breed', 'picture']
    def get_context_data(self, **kwargs):
        context = super(PetUpdate, self).get_context_data(**kwargs)
        try:
            context['color'] = self.request.user.color
            context['button_text_color'] = color_map[self.request.user.color.lower()]['button_text_color']
        except:
            context['color'] = 'lightgray'
            context['button_text_color'] = 'rgb(40,40,40)'
        return context

class PetDelete(DeleteView):
    model=Pet
    def get_success_url(self):
        return reverse_lazy('positivepets:user_pets', kwargs={'friend_id': self.request.user.id})

def user_pets_view(request, friend_id):
        friend = CustomUser.objects.get(id=friend_id)
        pet_list = Pet.objects.filter(user=friend_id)
        button_text_color = color_map[friend.color.lower()]['button_text_color']
        context = {'friend': friend, 'pet_list': pet_list, 'color': friend.color, 'button_text_color': button_text_color}

        return render(request, 'positivepets/user_pets.html', context)