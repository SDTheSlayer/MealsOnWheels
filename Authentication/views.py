import pyrebase
from django.contrib.auth import logout
from django.shortcuts import render, redirect, HttpResponseRedirect

import Vendor.views
from .forms import SignUpForm

config = {
	'apiKey': "AIzaSyC6MLEYIZxv7DHhs-vtmCB3rLkd1y2r3bI",
	'authDomain': "mealsonwheelsiit.firebaseapp.com",
	'databaseURL': "https://mealsonwheelsiit.firebaseio.com",
	'projectId': "mealsonwheelsiit",
	'storageBucket': "mealsonwheelsiit.appspot.com",
	'messagingSenderId': "755544742392"
}
firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
database = firebase.database()


# Create your views here.
def login_user(request):
	return render(request, 'Authentication/login.html')


def logout_user(request):
	logout(request)
	return redirect('Authentication:login')


def post_login(request):
	# Check if user is logged in using Django Authentication
	if request.user.is_authenticated:

		# TODO: Change to code like Vendor's below
		# Check if user is present in Customers
		customers = database.child('Users').shallow().get().val()
		for i in customers:
			curemail = database.child('Users').child(i).child('email').get().val()
			if curemail == request.user.email:
				return render(request, 'Authentication/home.html', {'usertype': 'Customer'})

		# Check if user is present in Vendors
		vendors = database.child('Vendors').shallow().get().val()
		curr_vendor_list = [i for i in vendors if database.child('Vendors').child(i).child('email').get().val() == request.user.email]
		if curr_vendor_list:
			return Vendor.views.home(request, curr_vendor_list[0])

		# TODO: Change to code like Vendor's above
		# Check if user is present in Deliverers
		delivery = database.child('Deliverers').shallow().get().val()
		for i in delivery:
			curemail = database.child('Deliverers').child(i).child('email').get().val()
			if curemail == request.user.email:
				return render(request, 'Authentication/home.html', {'usertype': 'Delivery'})

		# If not present anywhere ask him to signup
		return redirect('Authentication:signup')

	# If not logged in ask him to login(Django)
	return redirect('Authentication:login')


def signup(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			first_name = form.cleaned_data.get('first_name')
			last_name = form.cleaned_data.get('last_name')
			address_line1 = form.cleaned_data.get('address_line1')
			city = form.cleaned_data.get('city')
			phone_number = form.cleaned_data.get('phone_number')
			address = address_line1 + ", " + city
			name = first_name + " " + last_name
			data = {"deliveryAddress": address, "email": request.user.email, "name": name, "phone": phone_number}
			database.child("Users").push(data)
			return redirect('Authentication:home')
	else:
		form = SignUpForm(initial={'first_name': request.user.first_name, 'last_name': request.user.last_name})
	return render(request, 'Authentication/signup.html', {'form': form})
