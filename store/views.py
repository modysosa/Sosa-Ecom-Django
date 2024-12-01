from django.shortcuts import render, redirect
from .models import Product, Category, Profile
# for login
from django.contrib.auth import authenticate, login ,logout
# from messages
from django.contrib import messages
# for register
from django.contrib.auth.models import  User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm


from payment.forms import ShippingForm
from payment.models import ShippingAddress


from django import forms
from django.db.models import Q
import json
from cart.cart import Cart

# search for products

def search(request):
    # Determine if the filled out the form
    if request.method == "POST":
        searched = request.POST['searched']
        #  query the products
        searched = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))
        # test for null
        if not searched:
            messages.success(request, "That Product Is Not Exist... Please Try Again")
            return render(request, "search.html",{})
        else:
            # return the search results
            return render(request,"search.html",{'searched':searched})
    else:
        return render(request,"search.html",{})



# fuction for update user information
def update_info(request):
    if request.user.is_authenticated:
        # Get current user information
        current_user = Profile.objects.get(user__id=request.user.id)
        # Get current shipping address information
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)

        # Get original user form
        form = UserInfoForm(request.POST or None, instance=current_user)
        # Get user's shipping form
        shipping_form = ShippingForm(request.POST or None ,instance=shipping_user)

        if form.is_valid() or shipping_form.is_valid():
            # save original Form
            form.save()
            # save shipping form
            shipping_form.save()
            messages.success(request, ("Your Account has been updated..."))
            return redirect('home')
        return render(request, "update_info.html", {'form':form, 'shipping_form':shipping_form})
    else:
        messages.success(request, "You Must Be Logged In To Access That Page...")
        return redirect('login')

def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        # Did they fill out the form
        if request.method == 'POST':
            ##########
            form = ChangePasswordForm(current_user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Your password has been updated... Please Login again.")
                return redirect('login')
            else:
                for error in list(form.errors.values()):
                    messages.error(request,error)
            ################################
        else:
            form = ChangePasswordForm(current_user)
        return render(request, 'update_password.html', {'form': form})
    else:
        messages.error(request, "You must be logged in to change your password.")
        return redirect('login')

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)

        if user_form.is_valid():
            user_form.save()
            login(request, current_user)
            messages.success(request, ("Your Account has been updated..."))
            return redirect('home')
        return render(request, "update_user.html", {'user_form':user_form})
    else:
        messages.success(request, "You Must Be Logged In To Access That Page...")
        return redirect('login')


def category_summary(request):
    # Grap all thing from cattegory model 
    categories = Category.objects.all()
    return render(request, 'category_summary.html',{'categories':categories})

# category dropdown
def category(request, cat):
    # replace Hyphens with Spaces
    cat = cat.replace('-', ' ')
    # grab the cattegory from url
    try:
        # look up the cattegory
        category = Category.objects.get(name=cat)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html',{'products':products, 'category':category})
    except:
        messages.success(request, ("That Category Dosen't Exist..."))
        return redirect('home')

# product page
def product(request,pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product': product})


def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})


def about(request):
    return render(request, 'about.html', {})

# login user form 
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request, user)
            # retrive the old ccart data from model to user cart
            # first get the current user
            current_user = Profile.objects.get(user__id=request.user.id)
            # get thier saved cart from database
            saved_cart = current_user.old_cart
            # convert database string to python dicionary
            if saved_cart:
                #  convert to dicionary using JSON {"3":2,"4":3} to {'3':2,'4':3}
                converted_cart = json.loads(saved_cart)
                # Add the loaded cart dictionary to our session
                # Get the cart
                cart = Cart(request)
                # add the loaded cart to our session
                for key, value in converted_cart.items():
                    cart.db_add(product=key, quantity=value)


            messages.success(request, ("You have been logged In...Thanks"))
            return redirect('home') 
        else:
            messages.success(request, ("There was an error, Please try again."))
            return redirect('login') 
    else:
        return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, ("You have been logged out...Thanks"))
    return redirect('home') 

# register user form
def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            #login user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("Username Created Please fill Out Your Information... "))
            return redirect('update_info')
        else:
            messages.success(request, ("There wase a proplem sorry..."))
            return redirect('register')
    else:
        return render(request, 'register.html', {'form':form})
