from django.urls import path
from . import views

urlpatterns = [
   
    path('', views.print, name='Numbers-result'),
    # path('print/', views.print, name='print'),
    
    

]