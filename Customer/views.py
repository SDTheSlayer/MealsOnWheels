from django.shortcuts import render, redirect, HttpResponseRedirect
from .forms import ProfileForm
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
database = firebase.database()


def home(request):
    vendors = database.child('Vendors').shallow().get().val()
    ven_list = {}
    for i in vendors:
        addr = database.child('Vendors').child(i).child('address').get().val()
        ctime = database.child('Vendors').child(i).child('closingTime').get().val()
        email = database.child('Vendors').child(i).child('email').get().val()
        name = database.child('Vendors').child(i).child('name').get().val()
        otime = database.child('Vendors').child(i).child('openingTime').get().val()
        phone = database.child('Vendors').child(i).child('phone').get().val()
        _type = database.child('Vendors').child(i).child('rtype').get().val()
        d = dict({'Address': addr, 'ClosingTime': ctime, 'Email': email, 'OpeningTime': otime, 'phone': phone,
                  'Type': _type})

        # print(d)
        ven_list.update({name: d})
    # print(ven_list)
    return render(request, 'Customer/custhome.html', {'ven_list': ven_list})


def rest_view(request):
    restname = request.POST.get('restaurant')
    main = {}
    dessert = {}
    bev = {}
    vendors = database.child('Vendors').shallow().get().val()
    for i in vendors:
        if database.child('Vendors').child(i).child('name').get().val() == restname:
            uid = i
            break

    if uid in database.child('Menus').shallow().get().val():
        for i in database.child('Menus').child(uid).child("Main Course").shallow().get().val():
            c={}
            for j in database.child('Menus').child(uid).child("Main Course").child(i).get().each():
                c.update({j.key(): j.val()})
            main.update({i: c})
        for i in database.child('Menus').child(uid).child("Dessert").shallow().get().val():
            c = {}
            for j in database.child('Menus').child(uid).child("Dessert").child(i).get().each():
                c.update({j.key(): j.val()})
            dessert.update({i: c})
        for i in database.child('Menus').child(uid).child("Beverages").shallow().get().val():
            c = {}
            for j in database.child('Menus').child(uid).child("Beverages").child(i).get().each():
                c.update({j.key(): j.val()})
            bev.update({i: c})

    return render(request, 'Customer/restaurant_view.html',{'Main_Course': main, 'Beverages': bev, "Dessert":dessert })


def profile_view(request):
    for i in database.child("Users").shallow().get().val():
        if database.child("Users").child(i).child("email").get().val() == request.user.email:
            uid = i
            curaddress = database.child("Users").child(i).child("deliveryAddress").get().val()
            curphone = database.child("Users").child(i).child("phone").get().val()
            break
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            first_name = request.user.first_name
            last_name = request.user.last_name
            address = form.cleaned_data.get('address')
            phone_number = form.cleaned_data.get('phone_number')
            name = first_name + " " + last_name
            data = {"deliveryAddress": address, "email": request.user.email, "name": name, "phone": phone_number}
            database.child("Users").child(uid).update(data)
            return redirect('Customer:home')
    else:
        form = ProfileForm(initial={"address": curaddress, "phone_number": curphone})
    return render(request, 'Customer/profile.html', {'form': form})
