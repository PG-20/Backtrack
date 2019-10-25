from django import forms

from .models import ProductBacklog

 
class ProductBacklogForm(forms.ModelForm):
    class Meta:
        model=ProductBacklog
        fields=[
            'title',
            'effort',
            'story_points',
            'effort_done',
            'status',
            
            'pbi_type',
            'sprint_no',
            'main_dev',
            'other_dev',
            'priority'
        ]