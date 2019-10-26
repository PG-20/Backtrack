from django.urls import path
from productBacklog import views


urlpatterns = [
    path('', views.ProductBacklogView, name='pb'),
    path('add/', views.AddPBI, name='add-pbi'),
    path('edit/<int:pk>', views.EditPBI, name='edit-pbi'),
    path('delete/<int:pk>', views.DeletePBI, name='delete-pbi')
]
