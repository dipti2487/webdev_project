from django.shortcuts import render
from . import views
# Create your views here.

def base(request):
    return render(request, 'proj_app/base.html')

def home(request):
    return render(request, 'proj_app/home.html')
