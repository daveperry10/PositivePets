"""
The email module has four functions:
    - email_folder_show(request, folder):  show either the inbox or sent mail
    - email_read_show(request, email_id):  show the email in its own page and mark it read
    - email_compose_show(request, reply_type, email_id): display a blank email in a pop-out window.
        - if reply or reply-all, fill in recipients and previous msg/subj
    - email_send(request): save the new rows down to the DB and close the window

Notes:
    This doesn't actually send email.  It's just a closed-system toy email built on a single DB table.
    The table positivepets_mail stores one line for each email, and repeats the whole record for each recipient.
    msg_id is a common identifier in each of these repeated rows - it is used to collect recipients for 'reply_all'
        - this will be inefficient when the DB is larger - plan is to restructure to avoid this repetition.
    each row contains a status that changes from 'unread' (1) to read (2) when it is viewed by the recipient
    The model name remains "Mail" and not "Email" because of MySQL migration issues
    This module uses Function Based Views - arbitrary choice just to learn FBV
"""

from datetime import datetime
from django.db.models import Max
from django.shortcuts import render
from positivepets.models import Mail, CustomUser
from positivepets.forms import EmailForm
from positivepets.utils.utils import get_active_friendgroup, add_standard_context

EMAIL_STATUS_UNREAD = 1
EMAIL_STATUS_READ = 2

def email_send(request):
    mx = Mail.objects.all().aggregate(Max('msg_id'))
    msg_id = mx['msg_id__max'] + 1
    recipient_list = request.POST.getlist('recipients')
    form = EmailForm(request.POST)
    form.fields['recipients'].queryset = CustomUser.objects.filter(id__in=get_active_friendgroup(request.user.id)).exclude(id=request.user.id).exclude(username='admin')

    if form.is_valid():
        for r in recipient_list:
            m = Mail()
            m.msg_id = msg_id
            m.timestamp = datetime.now()
            m.sender = request.user
            m.status = EMAIL_STATUS_UNREAD
            m.subject = request.POST['subject']
            m.message = request.POST['message']
            m.recipient = CustomUser.objects.get(id=int(r))
            m.save()
        return render(request, 'positivepets/close_me.html')

    context = add_standard_context(request, {})
    context['subject'] = request.POST['subject']
    context['message'] = request.POST['message']
    context['recipient_list'] = recipient_list
    context['form'] = form

    return render(request, 'positivepets/email_folder.html', context)


def email_read_show(request, email_id):
    """
    Show the email on its own page.
    Change the status in the DB to "read"
    Make the recipients into a comma-separated list for display
    """

    email = Mail.objects.get(id=email_id)
    email.status = EMAIL_STATUS_READ
    email.save()

    recipient_list = list(Mail.objects.filter(msg_id=email.msg_id))
    my_list = [o.recipient.username.title() for o in recipient_list]
    recipient_string = ", ".join(my_list)
    context = {'email': email, 'recipients': recipient_string}

    return render(request, 'positivepets/email_read.html', context)

def email_compose_show(request, reply_type, email_id):

    context = add_standard_context(request, {})
    active_friendgroup_members = CustomUser.objects.filter(id__in=get_active_friendgroup(request.user.id)).exclude(id=request.user.id)
    context['user_list'] = active_friendgroup_members


    if reply_type == 'none':
        form = EmailForm()
        form.fields['recipients'].queryset = active_friendgroup_members

    elif reply_type == 'reply':
        msg = Mail.objects.get(id=email_id)
        form = EmailForm(initial={'message': "\n\n <<<<< previous message: >>>>> \n " + msg.message, 'subject': msg.subject})
        context['recipient_list'] = [msg.sender]

    else: #reply_type == 'reply_all'
        msg = Mail.objects.get(id=email_id)
        form = EmailForm(initial={'message': "\n\n <<<<< previous message: >>>>> \n " + msg.message, 'subject': msg.subject})
        mail_objects = Mail.objects.filter(msg_id=msg.msg_id)
        recipient_list = [msg.sender]

        for m in mail_objects:
            recipient_list.append(m.recipient)

        context['recipient_list'] = recipient_list

    context['form'] = form
    return render(request, 'positivepets/email_compose.html', context)



def email_folder_show(request, folder):
    """
    Build recipient list out of multiple email records with common msg_id
    Build context lists for inbox and sent_mail
    """

    context = add_standard_context(request, {'folder': folder})

    if folder == 'sent_mail':
        temp_sent_list = Mail.objects.filter(sender_id=request.user.id).filter(recipient__in=get_active_friendgroup(request.user.id)).order_by('-timestamp')
        sent_mail = []
        # fail nicely if there are no sent emails (new user)
        try:
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
        except:
            pass

    else:
        context['inbox'] = Mail.objects.filter(recipient_id=request.user).filter(sender__in=get_active_friendgroup(request.user.id)).order_by('-timestamp')

    return render(request, 'positivepets/email_folder.html', context)