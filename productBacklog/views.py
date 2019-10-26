from django.shortcuts import render, redirect
from django.views.generic.edit import UpdateView, CreateView
from django.http import HttpResponse

from .models import ProductBacklog
from .forms import ProductBacklogForm
import logging

logger = logging.getLogger(__name__)

def index(request):
    return redirect('product_backlog/')


def ProductBacklogView(request):
    pbis = ProductBacklog.objects.all()
    context = {'title': "Product Backlog", 'pbis': pbis}
    return render(request, 'product_backlog.html', context)


def AddPBI(request, *args, **kwargs):
    form = ProductBacklogForm(request.POST or None)
    if form.is_valid():
        form.save()
        context = {}
        # form.ProductBacklogForm()
        return redirect('index')
    context = {
        "form": form,
        "title": "Add PBI"
    }

    return render(request, "add_product_backlog_item.html", context)

def EditPBI(request, *args, **kwargs):
    pbi=ProductBacklog.objects.get(pk=kwargs['pk'])
    form = ProductBacklogForm(request.POST or None, instance=pbi)
    if form.is_valid():
        form.save()
        context = {}
        # form.ProductBacklogForm()
        return redirect('index')
    context = {
        "form": form,
        "title": "Edit PBI"
    }

    return render(request, "add_product_backlog_item.html", context)

