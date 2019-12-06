from django.urls import path
from sprintBacklog import views



urlpatterns = [
    path('add/<int:pk>', views.AddTask.as_view(), name='add-task'),
    path('edit/<int:pk>', views.EditTask, name='edit-task'),
    path('delete/<int:pk>', views.DeleteTask, name='delete-task'),
    path('remove-pbi/<int:pk>', views.RemovePBIFromSprint, name='remove-pbi-from-sprint'),
]
