from django import forms

from .models import Task
from products.models import Sprint
 
class AddTaskForm(forms.ModelForm):
    class Meta:
        model=Task
        fields=[
            'description',
            'owner',
            'effort',
        ]
 
class AddSprintForm(forms.ModelForm):
    class Meta:
        model=Sprint
        fields=[
            'capacity',
        ]
