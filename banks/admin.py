from django.contrib import admin
from .models import Branch, Bank
# Register your models here.
class MyBanks(admin.ModelAdmin):
 list_display=['name','description','inst_num','swift_code','admin']
 search_fields=['inst_num']
 
admin.site.register(Bank, MyBanks)

class MyBranch(admin.ModelAdmin):
 list_display=['name','email']
 search_fields=['name']
 
admin.site.register(Branch , MyBranch)