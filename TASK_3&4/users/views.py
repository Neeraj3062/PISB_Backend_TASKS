from django.shortcuts import render
from django.core.checks import messages
from django.db.models import Q
from django.shortcuts import redirect, render
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import extendeduser
import re


# VIEWS

def login(request):
    if request.method =='POST':
        user = auth.authenticate(username=request.POST['uname'],password=request.POST['pass'])
        if user is not None:
            auth.login(request,user)
            return redirect('home')
        else:
            return render (request, 'users/login.html',{'error':"Invaild Crededntials"})            
    else:
        return render(request,'users/login.html')      


def register(request):
    
    if request.method =='POST':
                  
            if request.POST['pass'] == request.POST['passwordagain']:
                
                try:
                    user = User.objects.get(username=request.POST['uname'])
                    return render(request,'users/register.html',{'error':"Username Already taken"})
                except User.DoesNotExist:                                
                    
                    first_name = request.POST['fn']
                    last_name = request.POST['ln']
                    place = request.POST['city']
                    phnum = request.POST['phone']
                    gender = request.POST['gen']
                    age = request.POST['age']
                    email = request.POST['email']

                if (len(request.POST['pass'])<8):
                    return render(request,'users/register.html',{'error':"Password too Short, Should Contain ATLEAST 1 Uppercase,1 lowercase,1 special Character and 1 Numeric Value"})

                elif not re.search(r"[\d]+",request.POST['pass']):
                    return render(request,'users/register.html',{'error':"Your Password must contain Atleast 1 Numeric "})

                elif not re.findall('[A-Z]', request.POST['pass']):   
                     return render(request,'users/register.html',{'error':"Your Password must contain Atleast 1 UpperCase Letter "})

                elif not re.findall('[a-z]',request.POST['pass']):
                    return render(request,'users/register.html',{'error':"Your Password must contain Atleast 1 lowercase Letter "})
                    
                elif not re.findall('[()[\]{}|\\`~!@#$%^&*_\-+=;:\'",<>./?]', request.POST['pass']):   
                     return render(request,'users/register.html',{'error':"Your Password must contain Atleast 1 Specail character "})     

                else:
                    if extendeduser.objects.filter(email=email):
                        return render(request,'users/register.html',{'error':"Email Already  Registered  "})
                    elif extendeduser.objects.filter(phone_num=phnum):
                        return render(request,'users/register.html',{'error':"Phone Number Already Registered"})

                    else:    
                        user = User.objects.create_user(username=request.POST['uname'],password=request.POST['pass'])                           
                        newextendeduser = extendeduser(first_name=first_name, last_name=last_name,phone_num=phnum,place=place,gender=gender,age=age,email=email,user=user)
                        newextendeduser.save()
                        auth.login(request, user)
                        messages.success(request, f'Your account has been Create!! Login Now')
                    

                    return redirect('login')
            else:
                return render(request,'users/register.html',{'error':"Password and Confirm Password Doesnt Match"})
             
    else:
           return render(request,'users/register.html')


@login_required(login_url='login')
def profile(request):
    datas = extendeduser.objects.filter(user = request.user)
    return render(request,'users/profile.html',{'data':datas})


def search(request):
    if request.method== 'POST':
        searched = request.POST['searched']
        res = extendeduser.objects.filter(Q(email__contains=searched )  |
                                                              Q(age__contains=searched )  |
                                                              Q(place__contains=searched)  |
                                                              Q(phone_num__contains=searched)   )

        if res:
            return render(request,'users/search.html',{'searched':searched ,'res':res})
        else: 
                 return render(request,'users/search.html',{'error':"No User FOund"})


    else:
     
        return render(request,'users/search.html')

def logout(request):
    auth.logout(request)
    return render(request,'users/logout.html')
            