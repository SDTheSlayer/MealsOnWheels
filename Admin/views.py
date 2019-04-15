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

all_list = database.get().each()

data = {}

for i in all_list:
    data.update({i.key(): i.val()})

def home(request):
    all_list = database.get().each()
    data = {}
    for i in all_list:
        data.update({i.key(): i.val()})
    vendors = data['Vendors']
    ven_list = {}
    for i in vendors:
        cur = vendors[i]
        addr = cur['address']
        ctime = cur['closingTime']
        email = cur['email']
        name = cur['name']
        otime = cur['openingTime']
        phone = cur['phone']
        _type = cur['type']
        avgprice = cur['avgPrice']
        time = str(otime) + ":00 - " + str(ctime) + ":00"
        d = dict({'Address': addr, 'Time': time, 'Email': email, 'phone': phone,
                  'Type': _type, 'Price': avgprice})
        ven_list.update({name: d})

    deliverylist = {}
    deliverers = data['Deliverers']
    for i in deliverers:
        cur = deliverers[i]
        addr = cur['address']
        email = cur['email']
        name = cur['name']
        phone = cur['phone']
        d = dict({'Address': addr, 'Email': email, 'phone': phone})
        deliverylist.update({name: d})
    return render(request, 'Admin/adminhome.html', {'ven_list': ven_list,'deliverylist':deliverylist})

def vendorprofile(request):
    return render(request, 'Admin/vendorprofile.html')