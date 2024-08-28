from django.contrib import admin
from .models import Branch, Bank
# Register your models here.
class MyBanks(admin.ModelAdmin):
 list_display=['name','description','inst_num','swift_code']
 search_fields=['bank_id']
 
admin.site.register(Bank, MyBanks)

class MyBranch(admin.ModelAdmin):
 list_display=['name','transit_num','address','email','capacity']
 search_fields=['branch_id']
 
admin.site.register(Branch , MyBranch)