from rest_framework import generics, viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .serializers import CartSerializer, CategorySerializer, OrderItemSerializer, OrderSerializer, UserSerializer, MenuItemSerializer
from .models import Cart, Category, Order, OrderItem, MenuItem
from django.contrib.auth.models import User, Group
from django.core.paginator import Paginator
from .permissions import IsCustomer, IsDeliveryCrew, IsManager
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from .pagination import LargeResultsSetPagination, StandardResultsSetPagination


# Create your views here.
class CategoriesView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    ordering_fields = ['title', 'slug']
    search_fields = ['title', 'slug']

    # Adding Large Pagination Class
    pagination_class = LargeResultsSetPagination

    # Check Permissions
    def check_permissions(self, request):
        if request.method in ['GET']:
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [IsManager | IsAdminUser]
        return super().check_permissions(request)


class SingleCategoriesView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    # Check Permissions
    def check_permissions(self, request):
        if request.method in ['GET']:
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [IsManager | IsAdminUser]
        return super().check_permissions(request)


class MenuItemView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    ordering_fields = ['title', 'price', 'featured', 'category']
    search_fields = ['title', 'price', 'featured']
    filterset_fields = ['title', 'price', 'featured']

    # Check Permissions
    def check_permissions(self, request):
        if request.method in ['GET']:
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [IsManager | IsAdminUser]
        return super().check_permissions(request)

    # Update FilterSet so that it can also take str as input
    def get_queryset(self):
        query_param_value = self.request.query_params.get('category')
        if query_param_value is not None:
            query_param_value.capitalize()
            try:
                category = Category.objects.get(pk=int(query_param_value))
            except ValueError:
                category = Category.objects.get(title=query_param_value)
            self.queryset = self.queryset.filter(category=category)
        return super().get_queryset()


class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    # Check Permissions
    def check_permissions(self, request):
        if request.method in ['GET']:
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [IsManager | IsAdminUser]
        return super().check_permissions(request)
