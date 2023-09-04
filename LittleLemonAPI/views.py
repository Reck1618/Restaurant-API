from rest_framework import generics, viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .serializers import CartSerializer, CategorySerializer, OrderItemSerializer, OrderSerializer, UserSerializer, MenuItemSerializer
from .models import Cart, Category, Order, OrderItem, MenuItem
from django.contrib.auth.models import User, Group
from django.core.paginator import Paginator
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from .pagination import LargeResultsSetPagination, StandardResultsSetPagination


# Create your views here.
class CategoriesView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    # Adding Pagination
    pagination_class = LargeResultsSetPagination

    # Request Throttling
    throttle_classes = [UserRateThrottle]