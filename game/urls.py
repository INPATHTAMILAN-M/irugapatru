
from django.urls import path
from . import views

urlpatterns = [
   path('',views.new_landing,name='landing'),
   path('check_game_slug/<str:slug>/',views.check_game_slug,name='check_game_slug'),
   path('home/',views.home,name='home'),
   path('game/<str:slug>/',views.game,name='game'),  
   path('new_landing',views.new_landing,name='new_landing'), 
   path('join',views.landing,name='join_and_register'),   
   path('check_first_round',views.cfr,name='cfr'),
]
