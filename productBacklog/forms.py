from django import forms

from .models import ProductBacklog

 
class ProductBacklogForm(forms.ModelForm):
    class Meta:
        model=ProductBacklog
        fields=[
            'title',
            'story_points',
            'pbi_type',
            'sprint_no',
            'priority',
        ]

    def clean_priority(self):
        data = self.cleaned_data['priority']
        if data > len(ProductBacklog.objects.all())+1:
            raise forms.ValidationError("Priority exceeds number of PBIS")
        elif data < 1:
            raise forms.ValidationError("Priority cannot be less than 1")
        return data
