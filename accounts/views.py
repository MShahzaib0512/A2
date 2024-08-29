from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login , logout
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode , urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .tokens import generate_token
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from A2 import settings
from django.contrib.auth.decorators import login_required
from banks.models import Bank
from django.views.decorators.http import require_POST


# Create your views here.

def accounts(request):
 return render(request , 'accounts.html')
@require_POST
def submit_signup(request):
#  if request.method == 'POST':
  uname = request.POST['uname']
  fname = request.POST['fname']
  lname = request.POST['lname']
  email = request.POST['email']
  pass1 = request.POST['pass1']
  pass2 = request.POST['pass2']
  
  if User.objects.filter(username = uname):
   messages.error(request,'A user with that username already exists')
   return redirect('accounts:signup')
  elif User.objects.filter(email = email):
   messages.error(request,'Email alraedy exist')
   return redirect('accounts:signup')
  elif pass1 != pass2:
   messages.error(request,"The two password fields didn't match")
   return redirect('accounts:signup')
  elif len(str(pass1)) < 8:
   messages.error(request,'This password is too short. It must contain at least 8 characters')
   return redirect('accounts:signup')
  elif not uname.isalnum():
   messages.error(request,'Username should only contain Alphabets and numbers')
   return redirect('accounts:signup')
  else:
   myuser = User.objects.create_user(uname, email, pass1)
   myuser.first_name = fname
   myuser.last_name = lname
   myuser.is_active = False
   myuser.save()
   
  #  confermation Email
   site = get_current_site(request)
    
   subject = "Confirm your E-mail Address"
   message = render_to_string('confermation_Email.html',{
      'user' : myuser.first_name,
      'domain':site.domain,
      'uid' : urlsafe_base64_encode(force_bytes(myuser.pk)),
      'token': generate_token.make_token(myuser),
    })
   from_mail = settings.EMAIL_HOST_USER 
   to_list = [myuser.email]
   send_mail(subject, message, from_mail, to_list, fail_silently = True)
   messages.info(request, "Your account have been created successfully conferm yoyr email to activate your account ")
   return redirect('accounts:signin')
def signup(request):
  return render (request,'signup.html')
@require_POST
def submit_signin(request):
  uname=request.POST['uname']
  pass1=request.POST['pass1']
  user=authenticate(username=uname,password=pass1)
  if user is not None:
   site=get_current_site(request)
   Subject="Authentication E-mail"
   message=render_to_string('authentication_mail.html',{
     'user':user.first_name,
     'domain':site.domain,
     'uid':urlsafe_base64_encode(force_bytes(user.pk)),
     'token':default_token_generator.make_token(user),
   })
   from_mail=settings.EMAIL_HOST_USER
   to_user=[user.email]
   send_mail(Subject,message,from_mail,to_user,fail_silently=True)
   messages.info(request,'An Email was send to your email please confirm that its you try to login')
   return render(request,'signin.html')
  else:
   messages.error(request,'Username or password is invalid')
   return redirect('accounts:signin')
def signin(request):
  return render(request, 'signin.html')
def signout(request):
 logout(request)
 banks = Bank.objects.all()
 return render(request , 'index.html',{'banks':banks})
def activate(request, uidb64, token):
  try:
    uid = force_str(urlsafe_base64_decode(uidb64))
    myuser = User.objects.get(pk = uid)
  except(TypeError ,ValueError ,User.DoesNotExist):
    myuser = None
    
  if myuser is not None and generate_token.check_token(myuser , token):
    myuser.is_active=True
    myuser.save()
    return redirect('accounts:signin')
  else:
    return render(request ,'activation_failed.html')
def password_reset_complete(request):
  return render(request , 'password_reset_complete.html')
@login_required
@require_POST
def submit_reset(request):
    user = request.user
    uname = request.POST['uname']
    pass1 = request.POST['pass1']
    if len(str(pass1)) < 8 :
      messages.error(request, 'password must contain 8 charcaters')
      return redirect('accounts:reset')
    elif user.username != uname:
      messages.error(request,'Enter the valid username')
      return redirect('accounts:reset')
    else:
      try:
        user = User.objects.get(username = uname)
        user.set_password(pass1)
        user.save()
        messages.success(request, "Password have been changed successfully")
        return redirect('accounts:signin')
      except:
        messages.error(request, 'Username is in-correct')
        return redirect('accounts:reset')
@login_required 
def reset(request):
  return render(request,'reset.html')
@login_required
def signout_html(request):
  user = request.user
  banks= Bank.objects.filter(admin = user)
  return render(request, 'signout.html',{'banks':banks})  
def user_activate(request,uidb64,token):
  try:
    uid=urlsafe_base64_decode(force_str(uidb64))
    user=User.objects.get(pk=uid)
  except(TypeError,ValueError,User.DoesNotExist):
    user=None
    
  if user is not None and default_token_generator.check_token(user,token):
    login(request,user)
    return redirect('accounts:signout_html')
  else:
    return render(request,'activation_failed.html')
    