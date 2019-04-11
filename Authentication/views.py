from django.shortcuts import render,redirect,HttpResponseRedirect
from django.contrib.auth import login, logout
from .forms import SignUpForm
import pyrebase
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
database=firebase.database()

# Create your views here.
def login_page(request):
	return render(request, 'Authentication/login_page.html')

def logout_view(request):
	logout(request)
	return redirect('Authentication:login')

def home(request):
	if request.user.is_authenticated:
		customers=database.child('Users').shallow().get().val()
		for i in customers:
			curemail=database.child('Users').child(i).child('email').get().val()
			if curemail == request.user.email:
				return render(request, 'Authentication/home.html',{'usertype':'Customer'})

		vendors=database.child('Vendors').shallow().get().val()
		for i in vendors:
			curemail=database.child('Vendors').child(i).child('email').get().val()
			if curemail == request.user.email:
				return render(request, 'Authentication/home.html',{'usertype':'Vendor'})

		delivery=database.child('Deliverers').shallow().get().val()
		for i in delivery:
			curemail=database.child('Deliverers').child(i).child('email').get().val()
			if curemail == request.user.email:
				return render(request, 'Authentication/home.html',{'usertype':'Delivery'})

		return redirect('Authentication:signup')
	else:
		return redirect('Authentication:login')


def signup(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			first_name = form.cleaned_data.get('first_name')
			last_name = form.cleaned_data.get('last_name')
			address_line1 = form.cleaned_data.get('address_line1')
			city = form.cleaned_data.get('city')
			phone_number=form.cleaned_data.get('phone_number')
			address = address_line1 + ", " + city
			name=first_name + " " + last_name
			data = {"deliveryAddress" : address , "email" : request.user.email, "name" : name , "phone" : phone_number}
			database.child("Users").push(data)
			return redirect('Authentication:home')
	else:
		form = SignUpForm(initial={ 'first_name': request.user.first_name,'last_name':request.user.last_name})
	return render(request, 'Authentication/signup.html', {'form': form})


