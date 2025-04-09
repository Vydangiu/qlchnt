from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import viewsets, status
from .models import User
from .serializers import UserSerializer
from .models import Category, Product, ProductImage
from .serializers import CategorySerializer, ProductSerializer, ProductImageSerializer
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from store.models import Order  
from store.serializers import OrderSerializer , CheckoutSerializer
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    @action(detail=True, methods=['patch'])
    def update_category(self, request, pk=None):
        """ Cập nhật danh mục """
        category = self.get_object()
        serializer = self.get_serializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Cập nhật danh mục thành công", "data": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'])
    def delete_category(self, request, pk=None):
        """ Xóa danh mục """
        category = self.get_object()
        category.delete()
        return Response({"message": "Xóa danh mục thành công"}, status=status.HTTP_204_NO_CONTENT)

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Q
from .models import Product
from .serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Chỉ user đăng nhập mới có thể sửa / xóa
    authentication_classes = [JWTAuthentication]  # Xác thực bằng Token JWT

    # @action(detail=False, methods=['get'], url_path='category/(?P<category_id>[^/.]+)')
    # def list_by_category(self, request, category_id=None):
    #     """ Lấy danh sách sản phẩm theo danh mục """
    #     products = Product.objects.filter(category_id=category_id)
    #     serializer = self.get_serializer(products, many=True)
    #     return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        queryset = self.queryset

        search_query = request.query_params.get("search", "")
        category = request.query_params.get("category")
        min_price = request.query_params.get("min_price")
        max_price = request.query_params.get("max_price")

        if search_query:
            queryset = queryset.filter(name__icontains=search_query)
        if category:
            queryset = queryset.filter(category_id=category)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='search')
    def search(self, request):
        """ Tìm kiếm sản phẩm theo tên """
        keyword = request.query_params.get('q', '')
        products = Product.objects.filter(name__icontains=keyword)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='price-range')
    def filter_by_price(self, request):
        """ Lọc sản phẩm theo khoảng giá """
        min_price = request.query_params.get('min', 0)
        max_price = request.query_params.get('max', 99999999)
        products = Product.objects.filter(price__gte=min_price, price__lte=max_price)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['patch'])
    def update_product(self, request, pk=None):
        """ Cập nhật sản phẩm """
        product = self.get_object()
        serializer = self.get_serializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Cập nhật sản phẩm thành công", "data": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'])
    def delete_product(self, request, pk=None):
        """ Xóa sản phẩm """
        product = self.get_object()
        product.delete()
        return Response({"message": "Xóa sản phẩm thành công"}, status=status.HTTP_204_NO_CONTENT)


class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    parser_classes = [MultiPartParser, FormParser]  # Hỗ trợ upload file ảnh

    def create(self, request, *args, **kwargs):
        product_id = request.data.get('product')
        image = request.FILES.get('image')

        if not product_id or not image:
            return Response({'error': 'Thiếu product_id hoặc file ảnh'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Sản phẩm không tồn tại'}, status=status.HTTP_404_NOT_FOUND)

        product_image = ProductImage.objects.create(product=product, image=image)
        return Response(ProductImageSerializer(product_image).data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['patch'])
    def update_image(self, request, pk=None):
        """ Cập nhật ảnh sản phẩm """
        product_image = self.get_object()
        serializer = self.get_serializer(product_image, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Cập nhật ảnh thành công", "data": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'])
    def delete_image(self, request, pk=None):
        """ Xóa ảnh sản phẩm """
        product_image = self.get_object()
        product_image.delete()
        return Response({"message": "Xóa ảnh sản phẩm thành công"}, status=status.HTTP_204_NO_CONTENT)

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

from rest_framework.decorators import action
from rest_framework.response import Response

class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)

    @action(detail=True, methods=["patch"])
    def update_quantity(self, request, pk=None):
        cart_item = self.get_object()
        quantity = request.data.get("quantity")

        if quantity and int(quantity) > 0:
            cart_item.quantity = int(quantity)
            cart_item.save()
            return Response({"message": "Cập nhật số lượng thành công", "quantity": cart_item.quantity})
        return Response({"error": "Số lượng không hợp lệ"}, status=400)
    @action(detail=True, methods=["delete"])
    def remove_item(self, request, pk=None):
        cart_item = self.get_object()
        cart_item.delete()
        return Response({"message": "Xóa sản phẩm khỏi giỏ hàng thành công"}, status=204)
    
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['post'], serializer_class=CheckoutSerializer)
    def checkout(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)