from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from positivepets.models import Pet, CustomUser
from django.http import HttpResponseRedirect
from django.urls import reverse

class PetCreate(CreateView):
    model = Pet
    fields = ['name', 'type', 'breed', 'picture']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(PetCreate, self).form_valid(form)

class PetUpdate(UpdateView):
    model = Pet
    fields = ['name', 'type', 'breed', 'picture']

class PetDelete(DeleteView):
     model=Pet
     success_url = reverse_lazy('positivepets:index')

class UserPets(generic.ListView):
    template_name = 'positivepets/user-pets.html'
    context_object_name = 'pet_list'
    model=CustomUser

    users = CustomUser.objects.all()

    def get_queryset(self):
        return Pet.objects.filter(user=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(UserPets, self).get_context_data(**kwargs)
        user = CustomUser.objects.get(id=self.kwargs['pk'])
        context['petowner'] = user
        return context

        url = reverse('positivepets:detail')
        return HttpResponseRedirect(url)