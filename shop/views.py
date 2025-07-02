from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render
from shop.form import CustomUserForm
from . models import *
from django.contrib import  messages
from django.contrib.auth import authenticate,login,logout
import json
from .models import Favourite

def home(request):
    products=product.objects.filter(trending=1)
    return render(request,"shop/index.html",{"products":products})


def favviewpage(request):
    if request.user.is_authenticated:
        fav=Favourite.objects.filter(user=request.user)
        return render(request,"shop/fav.html",{"fav":fav})
    else:
        return redirect("/")

def remove_fav(request,fid):
    item=Favourite.objects.get(id=fid)
    item.delete()
    return redirect("/favviewpage")

def cart_page(request):
    if request.user.is_authenticated:
        cart=Cart.objects.filter(User=request.user)
        return render(request, "shop/cart.html",{"cart":cart})
    else:
        return redirect("/")
    
def remove_cart(request,cid):
    cartitem=Cart.objects.get(id=cid)
    cartitem.delete()
    return redirect("/cart")

def fav_page(request):
   if request.headers.get('x-requested-with')=='XMLHttpRequest':
    if request.user.is_authenticated:
      data=json.load(request)
      product_id=data['pid']
      product_status=product.objects.get(id=product_id)
      if product_status:
         if Favourite.objects.filter(user=request.user.id,product_id=product_id):
          return JsonResponse({'status':'Product Already in Favourite'}, status=200)
         else:
          Favourite.objects.create(user=request.user,product_id=product_id)
          return JsonResponse({'status':'Product Added to Favourite'}, status=200)
    else:
      return JsonResponse({'status':'Login to Add Favourite'}, status=200)
   else:
    return JsonResponse({'status':'Invalid Access'}, status=200)


def add_to_cart(request):
    if request.headers.get('X-Requested-with')=='XMLHttpRequest':
        if request.user.is_authenticated:
            data=json.load(request)
            product_qty=data['product_qty']
            product_id =data['pid']
            #print(request.user.id)
            product_status=product.objects.get(id=product_id)
            if product_status:
                if Cart.objects.filter(User=request.user.id,product_id=product_id):
                    return JsonResponse({'status':'Product Already in Cart'},status=200)
                else:
                    if product_status.quantity>=product_qty:
                        Cart.objects.create(User=request.user,product_id=product_id,product_qty=product_qty)
                        return JsonResponse({'status':'Product Added to Cart'},status=200)
                    else:
                        return JsonResponse({'status':'Product stock Not Available'},status=200)
        else:
            return JsonResponse({'status':'Login to Add Cart'},status=200)
    else:
        return JsonResponse({'status':'Invalid Access'},status=200)



def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,"Logged Out Successfully")
    return redirect("/")


def login_page(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method=='POST':
            name=request.POST.get('username')
            pwd=request.POST.get('password')
            User=authenticate(request,username=name,password=pwd)
            if User is not None:
                login(request,User)
                messages.success(request,"Logged in successfully")
                return redirect("/")
            else:
                messages.error(request,"Invalid User Name or Password")
                return redirect("/login")
        return render(request, "shop/login.html")

def register(request):
        form = CustomUserForm()
        if request.method=='POST':
            form=CustomUserForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request,"Registration Success You Can Login Now")
                return redirect('/login')
        return render(request,"shop/register.html",{'form':form})

def collections(request):
    categorys= category.objects.filter(status=0)
    return render(request,"shop/collections.html",{"category":categorys})

def collectionsview(request,name):
    if(category.objects.filter(name=name,status=0)):
        products=product.objects.filter(category__name=name)
        return render(request,"shop/products/index1.html",{"products":products,"category_name":name})
    else:
        messages.warning(request,"no  such category found")
        return redirect ('collections')
    

def product_details (request,cname,pname):
    if(category.objects.filter(name=cname,status=0)):
        if(product.objects.filter(name=pname,status=0)):
            products=product.objects.filter(name=pname,status=0).first()
            return render(request,"shop/products/product_details.html",{"products":products})
        else:
            messages.error(request,"No such product Found")
            return redirect('collections')
    else:
        messages.error(request,"No such category Found")
        return redirect('collections')    


