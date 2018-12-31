import csv, json, io, os, requests
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
from bs4 import BeautifulSoup
from collections import defaultdict
from PIL import Image
import urllib.request
from positivepets.models import Pet
import uuid
from django.conf import settings
from django.templatetags.static import static

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


def get_json_info():
    static_root = getattr(settings, "STATIC_ROOT", "")
    path = os.path.join(static_root, 'breeds.csv')
    csv_file = open(path, 'r')
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

def shelter_adopt(request):

    if request.method == 'POST':
        # create a pet, assign values to it, and save it
        pet = Pet()
        pet.name = request.POST['adopted_pet_name']
        pet.type = request.POST['selected_animal']
        pet.breed = request.POST['selected_breed']
        pet.user = request.user
        url = request.POST['url']

        if url != "":
            path = io.BytesIO(urllib.request.urlopen(url).read())
            img = Image.open(path)
            pet.picture.name = pet.name + str(uuid.uuid4()) + '.jpg'
            img.save(os.path.join(settings.MEDIA_ROOT, pet.picture.name))
            #img.save(os.path.join(settings.STATIC_ROOT, pet.picture.name), path)
            pet.save()
            return HttpResponseRedirect(reverse('positivepets:user_pets', kwargs={'friend_id': request.user.id}))
    #user.picture.save('star_icon.jpg', File(open(os.path.join(settings.STATIC_ROOT, 'star_icon.jpg'), 'rb')))


            img = Image.open(self.picture)
            img.thumbnail((400, 400))
            file = os.path.join(settings.MEDIA_ROOT, self.picture.name)
            img.save(file, quality=60)



    # redirect to user_pets with the new pet added
    return render(request, reverse('positivepets:shelter_adopt'))