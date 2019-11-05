from django.shortcuts import render
from .models import Task,Sprint
from django.views.generic.edit import UpdateView, CreateView

from .forms import AddTaskForm
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
