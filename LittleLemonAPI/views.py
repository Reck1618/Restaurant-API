from datetime import date
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
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

    # Overriding default Pagination Class
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

    # Update FilterSet so that it can also take str(category name) as input
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


class CartView(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsCustomer]

    def get_queryset(self):
        return Cart.objects.all().filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        try:
            id = request.data['menu_item']
            quantity = 1 if 'quantity' not in request.data else request.data['quantity']
        except KeyError:
            return Response({"message": "Missing 'menu_item' or 'quantity' in request data"}, status=status.HTTP_400_BAD_REQUEST)

        item = get_object_or_404(MenuItem, pk=id)
        price = int(quantity) * item.price

        existing_cart_item = Cart.objects.filter(user=request.user, menu_item=item).first()
        if existing_cart_item:
            # Item already exists, update its quantity and price
            existing_cart_item.quantity += int(quantity)
            existing_cart_item.price += price
            existing_cart_item.save()
            return Response({"message": "Item already exists in cart and it's quantity has been updated"}, status=status.HTTP_200_OK)

        try:
            Cart.objects.create(user=request.user, quantity=quantity, unit_price=item.price, price=price,
                             menu_item=item)
        except IntegrityError as e:
            return Response({"message": e}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "Item added to cart"},status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        if 'menu_item' in request.data:
            item = get_object_or_404(MenuItem, pk=request.data['menu_item'])
            cart_item = Cart.objects.filter(user=request.user, menu_item=item).first()
            if cart_item:
                cart_item.delete()
                return Response({"message": "Item deleted from cart"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Item not found in cart"}, status=status.HTTP_404_NOT_FOUND)
        else:
            Cart.objects.filter(user=request.user).delete()
            return Response({"message": "Cart cleared"}, status=status.HTTP_200_OK)

class OrderView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.groups.filter(name='Manager').exists():
            return Order.objects.all()
        elif self.request.user.groups.filter(name='Customer'):
            return Order.objects.all().filter(user=self.request.user)
        elif self.request.user.groups.filter(name='Delivery Crew').exists():
            return Order.objects.all().filter(delivery_crew=self.request.user)
        else:
            return Order.objects.none()

    def check_permissions(self, request):
        if request.method in ['GET']:
            self.permission_classes = [IsAuthenticated]
        elif request.method in ['POST']:
            self.permission_classes = [IsCustomer]
        return super().check_permissions(request)

    def post(self, request):
        items = Cart.objects.all().filter(user=self.request.user)
        if items.count() == 0:
            return Response({"message": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

        total_price = sum(item.price for item in items)

        order = Order.objects.create(user=self.request.user, status=False, total=total_price, date=date.today())

        for item in items.values():
            OrderItem.objects.create(
                order=order,
                menu_item = MenuItem.objects.get(pk=item['menu_item_id']),
                quantity = item['quantity'],
                price = item['price']
            )
        items.delete()
        return Response({"message": "Order placed successfully"}, status=status.HTTP_201_CREATED)

class SingleOrderView(generics.ListCreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer


    def check_permissions(self, request):
        if request.method in ['GET']:
            self.permission_classes = [IsAuthenticated]
        elif request.method in ['PUT', 'DELETE']:
            self.permission_classes = [IsAuthenticated, IsManager | IsAdminUser]
        else:
            self.permission_classes = [IsDeliveryCrew | IsAdminUser | IsManager]
        return super().check_permissions(request)

    def get_queryset(self):

        if Order.objects.get(pk=self.kwargs['pk']):
            queryset = OrderItem.objects.filter(order_id=self.kwargs['pk'])
            return queryset
        else:
            return Response({"message": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, *args, **kwargs):
        order = Order.objects.get(pk=self.kwargs['pk'])
        if order:
            order.status = not order.status
            order.save()
            return Response({"message": f"Order status updated #Status of #{order.id} changed to {order.status} "}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Order not found"}, status=status.HTTP_404_NOT_FOUND)