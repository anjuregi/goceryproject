from django.shortcuts import render,redirect
from django.views.generic import View
from .models import Carousel
from django.contrib.auth import authenticate,login,logout
from .models import Category,UserProfileTable
from django.contrib import messages
from django.contrib.auth.models import User


# Create your views here.
class Navigation(View):
    def get(self,request,*args,**kwargs):
        return render(request,"navigation.html")
class About(View):
    def get(self,request,*args,**kwargs):
        return render(request,"about.html")
class Home(View):
    def get(self,request,*args,**kwargs):
        return render(request,"home.html")

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
            if user.is_staff:
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
    return render(request, 'admin_base.html')

def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

def add_category(request):
    if request.method == "POST":
        name = request.POST['name']
        Category.objects.create(name=name)
        messages.success(request,"category added")
        return redirect("view_category")
    return render(request, 'add_category.html', locals())
def view_category(request):
    category = Category.objects.all()
    return render(request, 'view_category.html', locals())

def edit_category(request, pk):
    category = Category.objects.get(id=pk)
    if request.method == "POST":
        name = request.POST['name']
        category.name = name
        category.save()
        msg = "Category Updated"
    return render(request, 'edit_category.html', locals())

def delete_category(request, pk):
    category = Category.objects.get(id=pk)
    category.delete()
    return redirect('view_category')

from .models import Product
def add_product(request):
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
    product = Product.objects.all()
    return render(request, 'view_product.html', locals())

def edit_product(request, pk):
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
            messages.success(request, "User login successfully")
            return redirect('home')
        else:
            messages.success(request,"Invalid Credentials")
    return render(request, 'login.html', locals())


def profile(request):
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
                return redirect('main')
            else:
                messages.success(request, "Password not matching")
                return redirect('change_password')
        else:
            messages.success(request, "Invalid Password")
            return redirect('change_password')
    return render(request, 'change_password.html')

def user_product(request,pid):
    if pid == 0:
        product = Product.objects.all()
    else:
        category = Category.objects.get(id=pid)
        product = Product.objects.filter(category=category)
    allcategory = Category.objects.all()
    return render(request, "user-product.html", locals())

def product_detail(request, pid):
    product = Product.objects.get(id=pid)
    latest_product = Product.objects.filter().exclude(id=pid).order_by('-id')[:10]
    return render(request, "product_detail.html", locals())


