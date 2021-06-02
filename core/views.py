from django.shortcuts import render
from django.http import HttpResponse
from programs import utils


def home(request):
    context = {'resume': utils.resume_programs()}
    return render(request, "core/home.html", context)

def contact(request):
    return render(request, "core/contact.html")