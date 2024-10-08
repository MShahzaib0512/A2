from django.urls import path
from .views import *

app_name = 'banks'

urlpatterns = [
    path('',index, name="index"),
    path('about',about, name="about"),
    path('view',view, name="view"),
    path('accounts',accounts, name="accounts"),
    path('details/<int:bank_id>',details, name="details"),
    path('Edit_branch/<int:branch_id>',Edit_branch, name="Edit_branch"),
    path('submit_Edit_branch/<int:branch_id>',submit_Edit_branch, name="submit_Edit_branch"),
    path('user_view',user_view, name="user_view"),
    path('AddBank',AddBank, name="AddBank"),
    path('submit_AddBank',submit_AddBank, name="submit_AddBank"),
    path('addbranch',addbranch, name="addbranch"),
    path('Addbranch/<bank_id>',Addbranch, name="Addbranch"),
    path('edit',edit, name="edit"),
    path('submit_edit',submit_edit, name="submit_edit"),
    
]