from django.urls import path, include
from . import views

app_name = 'Authentication'

urlpatterns = [
	path('login/', views.login_page, name='login'),
	path('logout/', views.logout_user, name='logout'),
	path('home/', views.home, name='home'),
]
