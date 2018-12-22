from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from positivepets.models import CustomUser
from positivepets.forms import CustomUserCreationForm,CustomUserChangePictureForm, PictureSearchForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.files import File
from django.conf import settings
from bs4 import BeautifulSoup
import requests
import os
import csv
import json
from collections import defaultdict

from positivepets.views.colors import color_map

class UserFormView(View):
    form_class = CustomUserCreationForm
    template_name = 'positivepets/registration_form.html'

    #display a blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form':form, 'color': request.user.color})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        #need request.FILES or image upload won't work.

        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data['username'].lower()
            password = form.cleaned_data['password1'].lower()
            try:
                user.picture = request.FILES['picture']
            except:
                #if they don't put a picture, give them the star icon.
                try:
                    user.picture.save('star_icon.jpg', File(open(os.path.join(settings.STATIC_ROOT, 'star_icon.jpg'),'rb')))
                except:
                    pass
            user.set_password(password)
            user.invitedby = request.user
            user.save()

            user = authenticate(username=user.username, password=password)
            if user is not None:
                if user.is_active:
                    #login(request, user)
                    return redirect('positivepets:index')

        return render(request, self.template_name, {'form':form, 'color': request.user.color})


def color_change_view(request):
    try:
        display_name = color_map[request.user.color.lower()]['display_name']
    except:
        display_name = 'Light Gray'

    context = {'color_map': color_map, 'color': request.user.color, 'color_name':display_name}
    return render(request, 'positivepets/color_change_form.html', context)

def color_save_view(request):

    if request.POST:
        user = request.user
        color_display_name = request.POST['color']


        for k, v in color_map.items():
            if v['display_name'] == color_display_name:
                user.color = k

        user.save()

        return HttpResponseRedirect(reverse('positivepets:profile', kwargs={'friend_id':request.user.id, 'action': 'show'}))

    return HttpResponseRedirect(reverse('positivepets:profile', kwargs={'friend_id': request.user.id, 'action': 'show'}))


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
    return render(request, 'positivepets/test/test_template.html', context)

def about_view(request):
    return render(request, 'positivepets/about.html')

def get_json_info():
    csv_file = open('static/breeds.csv', 'r')
    reader = csv.DictReader(csv_file)
    animal_names = reader.fieldnames
    breed_dict = defaultdict(list)

    for row in reader:
        for j in range(0,len(row)):
            if row[animal_names[j]] != "":
                breed_dict[animal_names[j]].append(row[animal_names[j]])

    json_breeds = json.dumps(breed_dict)
    json_animals = json.dumps(animal_names)
    return json_breeds, json_animals

def picture_search(request):
    json_breeds, json_animals = get_json_info()
    context = {'json_animals': json_animals, 'json_breeds':json_breeds, 'color':request.user.color}
    print(json_animals)
    return render(request, 'positivepets/animal_shelter.html',context)

def do_search(request):
    if request.POST:
        animal_type = request.POST['animal_type']
        breed = request.POST['breed']
        baby_or_fullgrown = request.POST['baby_or_fullgrown']
        key_word_string = animal_type+'+' + breed + "+" + baby_or_fullgrown

        user_search_words = request.POST['search_words']
        user_search_words = '+'.join(user_search_words.split())
        key_word_string = key_word_string + "+" + user_search_words

        search_url = "https://www.google.com/search?tbm=isch&q=" + key_word_string + "&safe=active"
        source = requests.get(search_url).text
        soup = BeautifulSoup(source, 'lxml')
        img_list = []
        for img in soup.find_all('img'):
            img_list.append(img['src'])

    json_breeds, json_animals = get_json_info()

    context = {'json_animals': json_animals, 'json_breeds': json_breeds, "image_list":img_list, 'color':request.user.color}
    return render(request, 'positivepets/animal_shelter.html', context)