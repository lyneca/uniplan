from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.auth_login, name='login'),
    path('logout', views.auth_logout, name='logout'),
    path('register', views.auth_register, name='register'),
    path('add_unit', views.add_unit, name='add_unit'),
    path('remove_unit', views.remove_unit, name='remove_unit'),
    path('generate_calendar', views.generate_calendar, name='generate_calendar'),
    path('num_users', views.num_users, name='num_users'),
]
