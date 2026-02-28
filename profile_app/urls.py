from django.urls import path
from . import views

app_name = 'profile_app'

urlpatterns = [
    path('', views.profile_view, name='main'),
    path('buy/<slug:item_slug>/', views.buy_item, name='buy'),
    path('toggle/<slug:item_slug>/', views.toggle_item, name='toggle'),
]
