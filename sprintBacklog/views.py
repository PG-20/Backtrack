from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from products.models import Sprint
from productBacklog.models import ProductBacklogItem
from .forms import AddTaskForm, AddSprintForm
from datetime import datetime, timedelta
from django.db.models import Sum
from .models import Task
from custom_auth.models import Product
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import login_required


def endSprint(sprint):
    if sprint and sprint.end_date:
        time_left = sprint.end_date - datetime.now()
        if time_left.total_seconds() <= 0:
            sprint.current = False
            sprint.status = 'D'
            for pbi in sprint.productbacklogitem_set.filter(status='P'):
                pbi.sprint = None
                pbi.status = 'NF'
                pbi.save()
            sprint.save()
            return True
    return False


@login_required
def SprintBacklogView(request, pk):
    context = {
        'title': 'Sprint Backlog',
        'product': Product.objects.get(pk=pk)
    }
    try:
        sprints = Sprint.objects.get(current=True)
    except Sprint.DoesNotExist:
        sprints = None
    context['sprint'] = sprints
    if sprints:
        if not endSprint(sprints):
            if sprints.end_date:
                time_left = sprints.end_date - datetime.now()
                context['time_left'] = str(time_left.days) + " day(s)" if time_left.days > 0 else str(
                    time_left.seconds // 3600) + " hr(s)"

            context['effort'] = sprints.productbacklogitem_set.all().aggregate(Sum('effort'))['effort__sum']
            context['effortDone'] = sprints.productbacklogitem_set.all().aggregate(Sum('effort_done'))[
                'effort_done__sum'] if sprints.productbacklogitem_set.count() else 0
            context["burndown"] = int((context['effortDone'] / context['effort']) * 100) if context['effort'] else 0
            context['capacity_left'] = sprints.capacity - (context['effort'] if context['effort'] else 0)
            context['pbis'] = sprints.productbacklogitem_set.all().order_by(
                'priority') if sprints.productbacklogitem_set.count() else None
            context['cum_sp'] = sprints.productbacklogitem_set.all().aggregate(Sum('story_points'))[
                'story_points__sum'] if sprints.productbacklogitem_set.count() else 0
        else:
            del context['sprint']
            context['end_message'] = "This sprint has ended."

    return render(request, 'sprint_backlog.html', context)


class AddTask(LoginRequiredMixin, CreateView):
    form_class = AddTaskForm
    template_name = 'task.html'

    def get_form_kwargs(self):
        kwargs = super(AddTask, self).get_form_kwargs()
        kwargs['product'] = self.request.user.developing
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = "Add Task"
        context['url'] = self.request.get_full_path()
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        pbi = ProductBacklogItem.objects.get(pk=self.kwargs['pk'])
        pbi.effort += self.object.effort
        pbi.status = 'P'
        pbi.last_updated = datetime.now()
        pbi.save()
        self.object.pbi = pbi
        self.object.save()
        return render(self.request, 'updateSuccess.html', {'message': "Task was successfully added"})


class AddSprint(LoginRequiredMixin, CreateView):
    form_class = AddSprintForm
    template_name = 'add_sprint.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['label'] = "Add Sprint"
        context['url'] = self.request.get_full_path()
        return context

    def form_valid(self, form):
        sprint = form.save(commit=False)
        sprint.product = Product.objects.get(pk=self.kwargs['pk'])
        sprint.save()
        return render(self.request, 'updateSuccess.html', {'message': "Sprint was added successfully"})


@login_required
def StartSprint(request, pk):
    sprint = Sprint.objects.get(current=True)
    if sprint.status == 'NS':
        sprint.status = 'P'
        sprint.end_date = datetime.now() + timedelta(days=Product.objects.get(pk=pk).sprint_length)
        sprint.save()
        return redirect('sb', sprint.product.id)


@login_required
def EditTask(request, *args, **kwargs):
    task = Task.objects.get(pk=kwargs['pk'])
    prevTaskEffort = task.effort
    prevStatus = task.status
    form = AddTaskForm(request.user.developing, request.POST or None, instance=task)
    if request.method == "POST":
        if form.is_valid():
            taskUpdated = form.save(commit=False)

            if form.has_changed():
                pbi = taskUpdated.pbi
                if 'effort' in form.changed_data:
                    pbi.effort -= prevTaskEffort
                    pbi.effort += taskUpdated.effort

                if 'status' in form.changed_data:
                    if prevStatus != 'D' and taskUpdated.status == 'D':
                        pbi.effort_done += taskUpdated.effort
                        if pbi.effort == pbi.effort_done: pbi.status = 'D'
                    elif prevStatus == 'D' and taskUpdated.status != 'D':
                        pbi.effort_done -= taskUpdated.effort
                        if pbi.status == 'D': pbi.status = 'P'

                pbi.last_updated = datetime.now()
                pbi.save()
                taskUpdated.pbi = pbi

            taskUpdated.save()
            return render(request, 'updateSuccess.html', {'message': "Task updated successfully"})
    context = {
        "form": form,
        "label": "Edit Task",
        "url": request.get_full_path(),
        "task": task,
        "isEdit": True
    }
    return render(request, "task.html", context)


@login_required
def DeleteTask(request, pk):
    task = Task.objects.get(pk=pk)
    pbi = task.pbi
    pbi.effort -= task.effort
    pbi.effort_done -= task.effort if task.status == 'D' else 0
    if pbi.task_set.filter(status=not 'D'):
        pass
    elif pbi.task_set.count() == 1:
        pbi.status = 'P'
    else:
        pbi.status = 'D'
    pbi.last_updated = datetime.now()
    pbi.save()
    task.delete()
    return HttpResponse(pk)


@login_required
def RemovePBIFromSprint(request, pk):
    pbi = ProductBacklogItem.objects.get(pk=pk)
    pbi.sprint = None
    if pbi.status == 'P':
        pbi.status = 'TD'
        pbi.save()
        return JsonResponse({'successMessage': 'pbi removed'})
    else:
        pbi.save()
        return JsonResponse({'errorMessage': "Cannot remove done PBI"})
