from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from sprintBacklog.views import endSprint
from products.models import Sprint
from datetime import datetime
from django.http import HttpResponse
from .models import ProductBacklogItem
from .forms import ProductBacklogForm
from custom_auth.models import Product
from django.contrib.auth.views import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


@login_required
def ProductBacklogView(request, pk):
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

    context = {'title': "Product Backlog", 'pbiList': [pbis, pbis2], 'product': Product.objects.get(pk=pk)}
    return render(request, 'product_backlog.html', context)


class ViewPBIView(LoginRequiredMixin, DetailView):
    model = ProductBacklogItem
    context_object_name = 'pbi'
    template_name = 'viewPBI.html'


class AddPBIView(LoginRequiredMixin, CreateView):
    form_class = ProductBacklogForm
    template_name = 'add_product_backlog_item.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = "Add PBI"
        context['url'] = self.request.get_full_path()
        return context

    def form_valid(self, form):
        pbi = form.save(commit=False)
        pbi.product = self.request.user.productOwned
        pbi.save()
        return render(self.request, 'updateSuccess.html', {'message': "PBI added successfully"})


@login_required
def EditPBIView(request, pk):
    pbi = ProductBacklogItem.objects.get(pk=pk)
    prevPriority = pbi.priority
    form = ProductBacklogForm(request.POST or None, instance=pbi)
    if request.method == "POST":
        if form.is_valid():
            pbi = form.save(commit=False)

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


@login_required
def DeletePBI(request, pk):
    ProductBacklogItem.objects.get(pk=pk).delete()
    return HttpResponse(pk)


@login_required
def AddPBIToCurrentSprint(request, pk):
    pbi = ProductBacklogItem.objects.get(pk=pk)
    sprint = get_object_or_404(Sprint, current=True)
    pbi.sprint = sprint
    pbi.status = 'P'
    pbi.save()
    return redirect('pb', pk=pbi.product.id)
