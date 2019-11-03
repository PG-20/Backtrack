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
            'main_dev',
            'other_dev',
            'priority'
        ]

    def clean_priority(self):
        data = self.cleaned_data['priority']
        if data > len(ProductBacklog.objects.all())+1:
            raise forms.ValidationError("Priority exceeds number of PBIS")
        elif data < 1:
            raise forms.ValidationError("Priority cannot be less than 1")
        return data
