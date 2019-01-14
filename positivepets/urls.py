"""
    URL categories are referenced here roughly in the order they appear in the Nav Bar
"""

from . import views

from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

# for icon redirect
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView

app_name = 'positivepets'

urlpatterns = [

    # USER #
    url(r'^$', views.profile_views.redirect),
    url(r'^profile/(?P<friend_id>[0-9]+)/(?P<action>edit_bio|show|edit_picture)/$', views.profile_views.ProfileView.as_view(), name='profile'),
    url(r'^profile/user_picture_save/$', views.profile_views.user_picture_save, name='user_picture_save'),
    url(r'^profile/user_picture_edit/$', views.profile_views.user_picture_edit, name='user_picture_edit'),
    url(r'^profile/bio_save/$', views.profile_views.bio_save, name='bio_save'),
    url(r'^profile/bio_edit/$', views.profile_views.bio_edit, name='bio_edit'),
    url(r'^profile/color_change/$', views.profile_views.color_change_view, name='color_change_view'),
    url(r'^profile/color_save/$', views.profile_views.color_save_view, name='color_save_view'),
    url(r'^profile/change_active_group/(?P<redirect>(chat|email|profile|pet_detail))/(?P<pet_id>[0-9]+)/$', views.misc_views.change_active_group, name='change_active_group'),

    # USER PETS #
    url(r'^user_pet/(?P<friend_id>[0-9]+)/$', views.pet_views.user_pets_show, name='user_pets_show'),
    url(r'^user_pet/add/$', views.pet_views.PetCreate.as_view(), name='pet_add'),
    url(r'^user_pet/update/(?P<pk>[0-9]+)/$', views.pet_views.PetUpdate.as_view(), name='pet_update'),
    url(r'^user_pet/delete/(?P<pk>[0-9]+)/delete/$', views.pet_views.PetDelete.as_view(), name='pet_delete'),

    # PET DETAIL #
    url(r'^pet_detail/(?P<pk>[0-9]+)/(?P<action>(edit|show))/$', views.pet_views.PetDetailView.as_view(), name='pet_detail'),
    url(r'^pet_detail/pet_description_save/(?P<pet_id>[0-9]+)/$', views.pet_views.pet_description_save, name='pet_description_save'),
    url(r'^pet_detail/pet_description_edit/(?P<pet_id>[0-9]+)/$', views.pet_views.pet_description_edit, name='pet_description_edit'),
    url(r'^pet_detail/pet_comment_message_create/(?P<action>(submit|refresh))/(?P<pet_id>[0-9]+)/$',
        views.pet_views.pet_comment_message_create, name='pet_comment_message_create'),

    # CHAT #
    # /positivepets/chatroom/new/
    url(r'chatroom/(?P<action>(submit|refresh))/$', views.chat_views.chat_message_create, name='chatmessage_create'),

    # EMAIL #
    # /positivepets/email/
    url(r'email/folder/(?P<folder>(inbox|sent_mail|))$', views.email_views.email_folder_show, name='email_folder_show'),
    url(r'email/read/(?P<email_id>[0-9]+)/$', views.email_views.email_read_show, name='email_read_show'),
    url(r'email/compose/(?P<reply_type>(none|reply|reply-all))/(?P<email_id>[0-9]+)/$', views.email_views.email_compose_show, name='email_compose_show'),
    url(r'email/send/$', views.email_views.email_send, name='email_send'),

    # ANIMAL SHELTER#
    url(r'^animal_shelter/$', views.animal_shelter_views.animal_shelter_show, name='animal_shelter_show'),
    url(r'^animal_shelter/google_search/$', views.animal_shelter_views.animal_shelter_google_search, name='animal_shelter_google_search'),
    url(r'^animal_shelter/adopt/$', views.animal_shelter_views.animal_shelter_adopt, name='animal_shelter_adopt'),

    # ABOUT #
    # /positivepets/about/
    url(r'^about/$', views.misc_views.about_view, name='about'),

    # ADMIN #
    url(r'^register/$', views.misc_views.UserFormView.as_view(), name='register'),
    url(r'^group/$', views.misc_views.group_admin_show, name='group_admin_show'),
    url(r'^group/add/$', views.misc_views.group_add_view, name='group_add_view'),

    #ICON
    url(r'^pawprint.ico$', RedirectView.as_view(url=staticfiles_storage.url('images/pawprint.ico')), name="pawprint"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)