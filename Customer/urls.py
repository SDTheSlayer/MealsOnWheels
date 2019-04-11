from django.urls import path, include
from . import views

app_name = 'Customer'

urlpatterns = [
	path('', views.home, name='home'),
	path('restaurant', views.rest_view, name='restaurant'),
]