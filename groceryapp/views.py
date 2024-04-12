from django.shortcuts import render,redirect,HttpResponse
from django.views.generic import View
from .models import Carousel,Booking,Feedback
from django.contrib.auth import authenticate,login,logout
from .models import Category,UserProfileTable,Cart,DeliveryProfileTable
from django.contrib import messages
from django.contrib.auth.models import User
import json
# import reportlab


# Create your views here.
class Navigation(View):
    def get(self,request,*args,**kwargs):
        return render(request,"navigation.html")
class About(View):
    def get(self,request,*args,**kwargs):
        return render(request,"about.html")
def Home(request):
    if request.user.is_superuser:
        return redirect("admindashboard")
    data = Carousel.objects.all()
    dic = {'data':data}
    return render(request, 'index.html', dic)

def Index(request):
    data = Carousel.objects.all()
    dic = {'data':data}
    return render(request, 'index.html', dic)


def adminLogin(request):
    msg = None
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        try:
            if user.is_superuser:
                login(request, user)
                msg = "User login successfully"
                return redirect('admindashboard')
            else:
                msg = "Invalid Credentials"
        except:
            msg = "Invalid Credentials"
    dic = {'msg': msg}
    return render(request, 'admin_login.html', dic)

def adminHome(request):
    if not request.user.is_superuser:
        return redirect("admin_login")
    return render(request, 'admin_base.html')

def admin_dashboard(request):
    if not request.user.is_superuser:
        return redirect("admin_login")
    user = UserProfileTable.objects.filter()
    category = Category.objects.filter()
    product = Product.objects.filter()
    new_order = Booking.objects.filter(status=1)
    dispatch_order = Booking.objects.filter(status=2)
    way_order = Booking.objects.filter(status=3)
    deliver_order = Booking.objects.filter(status=4)
    cancel_order = Booking.objects.filter(status=5)
    return_order = Booking.objects.filter(status=6)
    order = Booking.objects.filter()
    read_feedback = Feedback.objects.filter(status=1)
    unread_feedback = Feedback.objects.filter(status=2)
    return render(request, 'admin_dashboard.html', locals())

def contact(request):
    return render(request, 'contact.html')


def add_category(request):
    if not request.user.is_superuser:
        return redirect("admin_login")
    if request.method == "POST":
        name = request.POST['name']
        Category.objects.create(name=name)
        messages.success(request,"category added")
        return redirect("view_category")
    return render(request, 'add_category.html', locals())
def view_category(request):
    if not request.user.is_superuser:
        return redirect("admin_login")
    category = Category.objects.all()
    return render(request, 'view_category.html', locals())

def edit_category(request, pk):
    if not request.user.is_superuser:
        return redirect("admin_login")
    category = Category.objects.get(id=pk)
    if request.method == "POST":
        name = request.POST['name']
        category.name = name
        category.save()
        msg = "Category Updated"
    return render(request, 'edit_category.html', locals())

def delete_category(request, pk):
    if not request.user.is_superuser:
        return redirect("admin_login")
    category = Category.objects.get(id=pk)
    category.delete()
    return redirect('view_category')

from .models import Product
def add_product(request):
    if not request.user.is_superuser:
        return redirect("admin_login")
    category = Category.objects.all()
    if request.method == "POST":
        name = request.POST['name']
        price = request.POST['price']
        cat = request.POST['category']
        discount = request.POST['discount']
        desc = request.POST['desc']
        image = request.FILES['image']
        catobj = Category.objects.get(id=cat)
        Product.objects.create(name=name, price=price, discount=discount, category=catobj, description=desc, image=image)
        messages.success(request, "Product added")
    return render(request, 'add_product.html', locals())

def view_product(request):
    if not request.user.is_superuser:
        return redirect("admin_login")
    product = Product.objects.all()
    return render(request, 'view_product.html', locals())

def edit_product(request, pk):
    if not request.user.is_superuser:
        return redirect("admin_login")
    product = Product.objects.get(id=pk)
    category = Category.objects.all()
    if request.method == "POST":
        name = request.POST['name']
        price = request.POST['price']
        cat = request.POST['category']
        discount = request.POST['discount']
        desc = request.POST['desc']
        try:
            image = request.FILES['image']
            product.image = image
            product.save()
        except:
            pass
        catobj = Category.objects.get(id=cat)
        Product.objects.filter(id=pk).update(name=name, price=price, discount=discount, category=catobj, description=desc)
        messages.success(request, "Product Updated")
    return render(request, 'edit_product.html', locals())

def delete_product(request, pk):
    if not request.user.is_superuser:
        return redirect("admin_login")
    product = Product.objects.get(id=pk)
    product.delete()
    messages.success(request, "Product Deleted")
    return redirect('view_product')


