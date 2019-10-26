from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    context = {'title': "Home"}
    return render(request, 'product_backlog.html', context)


# Create your views here.
