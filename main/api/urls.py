from django.urls import path,include
from . import views

urlpatterns = [
    path('scanReader/', views.card_scan_reader, name='scanReader'),
    path('', views.info, name='info')
]