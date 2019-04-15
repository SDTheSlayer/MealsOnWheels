import pyrebase
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect, reverse


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
def home(request, curr_vendor):
	if request.user.is_authenticated:
		details = {i.key(): i.val() for i in database.child('Vendors').child(curr_vendor).get().each()}
		context = {
			'address': details['address'],
			'closingTime': details['closingTime'],
			'email': details['email'],
			'name': details['name'],
			'openingTime': details['openingTime'],
			'phone': details['phone'],
			'type': details['type'],
			'rating': details['rating'],
		}
		return render(request, 'Vendor/home.html', context)
	return redirect(reverse('Authentication:login'))


# TODO: redirect back to page where request was made (LOGIN_URL)
@login_required
def menu(request):
	vendors = database.child('Vendors').shallow().get().val()
	curr_vendor_list = [i for i in vendors if database.child('Vendors').child(i).child('email').get().val() == request.user.email]
	if curr_vendor_list:
		curr_vendor = curr_vendor_list[0]
	else:
		return redirect(reverse('Authentication:login'))
	context = {'categorywise_dict': database.child('Menus').child(curr_vendor).get().val()}
	return render(request, 'Vendor/menu.html', context)


@login_required
def curr_orders(request):
	vendors = database.child('Vendors').shallow().get().val()
	curr_vendor_list = [i for i in vendors if database.child('Vendors').child(i).child('email').get().val() == request.user.email]
	if curr_vendor_list:
		curr_vendor = curr_vendor_list[0]
	else:
		error_msg = {'msg': "You are not a registered Vendor!"}
		return render(request, 'Authentication/login.html', error_msg)

	# TODO: change delivered to notDelivered in next 3 lines.
	not_delivered_orders = database.child('Transactions').child('delivered').shallow().get().val()
	curr_transactions_list = [database.child('Transactions').child('delivered').child(i).get().val() for i in not_delivered_orders if database.child(
		'Transactions').child('delivered').child(i).child('vendor').get().val() == curr_vendor]
	context = {'curr_transactions_list': curr_transactions_list}
	return render(request, 'Vendor/curr_orders.html', context)


@login_required
def reviews(request):
	vendors = database.child('Vendors').shallow().get().val()
	curr_vendor_list = [i for i in vendors if database.child('Vendors').child(i).child('email').get().val() == request.user.email]
	if curr_vendor_list:
		curr_vendor = curr_vendor_list[0]
	else:
		error_msg = {'msg': "You are not a registered Vendor!"}
		return render(request, 'Authentication/login.html', error_msg)

	reviews_list = [database.child('Reviews').child(i).get().val() for i in database.child('Reviews').shallow().get().val() if database.child(
					'Reviews').child(i).child('vendor').get().val() == curr_vendor]
	context = {'reviews_list': reviews_list}
	return render(request, 'Vendor/reviews.html', context)


@login_required
def post_menu(request):
	vendors = database.child('Vendors').shallow().get().val()
	curr_vendor_list = [i for i in vendors if database.child('Vendors').child(i).child('email').get().val() == request.user.email]
	if curr_vendor_list:
		curr_vendor = curr_vendor_list[0]
	else:
		error_msg = {'msg': "You are not a registered Vendor!"}
		return render(request, 'Authentication/login.html', error_msg)

	if request.method == 'POST':
		category = request.POST.get('category')
		print(category)
		if category == 'new':
			category_name = request.POST.get('category_input')
		elif category == 'existing':
			category_name = request.POST.get('category_select')
		else:
			return redirect('Vendor:reviews')

		item_name = request.POST.get('item')
		ingredients = request.POST.get('ingredients')
		mark = request.POST.get('mark')
		price = request.POST.get('price')
		dict_item_properties = {'ingredients': ingredients, 'mark': mark, 'price': price}
		dict_item = {item_name: dict_item_properties}

		database.child('Menus').child(curr_vendor).child(category_name).set(dict_item)
		return redirect('Vendor:menu')
	return redirect('Vendor:reviews')
