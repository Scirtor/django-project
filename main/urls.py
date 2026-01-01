from django.urls import path
from .views import home, register, add_item, logout_view
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', logout_view, name='logout'),
    path('add/', add_item, name='add_item'),
]
