from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),

    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),

    path('book-add/', views.book_add, name='book_add'),
    path('book-edit/<int:book_id>/', views.book_edit, name='book_edit'),
    path('book-delete/<int:book_id>/', views.book_delete, name='book_delete'),
]
