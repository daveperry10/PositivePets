from positivepets.models import Chat, FriendGroup, UserState
from datetime import datetime
from django.shortcuts import render
from positivepets.utils.utils import get_users
from positivepets.utils.colors import color_map
from dateutil import tz

def chat_message_create(request, action):

    context = {}

    # ActiveGroup DropDown List:  1.  get all groups 2. get active group
    user_friend_groups = FriendGroup.objects.filter(friendgroupuser__user__id = request.user.id)
    selected_friend_group = FriendGroup.objects.get(id=UserState.objects.get(user = request.user).ref_id)
    context['user_friend_groups'] = user_friend_groups
    context['selected_friend_group'] = selected_friend_group

    if action == 'submit':
        if request.method == 'POST':
            msg = Chat()
            msg.timestamp = datetime.now()
            msg.user = request.user
            msg.comment = request.POST['textbox']
            msg.group = selected_friend_group
            msg.pet_id = 0
            msg.save()

    now = datetime.now()    #to_zone = tz.tzlocal()
    to_zone = tz.gettz("America/New_York")

    user_list = get_users(request.user.id)
    comment_list = Chat.objects.filter(user_id__in=user_list).filter(group=selected_friend_group.id).filter(pet_id=0).order_by('-timestamp')[:30]  # no neg indexing
    context['comment_list'] = comment_list
    context['button_text_color'] = color_map[request.user.color.lower()]['button_text_color']
    for comment in comment_list:
        comment.timestamp = comment.timestamp.astimezone(to_zone)

    context['user'] = request.user
    context['now'] = now
    context['color'] = request.user.color

    return render(request, 'positivepets/chat_form.html', context)