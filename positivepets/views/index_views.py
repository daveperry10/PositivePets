from django.views import generic
from positivepets.models import CustomUser
from positivepets.forms import CustomUserChangePictureForm
from django.http import HttpResponseRedirect
from django.urls import reverse


class IndexView(generic.ListView):
    template_name = 'positivepets/index.html'
    context_object_name = 'user_list'

    def get_queryset(self):
        return CustomUser.objects.all()

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

def change_picture(request):
    if request.method == 'POST':
        form = CustomUserChangePictureForm(request.POST, request.FILES)
        a = CustomUser.objects.get(id=request.user.id)
        a.picture = request.FILES['picture']
        a.save()
        url = reverse('positivepets:index')
        return HttpResponseRedirect(url)
    else:
        form = CustomUserChangePictureForm()

    return HttpResponseRedirect(reverse('positivepets:index'))
