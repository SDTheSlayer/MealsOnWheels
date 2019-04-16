from django.shortcuts import render, redirect, HttpResponseRedirect
from .forms import ProfileForm, RatingForm
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
    menu = data['Menus']
    if uid in menu:
        restmenu = menu[uid]
        review = {}
        allreviews = data['Reviews']
        s = 0
        for i in allreviews:
            if allreviews[i]['vendor'] == uid:
                review.update({s: {allreviews[i]['review']: allreviews[i]['rating']}})
                s = s + 1

        return render(request, 'Customer/restaurant_view.html',
                      {'menu': restmenu, "uid": uid, 'reviews': review, 'restname': restname})
    else:
       return redirect('Customer:home')



def profile_view(request):
    all_list = database.get().each()
    data = {}
    for i in all_list:
        data.update({i.key(): i.val()})
    users = data['Users']
    for i in users:
        curuser = users[i]
        if curuser['email'] == request.user.email:
            uid = i
            curaddress = curuser['deliveryAddress'].split(',')[0:-1]
            curcity = curuser['deliveryAddress'].split(',')[-1]
            curaddress=','.join(curaddress)
            curphone = curuser['phone']
            break
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            first_name = request.user.first_name
            last_name = request.user.last_name
            address = form.cleaned_data.get('address')
            city = form.cleaned_data.get('city')
            phone_number = form.cleaned_data.get('phone_number')
            name = first_name + " " + last_name
            addressfull = address + "," + city
            newdata = {"deliveryAddress": addressfull, "email": request.user.email, "name": name, "phone": phone_number}
            database.child("Users").child(uid).update(newdata)
            return redirect('Customer:home')
    else:
        form = ProfileForm(initial={"address": curaddress, 'city': curcity, "phone_number": curphone})
    return render(request, 'Customer/profile.html', {'form': form})


def cart_view(request):
    all_list = database.get().each()
    data = {}
    for i in all_list:
        data.update({i.key(): i.val()})
    restid = request.POST.get('restaurant')
    order = {}
    total = 0
    restmenu = data['Menus'][restid]
    for j in restmenu:
        for i in restmenu[j]:
            item = restmenu[j][i]
            quantity = request.POST.get(i)
            quantity = int(quantity)
            if quantity > 0:
                price = item['price']
                price = int(price)
                item = dict({"quantity": quantity, "price": price})
                order.update({i: item})
                total = total + price * quantity
    transaction = dict({"order": order, "restid": restid, "total": total})
    return render(request, 'Customer/cart.html', {"order": order, "restid": restid, "total": total,
                                                  "restname": data['Vendors'][restid]['name']})


def dashboard_view(request):
    all_list = database.get().each()
    data = {}
    for i in all_list:
        data.update({i.key(): i.val()})

    users = data['Users']
    all_reviews = data['Reviews']
    for i in users:
        cur_user = users[i]
        if cur_user['email'] == request.user.email:
            uid = i
            break
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            vendor = form.cleaned_data.get('vendor')
            rating = form.cleaned_data.get('rating')
            review = form.cleaned_data.get('review')
            id = form.cleaned_data.get('id')
            customer = form.cleaned_data.get('customer')
            curr_rating = float(data['Vendors'][vendor]['rating'])
            noOfRatings = int(data['Vendors'][vendor]['noOfRatings'])
            curr_rating = (curr_rating * noOfRatings + int(rating)) / (noOfRatings + 1)
            noOfRatings = noOfRatings + 1
            database.child('Vendors').child(vendor).child('rating').set(str(curr_rating))
            database.child('Vendors').child(vendor).child('noOfRatings').set(str(noOfRatings))
            newdata = {'customer':customer, 'rating':rating, 'review':review, 'vendor':vendor}

            database.child("Reviews").child(id).set(newdata)
            return  redirect('Customer:dashboard')

    del_trans = data['Transactions']['delivered']

    trans = {}
    for j in del_trans:
        if j is not None:
            if del_trans[j]['customer'] == uid:
                date = del_trans[j]['date']
                itemsOrdered = del_trans[j]['itemsOrdered']
                customer = del_trans[j]['customer']
                paymentMode = del_trans[j]['paymentMode']
                totalAmount = del_trans[j]['totalAmount']
                vendor = del_trans[j]['vendor']
                vendor_name = data['Vendors'][vendor]['name']
                if j in all_reviews.keys():
                    curr_rating = float(all_reviews[j]['rating'])
                    curr_review = all_reviews[j]['review']
                else:
                    curr_rating = 0
                    curr_review = "Write your review"
                c = {'id':j, 'date': date, 'itemsOrdered':itemsOrdered, 'paymentMode':paymentMode, 'totalAmount':totalAmount, 'vendor':vendor, 'vendorname': vendor_name,
                     'customer': customer, 'rating': curr_rating, 'review': curr_review}
                trans.update({j: c})
    return render(request, 'Customer/dashboard.html', {'trans': trans})