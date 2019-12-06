from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.db.models import Q
from .models import CustomUser, Product


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('email', 'name', 'role')
        widgets = {'role': forms.RadioSelect()}


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'name', 'role')
        widgets = {'role': forms.RadioSelect()}


class ProductForm(forms.ModelForm):
    developers = forms.ModelMultipleChoiceField(queryset=None)

    class Meta:
        model = Product
        fields = [
            'name',
            'sprint_length',
            'developers',
            'description'
        ]

    def __init__(self, user, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['developers'].queryset = CustomUser.objects.filter(productOwned__isnull=True,
                                                                       developing__isnull=True, role__exact=1).exclude(
            email=user.email) if not self.instance else CustomUser.objects.filter(
            Q(productOwned__isnull=True, role__exact=1) & (
                        Q(developing__isnull=True) | Q(developing=self.instance))).exclude(email=user.email)
        self.fields['developers'].initial = self.instance and self.instance.developers.all()
        self.fields['name'].disabled = not not self.instance
        self.fields['sprint_length'].disabled = not not self.instance
