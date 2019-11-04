from django.db import models
from products.models import User, Product
from datetime import datetime
from django.urls import reverse
# Create your models here.

class ProductBacklog(models.Model):
    # product=models.ForeignKey(Product, on_delete=models.CASCADE) commented for now
    title=models.CharField(max_length=100)
    effort=models.IntegerField()
    story_points=models.IntegerField()
    priority = models.IntegerField()
    effort_done=models.IntegerField(default=0)
    status=models.CharField(max_length=2,choices=[('TD','To-Do'),('P','In Progress'),('D','Done'),('NF', 'Not Finished')],default='TD')
    last_updated=models.DateTimeField(auto_now=False,auto_now_add=False,default=datetime.now())
    pbi_type=models.CharField(max_length=2,choices=[('B','Bug'),('E','Epic'),('US','User Story')],default='US')
    sprint_no=models.PositiveSmallIntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.id} {self.title}"

    def get_absolute_url(self):

        # from django.core.urlresolvers import reverse
        # return reverse('', kwargs={'pk': self.pk})
        return f"/products/{self.id}/"