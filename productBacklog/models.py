from django.db import models
from products.models import User, Product, Sprint
from datetime import datetime
from django.urls import reverse
import django
# Create your models here.

class ProductBacklogItem(models.Model):
    # product=models.ForeignKey(Product, on_delete=models.CASCADE) commented for now
    title=models.CharField(max_length=100)
    effort=models.PositiveSmallIntegerField(default=0)
    story_points=models.PositiveSmallIntegerField()
    priority = models.PositiveSmallIntegerField()
    effort_done=models.PositiveSmallIntegerField(default=0)
    status=models.CharField(max_length=2,choices=[('TD','To-Do'),('P','In Progress'),('D','Done'),('NF', 'Not Finished')],default='TD')
    last_updated=models.DateTimeField(default=django.utils.timezone.now)
    pbi_type=models.CharField(max_length=2,choices=[('B','Bug'),('E','Epic'),('US','User Story')],default='US')
    sprint=models.ForeignKey(Sprint, blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.title}"