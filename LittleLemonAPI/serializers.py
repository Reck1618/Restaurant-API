from rest_framework import serializers
from django.contrib.auth.models import User
from django.utils.text import slugify
from .models import Category, MenuItem, Cart, Order, OrderItem

class CategorySerializer(serializers.ModelSerializer):
    slug = serializers.SerializerMethodField(method_name='get_slug', read_only=True)
    class Meta:
        model = Category
        fields = ['id', 'title', 'slug']

    def get_slug(self, category: Category):
        return slugify(category.title)

class MenuItemSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset = Category.objects.all()
    )
    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'category', 'featured']

class CartSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset = User.objects.all(),
        default = serializers.CurrentUserDefault()
    )
    class Meta:
        model = Cart
        fields = ['user', 'menu_item', 'quantity', 'price']

    def validate(self, attrs):
        attrs['unit_price'] = attrs['menu_item'].price
        attrs['price'] = attrs['unit_price'] * attrs['quantity']
        return attrs

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'menu_item', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    order_item = OrderItemSerializer(many=True, read_only=True, source='order')
    class Meta:
        model = Order
        fields = ['id', 'user', 'delivery_crew', 'status', 'total', 'order_item']


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'email']