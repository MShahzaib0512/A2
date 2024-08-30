from django.contrib import admin
from django.urls import path
from . import views

app_name = 'accounts'


urlpatterns = [
    path('accounts' ,views.accounts , name='accounts'),
    path('signup' ,views.signup , name='signup'),
    path('submit_signup' ,views.submit_signup , name='submit_signup'),
    path('signout' ,views.signout , name='signout'),
    path('signin' ,views.signin , name='signin'),
    path('submit_signin' ,views.submit_signin , name='submit_signin'),
    path('signout_html' ,views.signout_html , name='signout_html'),
    path('reset' ,views.reset , name='reset'),
    path('submit_reset' ,views.submit_reset , name='submit_reset'),
    path('activate/<uidb64>/<token>', views.activate, name = 'activate'),
    path('user_activate/<uidb64>/<token>', views.user_activate, name = 'user_activate'),
    
    path('password_reset/', views.password_reset, name='password_reset'),
    path('password_reset/done/', views.password_reset_done, name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
    path('reset/done/', views.password_reset_complete, name='password_reset_complete'),
]

