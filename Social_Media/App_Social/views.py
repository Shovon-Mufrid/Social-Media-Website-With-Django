from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def home(request):
    return render(request, 'App_Social/home.html', context={'title':'Home'})