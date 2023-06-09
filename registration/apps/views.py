from django.shortcuts import render,HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm,SetPasswordForm,UserChangeForm
from . forms import UserRegistration,EditUserProfileForm,EditAdminProfileForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User

# User Sign Up Form
def show(request):
    if request.method=='POST':
        fm=UserRegistration(request.POST)
        if fm.is_valid():
            messages.success(request,'Thank you for submiting')
            fm.save()
    else:
        fm=UserRegistration()
    return render(request,'home.html',{'form':fm})

    
#User log In

def user_login(request):
    if not request.user.is_authenticated:
        if request.method=="POST":
            fm=AuthenticationForm(request=request,data=request.POST)
            if fm.is_valid():
                uname=fm.cleaned_data['username']
                upp=fm.cleaned_data['password']
                user=authenticate(username=uname,password=upp)
                if user is not None:
                    login(request,user)
                    messages.success(request,'Login Successfull')
                    return HttpResponseRedirect('/profile/')

        else:
            fm=AuthenticationForm()
        return render(request,'login.html',{'form':fm})
    else:
        return HttpResponseRedirect('/profile/')


#User Profile Pages Redirect
def profile(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            if request.user.is_superuser==True:
                fm=EditAdminProfileForm(request.POST,instance=request.user)
                users=User.objects.all()
            else:
                fm=EditUserProfileForm(request.POST,instance=request.user)
            if fm.is_valid():
                messages.success(request,'Profile Update')
                fm.save()
        else:
            if request.user.is_superuser==True:
                fm=EditAdminProfileForm(instance=request.user)
                users=User.objects.all()
            else:
                 fm=EditUserProfileForm(instance=request.user)
                 users=None
        return render(request,'profile.html',{'name':request.user,'form':fm,'users':users})
    else:
        return HttpResponseRedirect('/login/')


# User Log Out 
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/login/')

   
#User ChangePassword whth old password
def user_changepass(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            fm=PasswordChangeForm(user=request.user , data=request.POST)
            if fm.is_valid():
                fm.save()
                return HttpResponseRedirect('/profile/')
        else:
            fm=PasswordChangeForm(user=request.user)
        return render (request,'change.html',{'form':fm})
    else:
        return HttpResponseRedirect('/login/')


#change password without old password
def user_changepass1(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            fm=SetPasswordForm(user=request.user , data=request.POST)
            if fm.is_valid():
                fm.save()
                return HttpResponseRedirect('/profile/')
        else:
            fm=SetPasswordForm(user=request.user)
        return render (request,'change.html',{'form':fm})
    else:
        return HttpResponseRedirect('/login/')

def userdet(request,id):
    if request.user.is_authenticated:
        pi=User.objects.get(pk=id)
        fm=EditAdminProfileForm(instance=pi)
        return render(request,'userdetail.html',{'form':fm})
    else:
        return HttpResponseRedirect('/login/')
