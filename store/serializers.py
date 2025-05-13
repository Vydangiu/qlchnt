from rest_framework import serializers
from .models import  Category, Product, Cart, CartItem
from users.models import User 
from store.models import Product
from store.models import Order 
from store.models import OrderItem, CartItem, ProductImage

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    def get_image_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.image.url)

    class Meta:
        model = ProductImage
        fields = ['id', 'product', 'image_url']

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'category', 'name', 'description', 'price', 'stock', 'discount', 'created_at', 'updated_at', 'images']

class ProductInlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price']

class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source="product.name")

    class Meta:
        model = CartItem
        fields = ["id", "cart", "product", "product_name", "quantity"]

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ["id", "user", "created_at", "items", "total_price"]

    def get_total_price(self, obj):
        return obj.total_price()




class OrderItemReadSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)  # Trả về chi tiết sản phẩm

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price']

class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    quantity = serializers.IntegerField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'price']

# class OrderSerializer(serializers.ModelSerializer):
#     user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
#     shipping_address = serializers.CharField()
#     payment_method = serializers.ChoiceField(choices=Order.PAYMENT_CHOICES, default='cod')
#     items = OrderItemSerializer(many=True)
#     total_price = serializers.DecimalField(max_digits=10, decimal_places=2)

#     class Meta:
#         model = Order
#         fields = ['id', 'user', 'shipping_address', 'payment_method', 'items', 'total_price', 'status', 'created_at']

#     def validate_shipping_address(self, value):
#         if not value.strip():
#             raise serializers.ValidationError("This field is required.")
#         return value

#     def create(self, validated_data):
#         items_data = validated_data.pop('items')
#         order = Order.objects.create(**validated_data)
#         for item_data in items_data:
#             OrderItem.objects.create(order=order, **item_data)
#         return order


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    shipping_address = serializers.CharField()
    phone_number = serializers.CharField()  # Đảm bảo rằng trường phone_number có mặt trong serializer
    payment_method = serializers.ChoiceField(choices=Order.PAYMENT_CHOICES, default='cod')
    items = OrderItemSerializer(many=True)  # Dùng cho write (POST)
    items_detail = OrderItemReadSerializer(many=True, read_only=True, source='items')  # Dùng cho read (GET)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = Order
        fields = ['id', 'user', 'shipping_address', 'phone_number', 'payment_method', 'items', 'items_detail', 'total_price', 'status', 'created_at']

    def validate_shipping_address(self, value):
        if not value.strip():
            raise serializers.ValidationError("This field is required.")
        return value

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order



class CheckoutSerializer(serializers.Serializer):
    shipping_address = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)  
    payment_method = serializers.ChoiceField(choices=Order.PAYMENT_CHOICES, required=True)
    product_id = serializers.IntegerField(required=False)
    quantity = serializers.IntegerField(required=False, default=1)

    def validate(self, data):
        user = self.context['request'].user
        if not data.get('product_id') and not CartItem.objects.filter(cart__user=user).exists():
            raise serializers.ValidationError("Giỏ hàng đang trống và không có product_id!")
        return data

    def create(self, validated_data):
        request = self.context['request']
        user = request.user
        cart_items = []

        product_id = validated_data.get('product_id')
        if product_id:
            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                raise serializers.ValidationError({"product_id": "Sản phẩm không tồn tại."})
            cart_items = [CartItem(cart=None, product=product, quantity=validated_data.get('quantity', 1))]
        else:
            try:
                cart = Cart.objects.get(user=user)
            except Cart.DoesNotExist:
                raise serializers.ValidationError("Không tìm thấy giỏ hàng của người dùng.")
            cart_items = list(CartItem.objects.filter(cart=cart))

        total_price = sum(item.quantity * item.product.price for item in cart_items)

        order = Order.objects.create(
            user=user,
            shipping_address=validated_data['shipping_address'],
            phone_number=validated_data['phone_number'],
            payment_method=validated_data['payment_method'],
            total_price=total_price
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        if not product_id:
            CartItem.objects.filter(cart__user=user).delete()

        return order


class CheckoutSerializer(serializers.Serializer):
    shipping_address = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)  
    payment_method = serializers.ChoiceField(choices=Order.PAYMENT_CHOICES, required=True)
    product_id = serializers.IntegerField(required=False)
    quantity = serializers.IntegerField(required=False, default=1)

    def validate(self, data):
        user = self.context['request'].user
        if not data.get('product_id') and not CartItem.objects.filter(cart__user=user).exists():
            raise serializers.ValidationError("Giỏ hàng đang trống và không có product_id!")
        return data

    def create(self, validated_data):
        request = self.context['request']
        user = request.user
        cart_items = []

        product_id = validated_data.get('product_id')
        if product_id:
            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                raise serializers.ValidationError({"product_id": "Sản phẩm không tồn tại."})
            cart_items = [CartItem(cart=None, product=product, quantity=validated_data.get('quantity', 1))]
        else:
            try:
                cart = Cart.objects.get(user=user)
            except Cart.DoesNotExist:
                raise serializers.ValidationError("Không tìm thấy giỏ hàng của người dùng.")
            cart_items = list(CartItem.objects.filter(cart=cart))

        total_price = sum(item.quantity * item.product.price for item in cart_items)

        # Tạo đơn hàng
        order = Order.objects.create(
            user=user,
            shipping_address=validated_data['shipping_address'],
            phone_number=validated_data['phone_number'],
            payment_method=validated_data['payment_method'],
            total_price=total_price
        )

        # Tạo các items trong đơn hàng
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        # Xóa các mục trong giỏ hàng nếu không có sản phẩm id
        if not product_id:
            CartItem.objects.filter(cart__user=user).delete()

        return order
