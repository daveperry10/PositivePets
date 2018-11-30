from positivepets.models import Mail, CustomUser
from django.views.generic.edit import CreateView
from datetime import datetime
from django.db.models import Max
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render

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

        return HttpResponseRedirect(reverse('positivepets:mail_create'))

    def get_context_data(self, **kwargs):
        context = super(MailCreate, self).get_context_data(**kwargs)
        context['inbox'] = Mail.objects.filter(recipient=self.request.user).order_by('-timestamp')
        context['sent_mail'] = Mail.objects.filter(sender=self.request.user).order_by('-timestamp')
        context['sender'] = self.request.user
        context['user_list'] = CustomUser.objects.exclude(id=self.request.user.id).exclude(username='admin')
        return context

def mail_view(request, message_num):
    """
      Strategy:
      you either got a reply or a reply all variable in POST
      pull the whole inbox, sort descending
      get the one at message_num.  find it's id.
      send user back to url:'mail_create' with id as argument.
      mail id will prepopulate subj and msg
      ** need to pre-select the recipients using the msg_id associated with id
      if 'reply' just prepopulate the sender
      if 'reply all' prepopulate the sender and other recipients

      Necessary changes:
      1.  MailCreate has to take an argument for the id of the message to prepopulate the form with, if any
      2.  Table needs links in each row, with an id for each one to use as the argument
      ** template within a link
      3.
      """

    message_list = Mail.objects.filter(recipient=request.user.id).order_by('-timestamp')
    mail = message_list[int(message_num)]
    mail.status = EMAIL_STATUS_READ
    mail.save()
    context = {'mail': mail}

    return render(request, 'positivepets/mail_message_form.html', context)