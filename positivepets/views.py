

"""
Generic Class Templates
"""
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import View

from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from .models import Pet
from .forms import UserForm


class IndexView(generic.ListView):
    template_name = 'positivepets/index.html'
    context_object_name = 'user_list'

    def get_queryset(self):
        return User.objects.all()

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class DetailView(generic.DetailView):
    model = Pet
    template_name = 'positivepets/detail.html'

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
    form_class = UserForm
    template_name = 'positivepets/registration_form.html'

    #display a blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form':form})
    #process form data

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            # cleaned (normalized) data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            #returns user objecgts if credentials are correct
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('positivepets:index')
        return render(request, self.template_name, {'form':form})


def test_view(request):
    years_old = 30
    daisies = 2
    array_city_capital = ["Paris", "London", "Washington"]
    user_name = request.user.username
    user_id = request.user.id

    """
    Talk about your pet:
    1.  form to post a comment
    2.  Model to store comments about a {pet/picture} by a user.  Fields:  user (fk), pet(fk), comment, datetime
    2.  display box to show all of the comments that have been posted
    
    """


    #RENDER ARGUMENTS:  1. REQUEST, 2. TEMPLATE, 3. DICT OF TEMPLATE TAGS FOR ANY VARIABLES (aka the CONTEXT)

    context = {"user_name":user_name, "daisies":daisies, "years":years_old, "array_city":array_city_capital}
    return render(request, 'positivepets/subfolder/test_template.html', context)

class UserList(generic.ListView):
    template_name = 'positivepets/subfolder/user_list.html'
    context_object_name = 'pet_list'
    model=User
    #queryset=Pet.objects

    def get_queryset(self):
        #return Pet.objects.filter(user=self.request.user)
        return Pet.objects.filter(user=self.kwargs['pk'])