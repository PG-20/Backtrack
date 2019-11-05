from django.shortcuts import render
from .models import Task,Sprint
from django.views.generic.edit import UpdateView, CreateView

from .forms import AddTaskForm,AddSprintForm
# from .forms import ProductBacklogForm
import logging

logger = logging.getLogger(__name__)

# Create your views here.
def index(request):
    return redirect('sprint_backlog/')

def SprintBacklogView(request):
    return render(request, 'sprint_backlog.html')


class AddTask(CreateView):
    form_class = AddTaskForm
    template_name = 'task.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = "Add Task"
        context['url'] = self.request.get_full_path()
        return context

    def form_valid(self, form):
        form.save()
        return render(self.request, 'updateSuccess.html')


class AddSprint(CreateView):
    
    form_class = AddSprintForm
    template_name = 'add_sprint.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['label'] = "Add Sprint"
        context['url'] = self.request.get_full_path()
        print("inside ADD SPRINR")
        return context

    def form_valid(self, form):
        form.save()
        return render(self.request, 'updateSuccessSprint.html')
