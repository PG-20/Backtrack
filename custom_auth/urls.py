from django.urls import path, include
from django.conf.urls import url
from custom_auth import views
from productBacklog import views as pb_views
from sprintBacklog import views as sb_views

urlpatterns = [
    path('', views.ProductsView, name='products'),
    path('add/', views.AddProductView, name='add-product'),
    path('<int:pk>/productBacklog/', pb_views.ProductBacklogView, name='pb'),
    path('edit/<int:pk>/', views.AddProductView, name='edit-product'),
    path('<int:pk>/', views.ProductDetailsView.as_view(), name='view-product'),
    path('<int:pk>/sprintBacklog/', sb_views.SprintBacklogView, name='sb'),
    path('<int:pk>/add-sprint/', sb_views.AddSprint.as_view(), name='add-sprint'),
    path('<int:pk>/start-sprint/', sb_views.StartSprint, name='start-sprint'),
]
