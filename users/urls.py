from django.urls import path
from .views import dashboard_view, login_view, logout_view

urlpatterns = [
    path('dashboard/', dashboard_view, name='dashboard'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]
