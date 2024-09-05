from django.shortcuts import render,redirect,get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Bank,Branch
from django.views.decorators.http import require_POST
# Create your views here.
def index(request):
 bank = Bank.objects.all()
 return render(request,"index.html",{'banks':bank, 'content':request.show_registration_popup})
@login_required
@require_POST
def submit_Edit_branch(request,branch_id): 
  branch = get_object_or_404(Branch,branch_id=branch_id)
  if request.method=='POST':
    name = request.POST['name']
    transit_num = request.POST['transit_num']
    address = request.POST['address']
    email = request.POST['email']
    capacity = request.POST['capacity']
    
    branch.name=name
    branch.transit_num=transit_num
    branch.email=email
    branch.capacity=capacity
    branch.address=address
    branch.save()
    messages.success(request,"Branch data updated successfully")
    return render(request, 'Edit_branch.html',{'branch':branch})
@login_required
def Edit_branch(request,branch_id):
  branch = get_object_or_404(Branch,branch_id=branch_id)
  return render(request, "Edit_branch.html",{'branch':branch})
def about(request):
 return render(request, "about.html")
def accounts(request):
 return render(request, 'accounts.html')
@login_required
def view(request):
 user = request.user
 data = {
  'first_name' : user.first_name,
  'last_name' : user.last_name,
  'username' : user.username,
  'email' : user.email,
  'pk' : user.pk,
 }
 return JsonResponse(data)
@login_required
@require_POST
def submit_AddBank(request):
  user = request.user
  name = request.POST['name']
  description= request.POST['description']
  inst_num = request.POST['inst_num']
  swift_code = request.POST['swift_code']
  
  bank =Bank.objects.create(name = name, description=description ,inst_num=inst_num ,swift_code=swift_code,admin=user)
  bank.save()
  messages.success(request ,"bank has been created successfully")
  return redirect('banks:AddBank')
@login_required
def AddBank(request):
  return render(request,'AddBank.html')
@login_required
def user_view(request):
 return render(request, 'user_view.html')
@login_required
@require_POST
def submit_edit(request):
    user = request.user
    id = request.POST['id']
    uname = request.POST['uname']
    fname = request.POST['fname']
    lname = request.POST['lname']
    email = request.POST['email']
    
    user =User.objects.get(pk=id)
    user.first_name=fname
    user.last_name=lname
    user.email=email
    user.username=uname
    user.save()
    messages.success(request,"Data has been updated sucessfully")
    return redirect('banks:edit')
@login_required
def edit(request):
  user=request.user
  return render(request, 'edit.html' ,{'user': user})
@login_required
@require_POST
def addbranch(request): 
    name = request.POST['name']
    transit_num=request.POST['transit_num']
    address=request.POST['address']
    email=request.POST['email']
    capacity=request.POST['capacity']
    bank_id=request.POST['bank_id']
    bank_id1 = Bank.objects.get(bank_id=bank_id)
    branch=Branch.objects.create(name=name,transit_num=transit_num,address=address,email=email,capacity=capacity,bank=bank_id1)
    branch.save()
    messages.success(request,"Branch has been added successfully")
    return render(request,'addbranch.html',{'bank_id':bank_id})
@login_required
def Addbranch(request,bank_id):
  return render(request, "Addbranch.html", {'bank_id':bank_id})
def details(request,bank_id):
  bank=get_object_or_404(Bank,bank_id=bank_id)
  branch=bank.branches.all()
  return render(request, "details.html",{'bank':bank, 'branches':branch})