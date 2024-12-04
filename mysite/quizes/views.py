from django.shortcuts import render
from django.template import loader
from django.http import HttpResponseRedirect




def index(request):
    context = {
        "content": "elo"
    }
    return render(request)
    
# Create your views here.
