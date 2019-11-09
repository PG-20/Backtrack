from django.shortcuts import render
from django.views.generic.edit import UpdateView, CreateView
from products.models import Sprint
from django.views.generic.detail import DetailView
from productBacklog.models import ProductBacklogItem
from .forms import AddTaskForm, AddSprintForm
from datetime import datetime, timedelta
from django.db.models import Sum
from .models import Task
from django.http import HttpResponse

def endSprint(sprint):
    if sprint:
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

def SprintBacklogView(request):
    sprints = Sprint.objects.get(current=True)
    context = {
        'title': 'Sprint Backlog'
    }
    if not endSprint(sprints):
        time_left = sprints.end_date - datetime.now()
        sumOfEfforts = sprints.productbacklogitem_set.all().aggregate(Sum('effort'))[
            'effort__sum'] if sprints.productbacklogitem_set.count() else 0
        sumOfEffortDone = sprints.productbacklogitem_set.all().aggregate(Sum('effort_done'))[
            'effort_done__sum'] if sprints.productbacklogitem_set.count() else 0
        burndown = int((sumOfEffortDone/sumOfEfforts)*100)
        left = sprints.capacity - sumOfEfforts
        pbis = sprints.productbacklogitem_set.all().order_by('priority')

        str_time_left = str(time_left.days)+" day(s)" if time_left.days > 0 else str(time_left.seconds//3600)+" hr(s)"
        context = {
            "sprint": sprints,
            "sprint": sprints,
            "effort": sumOfEfforts,
            "effortDone": sumOfEfforts,
            "burndown": burndown,
            "capacity_left": left,
            'title': "Sprint Backlog",
            "pbis": pbis,
            "time_left": str_time_left
        }

    return render(request, 'sprint_backlog.html', context)


class AddTask(CreateView):
    form_class = AddTaskForm
    template_name = 'task.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = "Add Task"
        context['url'] = self.request.get_full_path()
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        pbi = ProductBacklogItem.objects.get(pk=self.kwargs['pk'])
        pbi.effort += self.object.effort
        pbi.last_updated = datetime.now()
        pbi.save()
        self.object.pbi = pbi
        self.object.save()
        return render(self.request, 'updateSuccess.html', {'message': "Task was successfully added"})


class AddSprint(CreateView):
    form_class = AddSprintForm
    template_name = 'add_sprint.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = "Add Sprint"
        context['url'] = self.request.get_full_path()
        return context

    def form_valid(self, form):
        form.save()
        return render(self.request, 'updateSuccess.html', {'message': "Sprint was added successfully"})


def EditTask(request, *args, **kwargs):
    task = Task.objects.get(pk=kwargs['pk'])
    prevTaskEffort = task.effort
    prevStatus = task.status
    form = AddTaskForm(request.POST or None, instance=task)
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


def RemovePBIFromSprint(request, pk):
    pbi = ProductBacklogItem.objects.get(pk=pk)
    if pbi.status == 'P':
        pbi.sprint = None
        pbi.status = 'TD'
        pbi.save()
        return HttpResponse({"success": pk})
    else:
        return HttpResponse({'error': "Cannot remove done PBI"})
