from positivepets.models import Pet, Chat, CustomUser, Mail
from datetime import datetime
from django.shortcuts import render
import time
def chat_message_create(request):
    model = Chat
    fields = ['comment']
    if request.method == 'POST':
        msg = Chat()
        msg.timestamp = datetime.now()
        msg.user = request.user
        msg.comment = request.POST['textbox']
        msg.save()
    comment_list = Chat.objects.all().order_by('-timestamp')[:15] #no neg indexing

    now = datetime.now()

    context = {'comment_list': comment_list,'user':request.user, 'now': now}

    return render(request, 'positivepets/chat_form.html', context)
