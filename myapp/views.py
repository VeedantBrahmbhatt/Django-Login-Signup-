from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
# Create your views here.
# @login_required(login_url='login')
# def HomePage(request):
#     request.session.set_expiry(5)
#     return render(request,'home.html')
@login_required(login_url='login')
def HomePage(request):
    if request.user.is_authenticated:
        return render(request, 'home.html')
    else:
        return redirect('login')

def SignupPage(request):
    if request.method=='POST':
        user=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')
        if pass1!=pass2:
            return HttpResponse("Password Mismatch")
        my_user=User.objects.create_user(user,email,pass1)
        my_user.save()
        return redirect('login')
    return render (request,'signup.html')

def LoginPage(request):
    if request.method=="POST":
        user=request.POST.get('username')
        pass1=request.POST.get('pass')
        user_auth=authenticate(request,username=user, password=pass1)
        if user_auth is not None:
            login(request,user_auth)
            return redirect('home')
        else:
            return HttpResponse("Invalid Credentials.")
    return render(request,'login.html')
# def LoginPage(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(request, data=request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = authenticate(username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect ('home')
#     else:
#         form = AuthenticationForm()
#     if 'ession_expired' in request.GET:
#         message = 'Session expired. Please log in again.'
#     else:
#         message = ''
#     return render(request, 'login.html', {'form': form, 'essage': message})
def LogoutPage(request):
    logout(request)
    return redirect('login')