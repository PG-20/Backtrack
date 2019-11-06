from django.shortcuts import render, redirect
from django.views.generic.edit import UpdateView, CreateView
from django.views.generic.detail import DetailView
from django.http import HttpResponse
from django.forms.models import model_to_dict
from products.models import Sprint
from datetime import datetime

from .models import ProductBacklogItem
from .forms import ProductBacklogForm
import logging

logger = logging.getLogger(__name__)

def index(request):
    return redirect('product_backlog/')


def ProductBacklogView(request):
    print(Sprint.objects.get(current=True).productbacklogitem_set.count())
    pbis = ProductBacklogItem.objects.all().order_by('priority', '-last_updated')
    cumsp = 0
    for i in range(len(pbis)):
        pbis[i].priority = i + 1
        pbis[i].save()
        cumsp = cumsp + pbis[i].story_points
        pbis[i].cumsp = cumsp

    context = {'title': "Product Backlog", 'pbis': pbis}
    return render(request, 'product_backlog.html', context)

class ViewPBIView(DetailView):
    model = ProductBacklogItem
    context_object_name = 'pbi'
    template_name = 'viewPBI.html'


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
        return render(self.  request, 'updateSuccess.html')


def EditPBIView(request, *args, **kwargs):
    pbi=ProductBacklogItem.objects.get(pk=kwargs['pk'])
    prevPriority = pbi.priority
    form = ProductBacklogForm(request.POST or None, instance=pbi)
    if request.method == "POST":
        if form.is_valid():
            form.save()

            pbi.last_updated = datetime.now()
            pbi.save()

            if form.cleaned_data['add_to_current_sprint']:
                pbi.sprint = Sprint.objects.get(current=True)
                pbi.save()

            pbis = ProductBacklogItem.objects.all().order_by('priority', '-last_updated')
            skip = False
            for i in range(len(pbis)):
                if skip:
                    skip = False
                    continue
                if i + 1 < len(pbis) and pbis[i].priority == pbis[i + 1].priority:
                    if prevPriority < pbi.priority:
                        pbis[i + 1].priority = i + 1
                        pbis[i + 1].save()
                        skip = True
                        continue
                    else:
                        pass
                pbis[i].priority = i + 1
                pbis[i].save()
            return render(request, 'updateSuccess.html')
    context = {
        "form": form,
        "label": "Edit PBI",
        "url": request.get_full_path(),
        "pbi": pbi
    }
    return render(request, "add_product_backlog_item.html", context)

def DeletePBI(request, pk):
    ProductBacklogItem.objects.get(pk=pk).delete()
    return HttpResponse(pk)




