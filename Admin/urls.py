from django.urls import path, include
from . import views

app_name = 'Admin'

urlpatterns = [
	path('', views.home, name='home'),
	path('vendor/',views.vendorprofile,name='vendorprofile')
]
