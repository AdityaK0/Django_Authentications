from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,authenticate,logout


# Create your views here.




def home(request):
    return render(request,'home.html')

def login_user(request):
    try :
        phone = None
        if request.method == "POST":
            
            username = request.POST.get("first")
            password = request.POST.get("password")
            print("GOT BOTH DATA ",username,password)
            if not all([username,password]):
                return HttpResponse({"message":"please provide full details"})
            
            if str(username).isdigit() and len(username)==10:
                print("Phone number")
                user_profile = Profile.objects.get(phonenumber=username)
                print(user_profile,"MAN")
                username = User.objects.get(id=user_profile.user_id)
            
            user = authenticate(request,username=username,password=password)
            
            if user:
                login(request,user)
                return redirect('home')
            else:
                return HttpResponse({"invalid":"wrong credentials"})
            
        return render(request,'login.html')

    except Exception as e :
        return HttpResponse("Error Occured =: ",e)

def register(request):
    try :
        if request.method == "POST":
            username = request.POST.get("username")
            email = request.POST.get("email")
            fullname = request.POST.get("fullname")
            password = request.POST.get("password")
            phonenumber = request.POST.get("phonenumber")
            
            if not all([username,email,fullname,phonenumber]):
                return HttpResponse({"message":"please provide full details"})
            
            user = User.objects.create_user(username=username,email=email,password=password)
            user.save()
            
            if user:
                user_profile = Profile.objects.create(user=user,fullname=fullname,phonenumber=phonenumber)
                user_profile.save()
                return redirect('login')
            
        return render(request,'register.html')

    except Exception as e :
        print(e)
        return HttpResponse("Error Occured =: ",str(e))
    
def logout_user(request):
        logout(request)
        return redirect('login')
    
@login_required()    
def userlist(request):
    users = User.objects.all()
    return render(request,'userlist.html',{'users':users})    