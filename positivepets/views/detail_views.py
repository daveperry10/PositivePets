from django.views import generic
from positivepets.models import Pet, CustomUser
from positivepets.forms import PetDescriptionForm
from django.http import HttpResponseRedirect
from django.urls import reverse

class DetailView(generic.DetailView):
    model = Pet
    template_name = 'positivepets/detail.html'
    fields = ['description']

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        pet_id = self.kwargs['pk']
        edit = self.kwargs['edit']
        pet = Pet.objects.get(id=pet_id)
        owner = CustomUser.objects.get(id=pet.user.id)
        description = pet.description
        context['owner'] = owner
        context['description'] = description
        context['edit'] = edit
        context['color'] = self.request.user.color  #only the user can see the buttons
        return context

def description_edit(request, pk):
    if request.method == 'POST':
        url = reverse('positivepets:detail', kwargs={'pk': pk, 'edit': 1})
        return HttpResponseRedirect(url)


def description_save(request, pk):
    if request.method == 'POST':
        form = PetDescriptionForm(request.POST)
        if form.is_valid():
            a = Pet.objects.get(id=pk)
            a.description = form.data['bigtext']
            a.save()
            url = reverse('positivepets:detail', kwargs={'pk': pk, 'edit': 0})
            return HttpResponseRedirect(url)
    else:
        form = PetDescriptionForm()

    return HttpResponseRedirect(reverse('positivepets:detail', kwargs={'pk': pk, 'edit': 0}))