def registration(request):
    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        password = request.POST['password']
        address = request.POST['address']
        mobile = request.POST['mobile']
        image = request.FILES['image']
        user = User.objects.create_user(username=email, first_name=fname, last_name=lname, email=email, password=password)
        UserProfileTable.objects.create(user=user, mobile=mobile, address=address, image=image)
        messages.success(request, "Registeration Successful")
    return render(request, 'registration.html', locals())

def userlogin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            if user.is_staff:
                login(request, user)
                msg = "User login successfully"
                return redirect('de_home')
            else:
                msg = "Invalid Credentials"
            messages.success(request, "User login successfully")
            return redirect('home')
        else:
            messages.success(request,"Invalid Credentials")
    return render(request, 'login.html', locals())

def profile(request):
    if not request.user.is_authenticated:
        return redirect("userlogin")
    data = UserProfileTable.objects.get(user=request.user)
    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        address = request.POST['address']
        mobile = request.POST['mobile']
        try:
            image = request.FILES['image']
            data.image = image
            data.save()
        except:
            pass
        user = User.objects.filter(id=request.user.id).update(first_name=fname, last_name=lname)
        UserProfileTable.objects.filter(id=data.id).update(mobile=mobile, address=address)
        messages.success(request, "Profile updated")
        return redirect('profile')
    return render(request, 'profile.html', locals())

def logoutuser(request):
    logout(request)
    messages.success(request, "Logout Successfully")
    return redirect('userlogin')

def change_password(request):
    if not request.user.is_authenticated:
        return redirect("userlogin")
    if request.method == 'POST':
        o = request.POST.get('old')
        n = request.POST.get('new')
        c = request.POST.get('confirm')
        user = authenticate(username=request.user.username, password=o)
        if user:
            if n == c:
                user.set_password(n)
                user.save()
                messages.success(request, "Password Changed")
                return redirect('userlogin')
            else:
                messages.success(request, "Password not matching")
                return redirect('change_password')
        else:
            messages.success(request, "Invalid Password")
            return redirect('change_password')
    return render(request, 'change_password.html')

def user_product(request,pid):
    if not request.user.is_authenticated:
        return redirect("userlogin")
    if pid == 0:
        product = Product.objects.all()
    else:
        category = Category.objects.get(id=pid)
        product = Product.objects.filter(category=category)
    allcategory = Category.objects.all()
    return render(request, "user-product.html", locals())

def product_detail(request, pid):
    if not request.user.is_authenticated:
        return redirect("userlogin")
    product = Product.objects.get(id=pid)
    latest_product = Product.objects.filter().exclude(id=pid).order_by('-id')[:10]
    return render(request, "product_detail.html", locals())

def addToCart(request, pid):
    if not request.user.is_authenticated:
        return redirect("userlogin")
    myli = {"objects":[]}
    try:
        cart = Cart.objects.get(user=request.user)
        myli = json.loads((str(cart.product)).replace("'", '"'))
        try:
            myli['objects'][0][str(pid)] = myli['objects'][0].get(str(pid), 0) + 1
        except:
            myli['objects'].append({str(pid):1})
        cart.product = myli
        cart.save()
    except:
        myli['objects'].append({str(pid): 1})
        cart = Cart.objects.create(user=request.user, product=myli)
    return redirect('cart')

def incredecre(request, pid):
    if not request.user.is_authenticated:
        return redirect("userlogin")
    cart = Cart.objects.get(user=request.user)
    if request.GET.get('action') == "incre":
        myli = json.loads((str(cart.product)).replace("'", '"'))
        myli['objects'][0][str(pid)] = myli['objects'][0].get(str(pid), 0) + 1
    if request.GET.get('action') == "decre":
        myli = json.loads((str(cart.product)).replace("'", '"'))
        if myli['objects'][0][str(pid)] == 1:
            del myli['objects'][0][str(pid)]
        else:
            myli['objects'][0][str(pid)] = myli['objects'][0].get(str(pid), 0) - 1
    cart.product = myli
    cart.save()
    return redirect('cart')

def cart(request):
    if not request.user.is_authenticated:
        return redirect("userlogin")
    try:
        cart = Cart.objects.get(user=request.user)
        product = (cart.product).replace("'", '"')
        myli = json.loads(str(product))
        product = myli['objects'][0]
    except:
        product = []
    lengthpro = len(product)
    return render(request, 'cart.html', locals())
    
def deletecart(request, pid):
    if not request.user.is_authenticated:
        return redirect("userlogin")
    cart = Cart.objects.get(user=request.user)
    product = (cart.product).replace("'", '"')
    myli = json.loads(str(product))
    del myli['objects'][0][str(pid)]
    cart.product = myli
    cart.save()
    messages.success(request, "Delete Successfully")
    return redirect('cart')

