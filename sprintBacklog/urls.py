from django.urls import path
from sprintBacklog import views



urlpatterns = [
    path('', views.SprintBacklogView, name='sb'),
    path('add-task/', views.AddTask.as_view(), name='add-task'),
    path('add/', views.AddSprint.as_view(), name='add-sprint')
]