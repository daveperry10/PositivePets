

"""
Generic Class Templates
"""
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic import View

from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
#from django.contrib.auth.models import CustomUser

from .models import Pet, Chat, CustomUser
from .forms import ChatMessageForm,CustomUserCreationForm,CustomUserChangeForm,PetDescriptionForm
from datetime import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse

class IndexView(generic.ListView):
    template_name = 'positivepets/index.html'
    context_object_name = 'user_list'

    def get_queryset(self):
        return CustomUser.objects.all()

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

class DetailView(generic.DetailView):
    model = Pet
    template_name = 'positivepets/detail.html'
    fields = ['description']

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        #this is a pet id
        pet_id = self.kwargs['pk']
        pet = Pet.objects.get(id=pet_id)
        user_id = pet.user.id
        user = CustomUser.objects.get(id=user_id)
        context['owner'] = user
        context['description'] = pet.description
        return context

    # def post(self, request, *args, **kwargs):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        # form = self.form_class(request.POST)
        # if form.is_valid():
        #     pet_id = 3 #self.kwargs['pk']
        #     pet = Pet.object.get(pet_id)
        #
        #     a = form.save(commit=False)
        #     #a.description = form.description
        #     pet.description = a.description

        # return super().form_valid(form)

class PetDescriptionView(generic.DetailView):
    model = Pet
    fields = ['description']
    template_name = 'positivepets/detail.html'
    def post(self, request):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form = self.form_class(request.POST)
        if form.is_valid():
            pet_id = self.kwargs['pk']
            pet = Pet.object.get(pet_id)

            a = form.save(commit=False)
            #a.description = form.description
            pet.description = a.description

        return super().form_valid(form)

class ChatMessageCreate(CreateView):
    model = Chat
    fields = ['comment']

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.

        obj = form.save(commit=False)
        obj.timestamp = datetime.now()
        obj.user = self.request.user
        obj.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ChatMessageCreate, self).get_context_data(**kwargs)

        context['comment_list'] = Chat.objects.all()

        context['user'] = self.request.user
        return context

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


class UserFormView(View):
    form_class = CustomUserCreationForm
    template_name = 'positivepets/registration_form.html'

    #display a blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form':form})
    #process form data

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        #need request.FILES or image upload won't work.

        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username'].lower()
            password = form.cleaned_data['password1'].lower()
            form.picture = request.FILES['picture']
            user.picture = form.picture
            user.set_password(password)
            user.save()

            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('positivepets:index')
        return render(request, self.template_name, {'form':form})


def test_view(request):
    """  Next:  talk about your pet:
    1.  form to post a comment
    2.  Model to store comments about a {pet/picture} by a user.  Fields:  user (fk), pet(fk), comment, datetime
    2.  display box to show all of the comments that have been posted   """

    years_old = 30
    daisies = 2
    array_city_capital = ["Paris", "London", "Washington"]
    user_name = request.user.username
    user_id = 5 # request.user.id
    user = CustomUser.objects.get(id=user_id)
    testy = "<b> dynamic html doesn't work </b>"

    #RENDER ARGUMENTS:  1. REQUEST, 2. TEMPLATE, 3. DICT OF TEMPLATE TAGS FOR ANY VARIABLES (aka the CONTEXT)
    context = {"testy":testy, "user":user, "user_name":user_name, "daisies":daisies, "years":years_old, "array_city":array_city_capital}
    return render(request, 'positivepets/test/test_template.html', context)

def pet_description_view(request, pk):
    if request.method == 'POST':
        form = PetDescriptionForm(request.POST)
        if form.is_valid():

            a = Pet.objects.get(id=pk)
            a.description = form.data['bigtext']
            a.save()
            url = reverse('positivepets:detail', kwargs={'pk': pk})
            return HttpResponseRedirect(url)
    else:
        form = PetDescriptionForm()

    return render(request, 'positivepets/test/test_template.html', {'form': form})


class UserPets(generic.ListView):
    template_name = 'positivepets/user-pets.html'
    context_object_name = 'pet_list'
    model=CustomUser
    #queryset=Pet.objects
    users = CustomUser.objects.all()

    def get_queryset(self):
        #return Pet.objects.filter(user=self.request.user)
        return Pet.objects.filter(user=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(UserPets, self).get_context_data(**kwargs)
        #user_id = int(self.request.POST['id'])
        user = CustomUser.objects.get(id=self.kwargs['pk'])
        context['petowner'] = user
        return context
