from django.db import models
from custom_auth.models import CustomUser
from productBacklog.models import ProductBacklogItem
# Create your models here.

class Task(models.Model):
    owner=models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    effort=models.PositiveSmallIntegerField(default=0)
    status=models.CharField(max_length=2, choices=[('TD','To-Do'),('P','In Progress'),('D','Done')],default='TD')
    pbi=models.ForeignKey(ProductBacklogItem, on_delete=models.CASCADE, blank=True, null=True)
    description=models.TextField(max_length=1000)

    def __str__(self):
        return self.description
