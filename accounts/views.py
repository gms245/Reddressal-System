from django.shortcuts import render,redirect
import datetime, random, hashlib
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
    )
from .models import UserProfile
from .forms import LoginUserForm,RegistrationForm
# from p2p_chat import *

@login_required(login_url='accounts:login')
def home_student(request):
    User = UserProfile.objects.get(user=request.user)
    if User.typ == "Student":
            app_qs = User.application_set.all()
            return render(request,'student/student.html',{'app_qs':app_qs})
    return redirect('accounts:login')

@login_required(login_url='accounts:login')
def home_staff(request):
    User = UserProfile.objects.get(user=request.user)
    if User.typ == "Staff":
        return render(request,'staff.html',{})
    return redirect('accounts:login')

def register(request):
    if request.user.is_authenticated():
        return redirect('accounts:login')
    form = RegistrationForm(request.POST or None)
    if form.is_valid():
        new_data = request.POST.copy()                                                                                                                                      
        new_user = form.save(new_data)                                                                                                                    
        salt = hashlib.sha1(str(random.random()).encode('utf-8')).hexdigest()[:5]
        activation_key = hashlib.sha1((salt+new_user.username).encode('utf-8')).hexdigest()                                                                                                                
        new_profile = UserProfile(user=new_user,
                                      activation_key=activation_key,
                                      typ='Student',dep='None',pos='None')
        new_profile.save()                                                                                                      
        email_subject = 'Your CGRS account confirmation'
        email_body = """Hello, %s, and thanks for signing up\n\nTo activate your account, click this link 
                        \n\nhttp://192.168.0.103:8000/confirm/%s""" % (
                									new_user.first_name,
                									new_profile.activation_key
                									)
        send_mail(email_subject,
                      email_body,
                      settings.EMAIL_HOST_USER,
                      [new_user.email])
        messages.success(request,'Verification email has been sent to your email id')
        return redirect('accounts:login')
    return render(request,'accounts/register.html', {'form': form})

def confirm(request, activation_id):
    if request.user.is_authenticated():
        return redirect('accounts:login')
    user_profile = get_object_or_404(UserProfile,
                                     activation_key=activation_id)
    # if user_profile.key_expires < datetime.datetime.today():
        # pass                 # do something
    user_account = user_profile.user
    user_account.is_active = True
    user_account.save()
    return redirect('accounts:login')

def Login(request):
    if request.user.is_authenticated():
        user_=UserProfile.objects.get(user=request.user)
        if user_.typ=="Student":
            return redirect('accounts:home_student')
        elif user_.typ=="Staff":
            return redirect('accounts:home_staff')
    form = LoginUserForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username,password=password)
        if user.is_active == True:
            login(request,user)
            user_a=UserProfile(user=request.user)
            if user_a.typ == "Student":
                return redirect('accounts:home_student')
            else:
                return redirect('accounts:home_staff')
        else:
            messages.success(request,'You are not a active user. To activate account click the link int mail sent to emailid')
            return redirect('accounts:login')
    return render(request,'accounts/login.html', {'form': form})

def Logout(request):
    logout(request)
    messages.success(request,'You have been successfully logged out')
    return redirect('accounts:login')

def chat(request):
    root = tk.Tk()
    p2p_chat = P2pChat(master=root)
    p2p_chat.mainloop()
    return redirect('accounts:login')