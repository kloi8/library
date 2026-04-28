from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('m/<int:pk>/', views.material_view, name='material_view'),
    path('add/', views.add_material, name='add_material'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]
