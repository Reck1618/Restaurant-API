from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.CategoriesView.as_view()),
    path('categories/<int:pk>', views.SingleCategoriesView.as_view()),
    path('menu-item/', views.MenuItemView.as_view()),
    path('menu-item/<int:pk>/', views.SingleMenuItemView.as_view()),
    path('cart/menu-item/', views.CartView.as_view()),
]