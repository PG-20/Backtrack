from django import forms

from .models import Task
from products.models import Sprint
 
class AddTaskForm(forms.ModelForm):
    class Meta:
        model=Task
        fields=[
            'owner',
            'effort',
            'status',
            'pbi',
            'description',
        ]
 
class AddSprintForm(forms.ModelForm):
    class Meta:
        model=Sprint
        fields=[
            'capacity',
        ]
