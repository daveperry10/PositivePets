from django.contrib import admin
from django.urls import path
from . import views

from django.conf.urls import url, include   #older
from django.conf import settings
from django.conf.urls.static import static

app_name = 'positivepets'

urlpatterns = [
    #ARGUMENTS:  1. BROWSER INPUT 2. FUNCTION NAME 3. TAG IN THE TEMPLATES

    # /positivepets/
    url(r'^$', views.IndexView.as_view(), name='index'),

    # /positivepets/register/
    url(r'^register/$', views.UserFormView.as_view(), name='register'),

    # /positivepets/test/
    url(r'^test/$', views.test_view, name='test_view'),

    # /positivepets/user/5/
    url(r'^user/(?P<pk>[0-9]+)/$', views.UserList.as_view(), name='user-list'),

    # /positivepets/71/    -- don't forget the comma on the end of the line
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),

    # /positivepets/pet/add/
    url(r'pet/add/$', views.PetCreate.as_view(), name='pet-add'),

    # /positivepets/pet/2/
    url(r'pet/(?P<pk>[0-9]+)/$', views.PetUpdate.as_view(), name='pet-update'),

    # /positivepets/pet/2/delete/
    url(r'pet/(?P<pk>[0-9]+)/delete/$', views.PetDelete.as_view(), name='pet-delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
