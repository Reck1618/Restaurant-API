from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.CategoriesView.as_view()),
    # path('menu-item/', views.MenuItemView.as_view()),
    # path('menu-item/<int:pk>/', views.SingleMenuItem.as_view()),
]