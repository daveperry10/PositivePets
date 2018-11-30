from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from positivepets.models import CustomUser
from positivepets.forms import CustomUserCreationForm,CustomUserChangePictureForm
from django.http import HttpResponseRedirect
from django.urls import reverse

class UserFormView(View):
    form_class = CustomUserCreationForm
    template_name = 'positivepets/registration_form.html'

    #display a blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form':form})

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

    if request.method == 'POST':
        form = CustomUserChangePictureForm(request.POST, request.FILES)
        a = CustomUser.objects.get(id=request.user.id)
        a.picture = request.FILES['picture']
        a.save()
        url = reverse('positivepets:index')
        return HttpResponseRedirect(url)

    context = {"testy":testy, "user":user, "user_name":user_name, "daisies":daisies, "years":years_old, "array_city":array_city_capital}
    return render(request, 'positivepets/views/test_template.html', context)

def about_view(request):
    return render(request, 'positivepets/about.html')
