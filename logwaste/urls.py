from django.urls import path
from . import views

urlpatterns = [
    path('logins/', views.logins),
    path('ewastes/', views.ewastes),
    path('signup/', views.signup),
    path('profile/', views.profile),
    path('logout/', views.user_logout, name='logout')
]
