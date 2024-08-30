from functools import wraps
from django.shortcuts import render
from banks.models import Bank

def owner(view_fun):
 @wraps(view_fun)
 def _wrap_view(request,*args, **kwargs):
  user=request.user
  banks=Bank.objects.filter(admin = user)
  return view_fun(request,*args, **kwargs, banks=banks)
 
 return _wrap_view