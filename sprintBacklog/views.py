from django.shortcuts import render
from django.views.generic.edit import UpdateView, CreateView
from products.models import Sprint
from productBacklog.models import ProductBacklogItem
from .forms import AddTaskForm, AddSprintForm
from datetime import datetime
from django.db.models import Sum

def SprintBacklogView(request):
    sprints = Sprint.objects.get(current=True)
    print(sprints.productbacklogitem_set.all().aggregate(Sum('effort')))
    left = sprints.capacity - sprints.productbacklogitem_set.all().aggregate(Sum('effort'))['effort__sum']
    context = {
        "sprint": sprints,
        "capacity_left": left
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
