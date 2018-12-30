from positivepets.models import Mail, CustomUser, FriendGroup, UserState
from django.views.generic.edit import CreateView
from datetime import datetime
from django.db.models import Max, Min
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from positivepets.utils.colors import color_map
from positivepets.utils.utils import get_users
from django.contrib import messages
from positivepets.forms import EmailForm

EMAIL_STATUS_UNREAD = 1
EMAIL_STATUS_READ = 2

def email_send(request):
    mx = Mail.objects.all().aggregate(Max('msg_id'))
    msg_id = mx['msg_id__max'] + 1
    recipient_list = request.POST.getlist('recipients')
    form = EmailForm
    for r in recipient_list:
        m = Mail()
        m.msg_id = msg_id
        m.timestamp = datetime.now()
        m.sender = request.user
        m.status = EMAIL_STATUS_UNREAD
        m.subject = request.POST['subject']
        m.message = request.POST['message']
        m.recipient = CustomUser.objects.get(username=r.lower())
        m.save()

    #return Http ResponseRedirect(reverse('positivepets:close', kwargs={'folder':'inbox'}))
    return render(request, 'positivepets/close_me.html')

def email_read_show(request, message_num):
    message_list = Mail.objects.filter(recipient=request.user.id).order_by('-timestamp')
    #email = message_list[int(message_num)]
    email = Mail.objects.get(id=message_num)
    email.status = EMAIL_STATUS_READ
    email.save()

    # take django query_set and turn it into a comma-delimited list of usernames
    recipient_list = list(Mail.objects.filter(msg_id=email.msg_id))
    my_list  = [o.recipient.username.title() for o in recipient_list]
    recipient_string = ", ".join(my_list)
    context = {'email': email, 'recipients': recipient_string}

    return render(request, 'positivepets/email_read.html', context)

def email_compose_show(request, reply_type, email_id):
    recipient_list = []
    context = {}
    if reply_type == 'reply-all':
        msg = Mail.objects.get(id=email_id)

        for item in Mail.objects.filter(msg_id=msg.msg_id):  #msg_id is a common id for all messages generated in a reply-all
            recipient_list.append(item.recipient.id)

        recipient_list.append(msg.sender.id)
        context['subject'] = msg.subject
        context['message'] = "\n\n <<<<< previous message: >>>>> \n " + msg.message

    elif reply_type == 'reply':
        id = email_id
        msg = Mail.objects.get(id=id)
        recipient_list.append(msg.sender.id)
        context['subject'] = msg.subject
        if msg.message is None:
            context['message'] = "\n\n <<<<< previous message: >>>>> \n "
        else:
            context['message'] = "\n\n <<<<< previous message: >>>>> \n " + msg.message
    else:
        context['subject'] = ''
        context['message'] = ''

    context['recipient_list'] = recipient_list
    context['color'] = request.user.color
    context['button_text_color'] = color_map[request.user.color.lower()]['button_text_color']

    # ActiveGroup DropDown List:  1.  get all groups 2. get active group
    user_friend_groups = FriendGroup.objects.filter(friendgroupuser__user__id=request.user.id)
    selected_friend_group = FriendGroup.objects.get(id=UserState.objects.get(user=request.user).ref_id)
    context['user_friend_groups'] = user_friend_groups
    context['selected_friend_group'] = selected_friend_group
    context['sender'] = request.user
    context['user_list'] = CustomUser.objects.filter(id__in=get_users(request.user.id)).exclude(id=request.user.id).exclude(
        username='admin')

    return render(request, 'positivepets/email_compose.html', context)

def email_folder_show(request, folder):
    context = {'folder':folder}

    context['inbox'] = Mail.objects.filter(recipient_id=request.user).filter(sender__in=get_users(request.user.id)).order_by('-timestamp')

    context['color'] = request.user.color
    context['button_text_color'] = color_map[request.user.color.lower()]['button_text_color']

    # ActiveGroup DropDown List:  1.  get all groups 2. get active group
    user_friend_groups = FriendGroup.objects.filter(friendgroupuser__user__id=request.user.id)
    selected_friend_group = FriendGroup.objects.get(id=UserState.objects.get(user=request.user).ref_id)
    context['user_friend_groups'] = user_friend_groups
    context['selected_friend_group'] = selected_friend_group

    # strategy: multi-recipient messages are stored as separate rows (emails) for each recipient, which share a common msg_id.
    # Need to reduce to one row for display.

    # result is a list of email objects
    temp_sent_list = Mail.objects.filter(sender_id=request.user.id).filter(recipient__in=get_users(request.user.id)).order_by('-timestamp')
    sent_mail = []
    this_message = temp_sent_list[0]
    this_message.recipient.username = ""
    counter = 0
    for email in temp_sent_list:
        if email.msg_id == this_message.msg_id:
            if counter == 0:
                this_message.recipient.username = email.recipient.username.title()
                counter = counter + 1
            else:
                this_message.recipient.username = ", ".join([this_message.recipient.username, email.recipient.username.title()])
                counter = counter + 1
        else:
            sent_mail.append(this_message)
            this_message = email
            counter = counter + 1

    sent_mail.append(this_message)

    context['sent_mail'] = sent_mail

    return render(request, 'positivepets/email_folder.html', context)