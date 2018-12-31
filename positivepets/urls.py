from . import views

from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

# for icon redirect
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView



app_name = 'positivepets'

urlpatterns = [

# PROFILE #
    # /positivepets/
    url(r'^$', views.profile_views.redirect),
    url(r'profile/(?P<friend_id>[0-9]+)/(?P<action>edit_bio|show|edit_picture)/$', views.profile_views.ProfileView.as_view(), name='profile'),

    # /positivepets/5/action/
    url(r'^(?P<friend_id>[0-9]+)/user_picture_save/$', views.profile_views.user_picture_save, name='user_picture_save'),
    url(r'^(?P<friend_id>[0-9]+)/user_picture_edit/$', views.profile_views.user_picture_edit, name='user_picture_edit'),
    url(r'^(?P<friend_id>[0-9]+)/bio_save/$', views.profile_views.bio_save, name='bio_save'),
    url(r'^(?P<friend_id>[0-9]+)/bio_edit/$', views.profile_views.bio_edit, name='bio_edit'),

    # /positivepets/change_active_group/
    url(r'^change_active_group/(?P<redirect>(chat|email|profile|pet_detail))/(?P<pet_id>[0-9]+)/$', views.misc_views.change_active_group, name='change_active_group'),

    # PET DETAIL #
    # /positivepets/71/
    url(r'^(?P<pk>[0-9]+)/(?P<edit>[0-9]+)/$', views.pet_detail_views.PetDetailView.as_view(), name='pet_detail'),

    # /positivepets/5/pet_description_save/
    url(r'^(?P<pk>[0-9]+)/pet_description_save/$', views.pet_detail_views.pet_description_save, name='pet_description_save'),

    # /positivepets/5/pet_description_edit/
    url(r'^(?P<pk>[0-9]+)/pet_description_edit/$', views.pet_detail_views.pet_description_edit, name='pet_description_edit'),

    # /positivepets/5/
    url(r'^pet_comment_message_create/(?P<action>(submit|refresh))/(?P<pet_id>[0-9]+)/$', views.pet_detail_views.pet_comment_message_create, name='pet_comment_message_create'),


# USER PETS #
    # /positivepets/user/5/
    url(r'^user/(?P<friend_id>[0-9]+)/$', views.user_pets_views.user_pets_view, name='user_pets'),

    # /positivepets/pet/...
    url(r'pet/add/$', views.user_pets_views.PetCreate.as_view(), name='pet_add'),
    url(r'pet/(?P<pk>[0-9]+)/$', views.user_pets_views.PetUpdate.as_view(), name='pet_update'),
    url(r'pet/(?P<pk>[0-9]+)/delete/$', views.user_pets_views.PetDelete.as_view(), name='pet_delete'),

# CHAT #
    # /positivepets/chatroom/new/
    url(r'chatroom/(?P<action>(submit|refresh))/$', views.chat_views.chat_message_create, name='chatmessage_create'),

# EMAIL #
    # /positivepets/email/...
    url(r'email/folder/(?P<folder>(inbox|sent_mail|))$', views.email_views.email_folder_show, name='email_folder_show'),
    url(r'email/read/(?P<message_num>[0-9]+)/$', views.email_views.email_read_show, name='email_read_show'),
    url(r'email/compose/(?P<reply_type>(none|reply|reply-all))/(?P<email_id>[0-9]+)/$', views.email_views.email_compose_show, name='email_compose_show'),
    url(r'email/send/$', views.email_views.email_send, name='email_send'),

# USER #
    # /positivepets/register/
    url(r'^register/$', views.misc_views.UserFormView.as_view(), name='register'),
    url(r'^colorchange/$', views.misc_views.color_change_view, name='color_change_view'),
    url(r'^colorsave/$', views.misc_views.color_save_view, name='color_save_view'),

# ABOUT #
    # /positivepets/about/
    url(r'^about/$', views.misc_views.about_view, name='about'),

# ANIMAL SHELTER#
    url(r'^picture_search/$', views.animal_shelter_views.picture_search, name='picture_search'),
    url(r'^do_google_search/$', views.animal_shelter_views.do_google_search, name='do_google_search'),
    url(r'^shelter_adopt/$', views.animal_shelter_views.shelter_adopt, name='shelter_adopt'),

#ICON
    url(r'^pawprint.ico$', RedirectView.as_view(url=staticfiles_storage.url('images/pawprint.ico')), name="pawprint"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)