from django.urls import path
from . import views

urlpatterns = [
    path('dumps/', views.dump),
    path('stats/', views.stat),
    path('about/', views.about),
]
