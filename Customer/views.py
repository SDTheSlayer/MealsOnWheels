from django.shortcuts import render, redirect, HttpResponseRedirect

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
        _type = database.child('Vendors').child(i).child('type').get().val()
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
            c = dict({'ingredients': database.child('Menus').child(uid).child("Main Course").child(i).child("ingredients").get().val(),
                      'isSpicy': database.child('Menus').child(uid).child("Main Course").child(i).child("isSpicy").get().val(),
                      'price': database.child('Menus').child(uid).child("Main Course").child(i).child("price").get().val()})
            main.update({i: c})
        print(main)
    return render(request, 'Customer/restaurant_view.html')
