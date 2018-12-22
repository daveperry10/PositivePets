from django.contrib import admin
from django.urls import path
from . import views

from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

# for icon redirect
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView



app_name = 'positivepets'

urlpatterns = [

# INDEX #
    # /positivepets/
    url(r'^$',views.index_views.redirect, name='index'),
    url(r'profile/(?P<friend_id>[0-9]+)/(?P<action>edit_bio|show|edit_picture)/$', views.index_views.IndexView.as_view(), name='profile'),

    # /positivepets/5/action/
    url(r'^(?P<friend_id>[0-9]+)/user_picture_save/$', views.index_views.user_picture_save, name='user_picture_save'),
    url(r'^(?P<friend_id>[0-9]+)/user_picture_edit/$', views.index_views.user_picture_edit, name='user_picture_edit'),
    url(r'^(?P<friend_id>[0-9]+)/bio_save/$', views.index_views.bio_save, name='bio_save'),
    url(r'^(?P<friend_id>[0-9]+)/bio_edit/$', views.index_views.bio_edit, name='bio_edit'),

# DETAIL #
    # /positivepets/71/
    url(r'^(?P<pk>[0-9]+)/(?P<edit>[0-9]+)/$', views.detail_views.DetailView.as_view(), name='detail'),

    # /positivepets/5/description_save/
    url(r'^(?P<pk>[0-9]+)/description_save/$', views.detail_views.description_save, name='description_save'),

    # /positivepets/5/description_edit/
    url(r'^(?P<pk>[0-9]+)/description_edit/$', views.detail_views.description_edit, name='description_edit'),

# USER PETS #
    # /positivepets/user/5/
    #url(r'^user/(?P<pk>[0-9]+)/$', views.user_pet_views.UserPets.as_view(), name='user_pets'),
    url(r'^user/(?P<friend_id>[0-9]+)/$', views.user_pet_views.user_pet_view, name='user_pets'),

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
    url(r'mail/new/(?P<reply_type>(none|reply|reply-all))/(?P<id>[0-9]+)/$', views.email_views.MailCreate.as_view(), name='mail_create'),
    url(r'mail/(?P<message_num>[0-9]+)/$', views.email_views.mail_view, name='mail_view'),

# ADMIN #
    # /positivepets/register/
    url(r'^register/$', views.misc_views.UserFormView.as_view(), name='register'),
    url(r'^colorchange/$', views.misc_views.color_change_view, name='color_change_view'),
    url(r'^colorsave/$', views.misc_views.color_save_view, name='color_save_view'),

# ABOUT #
    # /positivepets/about/
    url(r'^about/$', views.misc_views.about_view, name='about'),

# SEARCH #
    url(r'^picture_search/$', views.misc_views.picture_search, name='picture_search'),
    url(r'^do_search/$', views.misc_views.do_search, name='do_search'),

    #TEST
    # /positivepets/test/
    url(r'^test/$', views.misc_views.test_view, name='test_view'),

#ICON
    url(r'^pawprint.ico$', RedirectView.as_view(url=staticfiles_storage.url('images/pawprint.ico')), name="pawprint"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)