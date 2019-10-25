from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    context = {'title': "Home"}
    return render(request, 'products.html', context)


# Create your views here.
