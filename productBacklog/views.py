from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from .models import ProductBacklog
from .forms import ProductBacklogForm


def product_backlog_view(request,*args,**kwargs):
    form=ProductBacklogForm(request.POST or None)
    if form.is_valid():
            form.save()
            context={}
            # form.ProductBacklogForm()
            return render(request,"products.html",context)
    context={
            "form":form
               }
    

    return render(request,"product_backlog_view.html",context)