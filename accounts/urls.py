from django.contrib import admin
from django.urls import path
from . import views

app_name = 'accounts'


urlpatterns = [
    path('accounts' ,views.accounts , name='accounts'),
    path('signup' ,views.signup , name='signup'),
    path('signout' ,views.signout , name='signout'),
    path('signin' ,views.signin , name='signin'),
    path('signout_html' ,views.signout_html , name='signout_html'),
    path('reset' ,views.reset , name='reset'),
    path('activate/<uidb64>/<token>', views.activate, name = 'activate'),
]

