
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Product, Order, OrderItem


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        return user


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "price"]


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderItem
        fields = ["product", "quantity", "price"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ["id", "user", "total_price", "created_at", "items"]
        read_only_fields = ["user", "total_price", "created_at"]


class OrderCreateSerializer(serializers.Serializer):
    products = serializers.ListField(
        child =serializers.DictField (child=serializers.IntegerField())
    )

    def create(self, validated_data):
        user = self.context["request"].user
        products_data = validated_data.pop("products")
        order = Order.objects.create(user=user)
        total_price = 0

        for item in products_data:
            product_id = item.get("product_id")
            quantity = item.get("quantity")
            product = Product.objects.get(id=product_id)
            price = product.price * quantity

            OrderItem.objects.create(
                order=order, product=product, quantity=quantity, price=price
            )
            total_price += price

        order.total_price = total_price
        order.save()
        return order