# def booking(request):
#     user= UserProfileTable.objects.get(user=request.user)
#     cart = Cart.objects.get(user=request.user)
#     total = 0
#     productid = (cart.product).replace("'", '"')
#     productid = json.loads(str(productid))
#     try:
#         productid = productid['objects'][0]
#     except:
#         messages.success(request, "Cart is empty, Please add product in cart.")
#         return redirect('cart')
#     for i,j in productid.items():
#         product = Product.objects.get(id=i)
#         total += int(j) * int(product.price)
#     if request.method == "POST":
#         book = Booking.objects.create(user=request.user, product=cart.product, total=total)
#         cart.product = {'objects':[]}
#         cart.save()
#         messages.success(request, "Book Order Successfully")
#         return redirect('home')
#     return render(request, "booking.html", locals())

def booking(request):
    if not request.user.is_authenticated:
        return redirect("userlogin")
    user = UserProfileTable.objects.get(user=request.user)
    cart = Cart.objects.get(user=request.user)
    total = 0
    deduction = 0
    discounted = 0
    productid = (cart.product).replace("'", '"')
    productid = json.loads(str(productid))
    try:
        productid = productid['objects'][0]
    except:
        messages.success(request, "Cart is empty, Please add product in cart.")
        return redirect('cart')
    for i,j in productid.items():
        product = Product.objects.get(id=i)
        total += int(j) * float(product.price)
        price = float(product.price) * (100 - float(product.discount)) / 100
        discounted += int(j) * price
    deduction = total - discounted
    if request.method == "POST":
        return redirect('/payment/?total='+str(total)+'&discounted='+str(discounted)+'&deduction='+str(deduction))
    return render(request, "booking.html", locals())




def myOrder(request):
    if not request.user.is_authenticated:
        return redirect("userlogin")
    order = Booking.objects.filter(user=request.user)
    return render(request, "my-order.html", locals())

ORDERSTATUS = ((1, "Pending"), (2, "Dispatch"), (3, "On the way"), (4, "Delivered"), (5, "Cancel"), (6, "Return"))
def user_order_track(request, pid):
    if not request.user.is_authenticated:
        return redirect("userlogin")
    order = Booking.objects.get(id=pid)
    orderstatus = ORDERSTATUS
    return render(request, "user-order-track.html", locals())

def change_order_status(request, pid):
    if not request.user.is_authenticated:
        return redirect("userlogin")
    order = Booking.objects.get(id=pid)
    status = request.GET.get('status')
    if status:
        order.status = status
        order.save()
        messages.success(request, "Order status changed.")
    return redirect('myorder')

def user_feedback(request):
    if not request.user.is_authenticated:
        return redirect("userlogin")
    user = UserProfileTable.objects.get(user=request.user)
    if request.method == "POST":
        Feedback.objects.create(user=request.user, message=request.POST['feedback'])
        messages.success(request, "Feedback sent successfully")
    return render(request, "feedback-form.html", locals())

def manage_feedback(request):
    if not request.user.is_superuser:
        return redirect("admin_login")
    action = request.GET.get('action', 0)
    feedback = Feedback.objects.filter(status=int(action))
    return render(request, 'manage_feedback.html', locals())

def delete_feedback(request, pid):
    if not request.user.is_superuser:
        return redirect("admin_login")
    feedback = Feedback.objects.get(id=pid)
    feedback.delete()
    messages.success(request, "Deleted successfully")
    return redirect('/manage_feedback/?action=1')

def payment(request):
    if not request.user.is_authenticated:
        return redirect("userlogin")
    total = request.GET.get('total')
    discounted = request.GET.get('discounted')
    cart = Cart.objects.get(user=request.user)
    if request.method == "POST":
        book = Booking.objects.create(user=request.user, product=cart.product, total=discounted)
        cart.product = {'objects': []}
        cart.save()
        messages.success(request, "Book Order Successfully")
        return redirect('myorder')
    return render(request, 'payment.html', locals())



def read_feedback(request, pid):
    if not request.user.is_superuser:
        return redirect("admin_login")
    feedback = Feedback.objects.get(id=pid)
    feedback.status = 1
    feedback.save()
    return HttpResponse(json.dumps({'id':1, 'status':'success'}), content_type="application/json")

def manage_order(request):
    if not request.user.is_superuser:
        return redirect("admin_login")
    action = request.GET.get('action', 0)
    order = Booking.objects.filter(status=int(action))
    order_status = ORDERSTATUS[int(action)-1][1]
    if int(action) == 0:
        order = Booking.objects.filter()
        order_status = 'All'
    return render(request, 'manage_order.html', locals()) 

