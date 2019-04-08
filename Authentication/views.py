from django.shortcuts import render, HttpResponseRedirect, reverse
from django.contrib.auth import login, logout


# Create your views here.
def login_page(request):
	return render(request, 'Authentication/login_page.html')


def home(request):
	return render(request, 'Authentication/home.html')


def logout_user(request):
	logout(request)
	return HttpResponseRedirect(reverse('Authentication:home'))