from django.shortcuts import render, redirect, HttpResponseRedirect
import pyrebase
from .forms import delivererform, adddelivererform, addvendorform, vendorform

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
    return render(request, 'Admin/adminhome.html', {'ven_list': ven_list, 'deliverylist': deliverylist})


def delivererprofile(request):
    all_list = database.get().each()
    data = {}
    for i in all_list:
        data.update({i.key(): i.val()})

    name = request.POST.get('deliverer')
    deliverers = data['Deliverers']
    for i in deliverers:
        if deliverers[i]['name'] == name:
            uid = i
            break
    deliver = deliverers[uid]
    curaddress = deliver['address'].split(',')[0:-1]
    curcity = deliver['address'].split(',')[-1]
    curaddress = ','.join(curaddress)
    curphone = deliver['phone']
    email = deliver['email']
    form = delivererform(initial={"address_line1": curaddress, 'city': curcity, "phone_number": curphone})
    return render(request, 'Admin/delivererprofile.html', {'form': form, 'name': name, 'email': email})


def post_delivererprofile(request):
    all_list = database.get().each()
    data = {}
    for i in all_list:
        data.update({i.key(): i.val()})

    name = request.GET.get('name')
    deliverers = data['Deliverers']
    for i in deliverers:
        if deliverers[i]['name'] == name:
            uid = i
            break
    email = deliverers[uid]['email']
    form = delivererform(request.POST)
    if form.is_valid():
        address = form.cleaned_data.get('address_line1')
        city = form.cleaned_data.get('city')
        phone_number = form.cleaned_data.get('phone_number')
        addressfull = address + "," + city
        newdata = {"address": addressfull, "phone": phone_number}
        database.child("Deliverers").child(uid).update(newdata)
        return redirect('Admin:home')


def vendorprofile(request):
    all_list = database.get().each()
    data = {}
    for i in all_list:
        data.update({i.key(): i.val()})

    name = request.POST.get('restaurant')
    vendors = data['Vendors']
    for i in vendors:
        if vendors[i]['name'] == name:
            uid = i
            break
    vendor = vendors[uid]
    curaddress = vendor['address'].split(',')[0:-1]
    curcity = vendor['address'].split(',')[-1]
    curaddress = ','.join(curaddress)
    curphone = vendor['phone']
    curavgPrice = vendor['avgPrice']
    curclosingTime = vendor['closingTime']
    curopeningTime = vendor['openingTime']
    curtype = vendor['type']
    email = vendor['email']
    location = vendor['location']
    form = vendorform(
        initial={"address": curaddress, 'city': curcity, "phone_number": curphone, "avgPrice": curavgPrice,
                 "closingTime": curclosingTime, "openingTime": curopeningTime, "type": curtype})
    return render(request, 'Admin/vendorprofile.html', {'form': form, 'name': name, 'email': email,'location':location})


def post_vendorprofile(request):
    all_list = database.get().each()
    data = {}
    for i in all_list:
        data.update({i.key(): i.val()})
    name = request.GET.get('name')
    vendors = data['Vendors']
    for i in vendors:
        if vendors[i]['name'] == name:
            uid = i
            break
    email = vendors[uid]['email']
    form = vendorform(request.POST)
    if form.is_valid():
        vendorLocation = request.POST.get('pinlatitude') + "," + request.POST.get('pinlongitude')
        address = form.cleaned_data.get('address')
        city = form.cleaned_data.get('city')
        phone_number = form.cleaned_data.get('phone_number')
        addressfull = address + "," + city
        avgPrice = str(form.cleaned_data.get('avgPrice'))
        openingTime = form.cleaned_data.get('openingTime')
        closingTime = form.cleaned_data.get('closingTime')
        type = form.cleaned_data.get('type')
        newdata = {"address": addressfull, "phone": phone_number, "avgPrice": avgPrice, "openingTime": openingTime,
                   "closingTime": closingTime, "type": type,'location':vendorLocation}
        database.child("Vendors").child(uid).update(newdata)
        return redirect('Admin:home')


def adddeliverer(request):
    if request.method == 'POST':
        all_list = database.child("Deliverers").get().each()
        deliverers = {}
        for i in all_list:
            deliverers.update({i.key(): i.val()})

        form = adddelivererform(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            address_line1 = form.cleaned_data.get('address_line1')
            city = form.cleaned_data.get('city')
            phone_number = form.cleaned_data.get('phone_number')
            address = address_line1 + "," + city
            email = form.cleaned_data.get('email')
            for i in deliverers:
                if deliverers[i]['email'] == email:
                    return redirect('Admin:home')
            newdata = {"address": address, "email": email, 'isFree': "Yes", "name": name, "phone": phone_number}
            database.child("Deliverers").push(newdata)
            return redirect('Admin:home')
    else:
        form = adddelivererform()
    return render(request, 'Admin/adddeliverer.html', {'form': form})


def addvendor(request):
    if request.method == 'POST':
        all_list = database.child("Vendors").get().each()
        vendors = {}
        for i in all_list:
            vendors.update({i.key(): i.val()})

        form = addvendorform(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            address_line1 = form.cleaned_data.get('address_line1')
            city = form.cleaned_data.get('city')
            openingTime = form.cleaned_data.get('openingTime')

            closingTime = form.cleaned_data.get('closingTime')
            vendorLocation = request.POST.get('pinlatitude') + "," + request.POST.get('pinlongitude')
            phone_number = form.cleaned_data.get('phone_number')
            address = address_line1 + "," + city
            email = form.cleaned_data.get('email')
            type = form.cleaned_data.get('type')
            avgPrice = str(form.cleaned_data.get('avgPrice'))
            for i in vendors:
                if vendors[i]['email'] == email:
                    return redirect('Admin:home')
            newdata = {"address": address, "avgPrice": avgPrice, "closingTime": closingTime, "email": email,
                       "name": name, 'noOfRatings': "0", "openingTime": openingTime, "phone": phone_number,
                       'rating': "0", "type": type,'location':vendorLocation}
            database.child("Vendors").push(newdata)
            return redirect('Admin:home')
    else:
        form = addvendorform()
    return render(request, 'Admin/addvendor.html', {'form': form})