def delete_order(request, pid):
    if not request.user.is_superuser:
        return redirect("admin_login")
    order = Booking.objects.get(id=pid)
    order.delete()
    messages.success(request, 'Order Deleted')
    return redirect('/manage-order/?action='+request.GET.get('action'))

def admin_order_track(request, pid):
    if not request.user.is_superuser:
        return redirect("admin_login")
    order = Booking.objects.get(id=pid)
    orderstatus = ORDERSTATUS
    status = int(request.GET.get('status',0))
    if status:
        order.status = status
        order.save()
        return redirect('admin_order_track', pid)
    return render(request, 'admin-order-track.html', locals()) 

def manage_user(request):
    if not request.user.is_superuser:
        return redirect("admin_login")
    user = UserProfileTable.objects.all()
    return render(request, 'manage_user.html', locals()) 

# def delete_user(request, pid):
#     if not request.user.is_superuser:
#         return redirect("admin_login")
#     user=User.objects.get(id=pid)
#     user.delete()
#     user_profile=UserProfileTable.objects.get(user_id=pid).delete()
#     user_profile.delete()
#     messages.success(request, "User deleted successfully")
#     return redirect('manage_user') 

def delete_user(request, pid):
    if not request.user.is_superuser:
        return redirect("admin_login")

    try:
        # Try to retrieve and delete the User and UserProfileTable objects
        user = User.objects.get(id=pid)
        user.delete()

        # user_profile = UserProfileTable.objects.get(user_id=pid)
        # user_profile.delete()

        # Success message
        messages.success(request, "User deleted successfully")
    except User.DoesNotExist:
        # Handle case where User does not exist
        messages.error(request, "User does not exist")
    # except UserProfileTable.DoesNotExist:
    #     # Handle case where UserProfileTable does not exist
    #     messages.error(request, "User profile does not exist")
    
    # Redirect to the appropriate URL
    return redirect('manage_user')

def admin_change_password(request):
    if not request.user.is_superuser:
        return redirect("admin_login")
    if request.method == 'POST':
        o = request.POST.get('currentpassword')
        n = request.POST.get('newpassword')
        c = request.POST.get('confirmpassword')
        user = authenticate(username=request.user.username, password=o)
        if user:
            if n == c:
                user.set_password(n)
                user.save()
                messages.success(request, "Password Changed")
                return redirect('home')
            else:
                messages.success(request, "Password not matching")
                return redirect('admin_change_password')
        else:
            messages.success(request, "Invalid Password")
            return redirect('admin_change_password')
    return render(request, 'admin_change_password.html')


def delivery_registration(request):
    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        password = request.POST['password']
        address = request.POST['address']
        mobile = request.POST['mobile']
        image = request.FILES['image']
        d_boy=True
        user = User.objects.create_user(username=email, first_name=fname, last_name=lname, email=email, password=password, is_staff=d_boy)
        DeliveryProfileTable.objects.create(user=user, mobile=mobile, address=address, image=image)
        messages.success(request, "Registeration Successful")
    return render(request, 'delivery_registration.html', locals())

def delivery(request):
    if not request.user.is_staff:
        return redirect("userlogin")
    user = UserProfileTable.objects.filter()
    # category = Category.objects.filter()
    # product = Product.objects.filter()
    new_order = Booking.objects.filter(status=1)
    dispatch_order = Booking.objects.filter(status=2)
    way_order = Booking.objects.filter(status=3)
    deliver_order = Booking.objects.filter(status=4)
    cancel_order = Booking.objects.filter(status=5)
    return_order = Booking.objects.filter(status=6)
    order = Booking.objects.filter()
    # read_feedback = Feedback.objects.filter(status=1)
    # unread_feedback = Feedback.objects.filter(status=2)
    return render(request, 'delivery.html', locals())

def delivery_manage_order(request):
    if not request.user.is_staff:
        return redirect("userlogin")
    action = request.GET.get('action', 0)
    order = Booking.objects.filter(status=int(action))
    order_status = ORDERSTATUS[int(action)-1][1]
    if int(action) == 0:
        order = Booking.objects.filter()
        order_status = 'All'
    return render(request, 'delivery_manage_order.html', locals()) 

def delivery_delete_order(request, pid):
    if not request.user.is_staff:
        return redirect("userllogin")
    order = Booking.objects.get(id=pid)
    order.delete()
    messages.success(request, 'Order Deleted')
    return redirect('/delivery_manage_order/?action='+request.GET.get('action'))

def delivery_order_track(request, pid):
    if not request.user.is_staff:
        return redirect("userlogin")
    order = Booking.objects.get(id=pid)
    orderstatus = ORDERSTATUS
    status = int(request.GET.get('status',0))
    if status:
        order.status = status
        order.save()
        return redirect('delivery_order_track', pid)
    return render(request, 'delivery_order_track.html', locals())