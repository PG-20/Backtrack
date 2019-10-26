from django.db import models
from products.models import User, Product
from datetime import datetime
from django.urls import reverse
# Create your models here.

class ProductBacklog(models.Model):
    product=models.ForeignKey(Product, on_delete=models.CASCADE, default=1)
    title=models.CharField(max_length=100)
    effort=models.IntegerField()
    story_points=models.IntegerField()
    effort_done=models.IntegerField()
    status=models.CharField(max_length=2,choices=[('TD','To-Do'),('P','In Progress'),('D','Done')],default='TD')
    last_updated=models.DateTimeField(auto_now=False,auto_now_add=False,default=datetime.now())
    pbi_type=models.CharField(max_length=2,choices=[('B','Bug'),('E','Epic'),('US','User Story')],default='US')
    sprint_no=models.PositiveSmallIntegerField(blank=True, null=True)
    main_dev=models.ForeignKey(User, on_delete=models.CASCADE, related_name="main_project_pbis")
    other_dev=models.ManyToManyField(User)
    priority=models.IntegerField(blank=True, null=True)

    def get_absolute_url(self):

        # from django.core.urlresolvers import reverse
        # return reverse('', kwargs={'pk': self.pk})
        return f"/products/{self.id}/"