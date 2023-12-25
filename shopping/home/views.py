from django.http import JsonResponse
from django.shortcuts import render,redirect
from home.models import Category,Product,Cart,Favourite
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
import json

def home(request):    
    product=Product.objects.filter(trending=1)
    context={"product":product}
    return render(request,'index.html',context)

def register(request):
    if request.method=='POST':
        username=request.POST['username']
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        pass1=request.POST['password1']
        pass2=request.POST['password2']

        if pass1!=pass2:
            messages.error(request,"Password not match")
            return redirect('/register')
        
        if User.objects.filter(username=username).exists():
            messages.error(request,"user exist")
            return redirect("/register")
        else:
            myuser=User.objects.create_user(username,email,pass1)
            myuser.first_name=fname
            myuser.last_name=lname
            myuser.save()
            messages.success(request,"Signup successful")  
            login(request,myuser)
            return redirect("/")   
    return render(request,'register.html')

def fnlogin(request):
    if request.user.is_authenticated:
        messages.success(request,f"The user {request.user} Login")
        return redirect("/") 
    else:
        if request.method=="POST":
            usernamelogin=request.POST['usernamelogin']
            passwordlogin=request.POST['passwordlogin']       
            user=authenticate(username=usernamelogin,password=passwordlogin)
            if user is not None:
               login(request,user)
               messages.success(request,"Login Successful")
               return redirect("/")             
    return render(request,'fnlogin.html')

def fnlogout(request):
    logout(request)
    messages.success(request,"Logout")
    return redirect('/')


def collection(request):
    category=Category.objects.filter(status=0)
    context={"category":category}
    return render(request,'collection.html',context)

def collectionview(request,slug):
    if(Category.objects.filter(name=slug,status=0)):
       product=Product.objects.filter(category__name=slug)
       context={"product":product,"category":slug}
       return render(request,'collectionview.html',context)
    else:
        messages.warning(request,"No such Category Found")
        return redirect('/collection')

def collectiondetail(request,slugc,slugp):
    if (Category.objects.filter(name=slugc,status=0)):
        if (Product.objects.filter(name=slugp,status=0)):
            product=Product.objects.filter(name=slugp).first()
            context={"product":product}
            return render(request,'collectiondetail.html',context)
        else:
            messages.warning(request,"No such product found") 
            return redirect('/collection')     
    else:
        messages.warning(request,"No such category found")
        return redirect('collection')
    
def addtocart(request):
    if request.headers.get('x-requested-with')=='XMLHttpRequest':
       if request.user.is_authenticated:
           data=json.load(request)
           product_qty=data['product_qty']
           product_id=data['pid']
           product_status=Product.objects.get(id=product_id)
           if product_status:
               if Cart.objects.filter(user=request.user.id,product_id_id=product_id):
                   return JsonResponse({'status':'Product Already in cart'},status=200)
               else:
                   if product_status.quantity>=product_qty:
                       Cart.objects.create(user=request.user,product_id_id=product_id,product_quantity=product_qty)
                       return JsonResponse({'status':'Product Add To Cart'},status=200)
                   else:
                       return JsonResponse({'status':'Product stock not available'},status=200)
       else:
           return JsonResponse({'status':'Login to Add Cart'},status=200)
    else:
        return JsonResponse({'status':'Invalid Access'},status=200)      
    
def cartpage(request):
    if request.user.is_authenticated:
        cart=Cart.objects.filter(user=request.user)
        context={"cart":cart}
        return render(request,'cartpage.html',context)
    else:
        messages.warning(request,"Login to see Cart")
        return redirect("/")    
    
def removecart(request,id):
    cart=Cart.objects.get(id=id)
    cart.delete()
    return redirect("/cartpage")   

def favourite(request):
    if request.headers.get('x-requested-with')=='XMLHttpRequest':
       if request.user.is_authenticated:
           data=json.load(request)
           product_id=data['pid']
           product_status=Product.objects.get(id=product_id)
           if product_status:
               if Favourite.objects.filter(user=request.user.id,product_id_id=product_id):
                   return JsonResponse({'status':'Product Already in Favourite'},status=200)
               else:
                    Favourite.objects.create(user=request.user,product_id_id=product_id)     
                    return JsonResponse({'status':'Product Add to Favourite'},status=200)             
       else:
           return JsonResponse({'status':'Login to Add Favourite'},status=200)
    else:
        return JsonResponse({'status':'Invalid Access'},status=200)    

def favouritepage(request):
    if request.user.is_authenticated:
        fav=Favourite.objects.filter(user=request.user)
        context={"favourite":fav}
        return render(request,'favouritepage.html',context) 
    else:
        messages.warning(request,"Login to see Favourite")
        return redirect("/")
    
def removefavourite(request,id):
    favourite=Favourite.objects.get(id=id)
    favourite.delete()
    return redirect("/favouritepage")    

def search(request):
    if request.method=='GET':
        sname=request.GET.get('insearch')
        if (Category.objects.filter(name=sname)):
           category=Category.objects.filter(name=sname).first()
           print(f"/collectionview/{category.name}")
           return redirect(f"/collectionview/{category.name}")
        elif(Product.objects.filter(name=sname)):
            product=Product.objects.filter(name=sname).first()
            print(f"collectiondetail/{product.category}/{product.name}")
            return redirect(f"collectiondetail/{product.category}/{product.name}")
        else:
            messages.warning(request,"Product Not Found")
            return redirect("/collection")
    return redirect("/")   

def buy(request):
    cart=Cart.objects.filter(user=request.user)
    cart.delete()
    return redirect("/")

    