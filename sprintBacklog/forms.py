from django import forms

from .models import Task
from products.models import Sprint
from custom_auth.models import CustomUser
 
class AddTaskForm(forms.ModelForm):
    class Meta:
        model=Task
        fields=[
            'description',
            'owner',
            'effort',
            'status',
        ]

    def __init__(self, product, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].required = False
        self.fields['owner'].queryset = product.developers.all()

 
class AddSprintForm(forms.ModelForm):
    class Meta:
        model=Sprint
        fields=[
            'capacity',
        ]
