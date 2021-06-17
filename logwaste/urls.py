from django.urls import path
from . import views

urlpatterns = [
    path('logins/', views.logins),
    path('ewastes/', views.ewastes),
    path('picked/', views.picked),
    path('signup/', views.signup),
    path('profile/', views.profile),
    path('logout/', views.user_logout, name='logout'),
    path('edit/', views.edit, name='edit'),
    path('delete_id/', views.delete_id, name='delete'),
    path('delwaste/<int:id>/', views.ewaste_handle, name='delwaste')
]
