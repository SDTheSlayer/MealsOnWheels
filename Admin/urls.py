from django.urls import path, include
from . import views

app_name = 'Admin'

urlpatterns = [
    path('', views.home, name='home'),
    path('vendor/', views.vendorprofile, name='vendorprofile'),
    path('post_vendor/', views.post_vendorprofile, name='post_vendorprofile'),
    path('deliverer/', views.delivererprofile, name='delivererprofile'),
    path('post_deliverer/', views.post_delivererprofile, name='post_delivererprofile'),
    path('adddeliverer/', views.adddeliverer, name='adddeliverer'),
    path('addvendor/', views.addvendor, name='addvendor'),
]
