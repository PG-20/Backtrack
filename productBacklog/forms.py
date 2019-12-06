from django import forms

from .models import ProductBacklogItem
from products.models import Sprint


class ProductBacklogForm(forms.ModelForm):
    class Meta:
        model = ProductBacklogItem
        fields = [
            'title',
            'story_points',
            'pbi_type',
            'priority',
        ]

    def clean_priority(self):
        data = self.cleaned_data['priority']
        if data > len(ProductBacklogItem.objects.all()) + 1:
            raise forms.ValidationError("Priority exceeds number of PBIS")
        elif data < 1:
            raise forms.ValidationError("Priority cannot be less than 1")
        return data
