from django.shortcuts import render, redirect
from django.views.generic.edit import UpdateView, CreateView
from django.http import HttpResponse
from django.forms.models import model_to_dict
from datetime import datetime

from .models import ProductBacklog
from .forms import ProductBacklogForm
import logging

logger = logging.getLogger(__name__)

def index(request):
    return redirect('product_backlog/')


def ProductBacklogView(request):
    pbis = ProductBacklog.objects.all().order_by('priority', '-last_updated')
    skip=False
    for i in range(len(pbis)):
        if skip:
            skip=False
            continue
        if i+1 < len(pbis) and pbis[i].priority == pbis[i+1].priority:
            pbis[i+1].priority = i+1
            pbis[i+1].save()
            skip=True
            continue
        print(i)
        pbis[i].priority = i+1
        pbis[i].save()
    context = {'title': "Product Backlog", 'pbis': pbis.order_by('priority')}
    return render(request, 'product_backlog.html', context)


class AddPBIView(CreateView):
    form_class = ProductBacklogForm
    template_name = 'add_product_backlog_item.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = "Add PBI"
        context['url'] = self.request.get_full_path()
        return context

    def form_valid(self, form):
        form.save()
        return render(self.request, 'updateSuccess.html')


def EditPBIView(request, *args, **kwargs):
    pbi=ProductBacklog.objects.get(pk=kwargs['pk'])
    form = ProductBacklogForm(request.POST or None, instance=pbi)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            pbi.last_updated = datetime.now()
            pbi.save()
            return render(request, 'updateSuccess.html')
    #     TODO: handle else condition since it is causing UI break
    context = {
        "form": form,
        "label": "Edit PBI",
        "url": request.get_full_path()
    }
    return render(request, "add_product_backlog_item.html", context)

def DeletePBI(request, pk):
    ProductBacklog.objects.get(pk=pk).delete()
    return HttpResponse(pk)




