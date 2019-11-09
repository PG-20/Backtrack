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
            'status',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].required = False

 
class AddSprintForm(forms.ModelForm):
    class Meta:
        model=Sprint
        fields=[
            'capacity',
        ]
