from django.urls import path
from task import views



urlpatterns = [
    path('', views.SprintBacklogView, name='task'),
    path('add/', views.AddTask.as_view(), name='add-task'),
#     path('add/', views.AddPBIView.as_view(), name='add-pbi'),
#     path('edit/<int:pk>', views.EditPBIView, name='edit-pbi'),
#     path('delete/<int:pk>', views.DeletePBI, name='delete-pbi')
# ]
]