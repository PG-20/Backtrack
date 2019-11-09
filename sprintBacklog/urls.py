from django.urls import path
from sprintBacklog import views



urlpatterns = [
    path('', views.SprintBacklogView, name='sb'),
    path('add-task/<int:pk>', views.AddTask.as_view(), name='add-task'),
    path('edit/<int:pk>', views.EditTask, name='edit-task'),
    path('add/', views.AddSprint.as_view(), name='add-sprint'),
    path('delete/<int:pk>', views.DeleteTask, name='delete-task'),
    path('remove-pbi/<int:pk>', views.RemovePBIFromSprint, name='remove-pbi-from-sprint')
]
