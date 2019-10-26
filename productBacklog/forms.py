from django import forms

from .models import ProductBacklog

 
class ProductBacklogForm(forms.ModelForm):
    class Meta:
        model=ProductBacklog
        fields=[
            'title',
            'effort',
            'story_points',
            'status',
            'pbi_type',
            'main_dev',
            'other_dev',
            'priority'
        ]
