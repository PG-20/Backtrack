from django.urls import path
from productBacklog import views


urlpatterns = [
    path('', views.ProductBacklogView, name='pb'),
    path('<int:pk>/', views.ViewPBIView.as_view(), name='view-pbi'),
    path('add/', views.AddPBIView.as_view(), name='add-pbi'),
    path('edit/<int:pk>', views.EditPBIView, name='edit-pbi'),
    path('delete/<int:pk>', views.DeletePBI, name='delete-pbi')
]
