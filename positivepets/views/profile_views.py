from datetime import datetime, timedelta
from django.views import generic
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Count
from django.shortcuts import render
from positivepets.models import CustomUser, Pet, Chat, Mail, FriendGroupUser
from positivepets.forms import CustomUserChangePictureForm, BioForm
from positivepets.utils import get_active_friendgroup, add_standard_context, color_map

class ProfileView(generic.ListView):
    template_name = 'positivepets/profile.html'
    fields = ['bio']

    def get_queryset(self):
        return CustomUser.objects.all()

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)

        if (int(self.kwargs['friend_id'])==0) or self.request.user.is_anonymous:
            context['color'] = 'lightgray'  # set to avoid error when color is referenced later
        else:
            friend = CustomUser.objects.get(id=self.kwargs['friend_id'])
            context = add_standard_context(self.request, context)
            context['friend'] = friend
            context['action'] = self.kwargs['action']
            context['pet_list'] = Pet.objects.filter(user=friend.id)
            context['user_list'] = CustomUser.objects.filter(id__in=get_active_friendgroup(self.request.user.id))

            # Build up list of recent activity to display on profile page
            activity_list = []
            as_of_date = datetime.now() - timedelta(hours=48)
            pet_comment_list = Chat.objects.filter(timestamp__gte=as_of_date).filter(pet_id__gt=1).filter(pet__user=self.request.user).values('pet__name', 'user__username', 'group__name').annotate(pet_msg_count=Count('id'))
            email_list = Mail.objects.filter(timestamp__gte=as_of_date).filter(recipient=self.request.user).values('sender__username').annotate(email_count=Count('id'))
            group_ids = FriendGroupUser.objects.filter(user_id=self.request.user.id).values('group_id')
            chat_list = Chat.objects.filter(pet_id=1).filter(timestamp__gte=as_of_date).filter(group_id__in=group_ids).values('user__username', 'group__name').annotate(chat_count=Count('id'))

            for row in pet_comment_list:
                activity_list.append(row["pet__name"].title() + " has " + str(row["pet_msg_count"]) + " new comment" + ("s" if row["pet_msg_count"]>1 else "") + \
                                     " from " + row["user__username"].title()  + " in " + row["group__name"])

            for row in email_list:
                activity_list.append(row["sender__username"].title() + " sent you " + str(row["email_count"]) + " email" + ("s" if row["email_count"]>1 else ""))

            for row in chat_list:
                activity_list.append(row["user__username"].title() + " posted " + str(row["chat_count"]) + " chat message" + \
                                     ("s" if row["chat_count"]>1 else "") + " in " + row["group__name"])

            context['activity_list'] = activity_list
        return context

def redirect(request):
    """
    Called if someone goes to the base url (first time users, visitors, people who bookmarked it)
    Sets friend_id based on authentication status for branching in the profile view
    """

    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('positivepets:profile', kwargs={'friend_id':request.user.id, 'action':'show'}))
    else:
        return HttpResponseRedirect(reverse('positivepets:profile', kwargs={'friend_id':0, 'action': 'show'}))

def bio_edit(request):
    if request.method == 'POST':
        url = reverse('positivepets:profile', kwargs={'friend_id': request.user.id, 'action': 'edit_bio'})
        return HttpResponseRedirect(url)

def user_picture_edit(request):
    if request.method == 'POST':
        url = reverse('positivepets:profile', kwargs={'friend_id': request.user.id, 'action': 'edit_picture'})
        return HttpResponseRedirect(url)

def bio_save(request):
    if request.method == 'POST':
        form = BioForm(request.POST)
        #if form.is_valid():
        a = CustomUser.objects.get(id=request.user.id)
        a.bio = form.data['bigtext']
        a.save()
        url = reverse('positivepets:profile', kwargs={'friend_id': request.user.id, 'action': 'show'})
        return HttpResponseRedirect(url)
    return HttpResponseRedirect(reverse('positivepets:profile', kwargs={'friend_id': request.user.id, 'action': 'show'}))

def user_picture_save(request):
    if request.method == 'POST':
        form = CustomUserChangePictureForm(request.POST, request.FILES)
        user = CustomUser.objects.get(id=request.user.id)
        try:
            user.picture = request.FILES['picture']
            user.save()
            url = reverse('positivepets:profile', kwargs={'friend_id': request.user.id, 'action': 'show'})
            return HttpResponseRedirect(url)
        except:
            url = reverse('positivepets:profile', kwargs={'friend_id': request.user.id, 'action': 'edit_picture'})
            return HttpResponseRedirect(url)

    return HttpResponseRedirect(reverse('positivepets:profile', kwargs={'friend_id': request.user.id, 'action': 'show'}))

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
