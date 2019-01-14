from django.db import connection
from positivepets.models import FriendGroup, UserState
from positivepets.utils.colors import color_map

def get_active_friendgroup(user_id):
    query_string = \
        "select u.id " + \
        "from positivepets_userstate us, positivepets_friendgroupuser fgu, positivepets_customuser u " + \
        "where u.id = fgu.user_id and us.ref_id = fgu.group_id and us.name = 'ActiveGroup' and us.user_id = " \
        + str(user_id)

    with connection.cursor() as cursor:
        cursor.execute(query_string)
        query_result_list = cursor.fetchall()
    user_list = [x[0] for x in query_result_list]

    return user_list


def add_standard_context(request, context, friend):
    context['color'] = friend.color
    context['button_text_color'] = color_map[friend.color.lower()]['button_text_color']
    user_friend_groups = FriendGroup.objects.filter(friendgroupuser__user__id=request.user.id)
    try:
        selected_friend_group = FriendGroup.objects.get(id=UserState.objects.get(user=request.user).ref_id)
        context['selected_friend_group'] = selected_friend_group
    except:
        context['selected_friend_group'] =[]

    context['user_friend_groups'] = user_friend_groups

    return context
