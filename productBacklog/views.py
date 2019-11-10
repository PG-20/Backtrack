from django.shortcuts import render, redirect
from django.views.generic.edit import UpdateView, CreateView
from django.views.generic.detail import DetailView
from django.http import HttpResponse
from sprintBacklog.views import endSprint
from products.models import Sprint
from datetime import datetime, timedelta

from .models import ProductBacklogItem
from .forms import ProductBacklogForm
import logging

logger = logging.getLogger(__name__)

def index(request):
    return redirect('product_backlog/')


def ProductBacklogView(request):
    try:
        sprint = Sprint.objects.get(current=True)
    except Exception:
        sprint = None
    endSprint(sprint)
    pbis = ProductBacklogItem.objects.all().order_by('priority', '-last_updated')
    pbis2 = pbis.exclude(status='D')

    cumsp = 0
    for i in range(len(pbis)):
        pbis[i].priority = i + 1
        pbis[i].save()
        cumsp = cumsp + pbis[i].story_points
        pbis[i].cumsp = cumsp
    cumsp = 0
    for i in range(len(pbis2)):
        pbis2[i].priority = i + 1
        pbis2[i].save()
        cumsp = cumsp + pbis2[i].story_points
        pbis2[i].cumsp = cumsp

    context = {'title': "Product Backlog", 'pbiList': [pbis, pbis2]}
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
        return render(self.request, 'updateSuccess.html', {'message': "PBI added successfully"})


def EditPBIView(request, pk):
    pbi=ProductBacklogItem.objects.get(pk=pk)
    prevPriority = pbi.priority
    form = ProductBacklogForm(request.POST or None, instance=pbi)
    if request.method == "POST":
        if form.is_valid():
            pbi = form.save(commit=False)

            if form.cleaned_data['add_to_current_sprint']:
                sprint = Sprint.objects.get(current=True)
                if sprint.status == 'NS':
                    sprint.status = 'P'
                    sprint.end_date = datetime.now() + timedelta(days=15)
                    sprint.save()
                pbi.sprint = sprint
                pbi.status = 'P'

            if form.has_changed():
                pbi.last_updated = datetime.now()

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
            return render(request, 'updateSuccess.html', {'message': "PBI updated successfully"})
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
