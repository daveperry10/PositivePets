from positivepets.models import Mail, CustomUser
from django.views.generic.edit import CreateView
from datetime import datetime
from django.db.models import Max
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from .colors import color_map

EMAIL_STATUS_UNREAD = 1
EMAIL_STATUS_READ = 2

class MailCreate(CreateView):
    model = Mail
    fields = ['message', 'subject']

    def form_valid(self, form):
        mx = Mail.objects.all().aggregate(Max('msg_id'))
        msg_id = mx['msg_id__max'] + 1
        recipient_list = self.request.POST.getlist('recipients')

        for r in recipient_list:
            m = Mail()
            m.msg_id = msg_id
            m.timestamp = datetime.now()
            m.sender = self.request.user
            m.status = EMAIL_STATUS_UNREAD
            m.subject = form.cleaned_data['subject']
            m.message = form.cleaned_data['message']
            m.recipient = CustomUser.objects.get(username=r.lower())
            m.save()

        return HttpResponseRedirect(reverse('positivepets:mail_create', kwargs=self.kwargs))

    def get_context_data(self, **kwargs):
        """
        messages are repeated in the table if there are multiple recipients.
        id is the auto-incremented primary key of the Mail table.
        msg_id is the common identifier for several rows if multiple recipients.
        """
        context = super(MailCreate, self).get_context_data(**kwargs)
        context['inbox'] = Mail.objects.filter(recipient=self.request.user).order_by('-timestamp')
        context['sent_mail'] = Mail.objects.filter(sender=self.request.user).order_by('-timestamp')
        context['sender'] = self.request.user
        context['user_list'] = CustomUser.objects.exclude(id=self.request.user.id).exclude(username='admin')
        context['color'] = self.request.user.color
        context['button_text_color'] = color_map[self.request.user.color.lower()]['button_text_color']
        recipient_list = []

        if self.kwargs['reply_type'] == 'reply-all':
            id = self.kwargs['id']
            msg = Mail.objects.get(id=id)

            for item in Mail.objects.filter(msg_id=msg.msg_id):
                recipient_list.append(item.recipient.id)

            recipient_list.append(msg.sender.id)
            context['subject'] = msg.subject
            context['message'] = "\n\n ------------------- \n " + msg.message

        elif self.kwargs['reply_type'] == 'reply':
            id = self.kwargs['id']
            msg = Mail.objects.get(id=id)
            recipient_list.append(msg.sender.id)
            context['subject'] = msg.subject
            context['message'] = "\n\n ------------------- \n " + msg.message

        else:
            context['subject'] = ''
            context['message'] = ''

        context['recipient_list'] = recipient_list

        return context


def mail_view(request, message_num):

    message_list = Mail.objects.filter(recipient=request.user.id).order_by('-timestamp')
    mail = message_list[int(message_num)]
    mail.status = EMAIL_STATUS_READ
    mail.save()

    # take django query_set and turn it into a comma-delimited list of usernames
    recipient_list = list(Mail.objects.filter(msg_id=mail.msg_id))
    my_list  = [o.recipient.username.title() for o in recipient_list]
    recipient_string = ", ".join(my_list)


    context = {'mail': mail, 'recipients': recipient_string}

    return render(request, 'positivepets/mail_message_form.html', context)