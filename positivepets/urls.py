from django.contrib import admin
from django.urls import path
from . import views

from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

app_name = 'positivepets'

urlpatterns = [

# INDEX #
    # /positivepets/
    url(r'^$', views.index_views.IndexView.as_view(), name='index'),
    url(r'^change_picture/$', views.index_views.change_picture, name='change_picture'),

# DETAIL #
    # /positivepets/71/
    url(r'^(?P<pk>[0-9]+)/(?P<edit>[0-9]+)/$', views.detail_views.DetailView.as_view(), name='detail'),

    # /positivepets/5/description_save/
    url(r'^(?P<pk>[0-9]+)/description_save/$', views.detail_views.description_save, name='description_save'),

    # /positivepets/5/description_edit/
    url(r'^(?P<pk>[0-9]+)/description_edit/$', views.detail_views.description_edit, name='description_edit'),

# USER PETS #
    # /positivepets/user/5/
    url(r'^user/(?P<pk>[0-9]+)/$', views.user_pet_views.UserPets.as_view(), name='user_pets'),

    # /positivepets/pet/add/
    url(r'pet/add/$', views.user_pet_views.PetCreate.as_view(), name='pet_add'),

    # /positivepets/pet/2/
    url(r'pet/(?P<pk>[0-9]+)/$', views.user_pet_views.PetUpdate.as_view(), name='pet_update'),

    # /positivepets/pet/2/delete/
    url(r'pet/(?P<pk>[0-9]+)/delete/$', views.user_pet_views.PetDelete.as_view(), name='pet_delete'),

# CHAT #
    # /positivepets/chatroom/new/
    url(r'chatroom/new/$', views.chat_views.chat_message_create, name='chatmessage_create'),

# EMAIL #
    # /positivepets/mail/new/
    url(r'mail/new/$', views.email_views.MailCreate.as_view(), name='mail_create'),
    url(r'mail/(?P<message_num>[0-9]+)/$', views.email_views.mail_view, name='mail_view'),

# ADMIN #
    # /positivepets/register/
    url(r'^register/$', views.misc_views.UserFormView.as_view(), name='register'),
    url(r'^modifyuser/$', views.misc_views.UserFormView.as_view(), name='modify_user'),

# ABOUT #
    # /positivepets/about/
    url(r'^about/$', views.misc_views.about_view, name='about'),

#TEST
    # /positivepets/views/
    url(r'^views/$', views.misc_views.test_view, name='test_view'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)