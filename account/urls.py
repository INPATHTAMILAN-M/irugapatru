
from django.urls import path, re_path
from . import views

urlpatterns = [
    path('signup',views.signup,name='signup'),  
    path('login/',views.customlogin, name='login'),
    path('logout/',views.logout, name="logout"),
    re_path(r'^google-login/$', views.google_login, name="google_login"), 
    path('add_gender/',views.add_gender, name="add_gender"),
    path('terms_and_conditions/',views.terms_and_conditions, name="terms_and_conditions"),
    path('privacy-policy/',views.privacy_policy, name="privacy_policy"),
]
