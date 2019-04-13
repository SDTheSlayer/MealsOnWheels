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

all_list= database.get().each()

data={}

for i in all_list:
    data.update({i.key():i.val()})

def home(request):
    all_list = database.get().each()
    data = {}
    for i in all_list:
        data.update({i.key(): i.val()})
    vendors = data['Vendors']
    ven_list = {}
    for i in vendors:
        cur=vendors[i]
        addr = cur['address']
        ctime = cur['closingTime']
        email =cur['email']
        name = cur['name']
        otime =  cur['openingTime']
        phone = cur['phone']
        _type =cur['type']
        d = dict({'Address': addr, 'ClosingTime': ctime, 'Email': email, 'OpeningTime': otime, 'phone': phone,
                  'Type': _type})
        ven_list.update({name: d})
    return render(request, 'Customer/custhome.html', {'ven_list': ven_list})


def rest_view(request):
    all_list = database.get().each()
    data = {}
    for i in all_list:
        data.update({i.key(): i.val()})
    restname = request.POST.get('restaurant')
    main = {}
    dessert = {}
    bev = {}
    vendors = data['Vendors']
    for i in vendors:
        if vendors[i]['name'] == restname:
            uid = i
            break
    menu=data['Menus']
    if uid in menu:
        restmenu=menu[uid]
        main=restmenu["Main Course"]
        dessert=restmenu["Dessert"]
        bev=restmenu["Beverages"]
    return render(request, 'Customer/restaurant_view.html', {'Main_Course': main, 'Beverages': bev, "Dessert": dessert,
                                                             "uid": uid})


def profile_view(request):
    all_list = database.get().each()
    data = {}
    for i in all_list:
        data.update({i.key(): i.val()})
    users = data['Users']
    for i in users:
        curuser= users[i]
        if curuser['email'] == request.user.email:
            uid = i
            curaddress = curuser['deliveryAddress']
            curphone = curuser['phone']
            break
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            first_name = request.user.first_name
            last_name = request.user.last_name
            address = form.cleaned_data.get('address')
            phone_number = form.cleaned_data.get('phone_number')
            name = first_name + " " + last_name
            newdata = {"deliveryAddress": address, "email": request.user.email, "name": name, "phone": phone_number}
            database.child("Users").child(uid).update(newdata)
            return redirect('Customer:home')
    else:
        form = ProfileForm(initial={"address": curaddress, "phone_number": curphone})
    return render(request, 'Customer/profile.html', {'form': form})


def cart_view(request):
    all_list = database.get().each()
    data = {}
    for i in all_list:
        data.update({i.key(): i.val()})
    restid=request.POST.get('restaurant')
    order= {}
    total = 0
    restmenu=data['Menus'][restid]
    for j in {'Main Course','Dessert','Beverages'}:
        for i in restmenu[j]:
            item = restmenu[j][i]
            quantity = request.POST.get(i)
            quantity=int(quantity)
            if quantity > 0:
                price = item['price']
                price = int(price)
                item = dict({"quantity":quantity,"price":price})
                order.update({i:item})
                total=total+price*quantity

    return render(request, 'Customer/cart.html',{"order":order, "restid":restid, "total":total})
