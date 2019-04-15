from django.urls import path
from . import views

app_name = 'Authentication'

urlpatterns = [
	path('login/', views.login_user, name='login'),
	path('logout/', views.logout_user, name='logout'),
	path('', views.post_login, name='post_login'),
	path('signup/', views.signup, name='signup'),
]
