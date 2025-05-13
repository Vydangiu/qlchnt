from django.db import models
from users.models import User 


# class StoreUser(models.Model):
#     ROLE_CHOICES = [
#         ('customer', 'Customer'),
#         ('admin', 'Admin'),
#     ]

#     username = models.CharField(max_length=50, unique=True)
#     email = models.EmailField(unique=True)
#     password = models.CharField(max_length=255)
#     full_name = models.CharField(max_length=100, blank=True, null=True)
#     phone = models.CharField(max_length=15, blank=True, null=True)
#     address = models.TextField(blank=True, null=True)
#     role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.username





# Bảng danh mục sản phẩm
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

# Bảng sản phẩm
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return f"Image for {self.product.name}"


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="carts")
    created_at = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        return sum(item.product.price * item.quantity for item in self.items.all())

    def __str__(self):
        return f"Cart {self.id} - {self.user.username}"

    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
    
# class Order(models.Model):
#     PAYMENT_CHOICES = [
#         ('cod', 'Cash on Delivery'),
#         ('banking', 'Bank Transfer'),
#     ]

#     STATUS_CHOICES = [
#         ('pending', 'Pending'),
#         ('processing', 'Processing'),
#         ('completed', 'Completed'),
#         ('cancelled', 'Cancelled'),
#     ]

#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     # shipping_address = models.TextField(null=True, blank=True)
#     shipping_address = models.TextField()


#     payment_method = models.CharField(
#         max_length=20,
#         choices=PAYMENT_CHOICES,
#         default='cod'  # <-- match the key from choices
#     )
#     total_price = models.DecimalField(max_digits=10, decimal_places=2)
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"Order {self.id} - {self.user.username}"

# class OrderItem(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField()
#     price = models.DecimalField(max_digits=10, decimal_places=2)

# class Order(models.Model):
#     PAYMENT_CHOICES = [
#         ('cod', 'Cash on Delivery'),
#         ('banking', 'Bank Transfer'),
#     ]

#     STATUS_CHOICES = [
#         ('pending', 'Pending'),
#         ('processing', 'Processing'),
#         ('completed', 'Completed'),
#         ('cancelled', 'Cancelled'),
#     ]

#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     shipping_address = models.TextField()
#     # shipping_address = models.TextField(null=True, blank=True)

#     payment_method = models.CharField(
#         max_length=20,
#         choices=PAYMENT_CHOICES,
#         default='cod'
#     )
#     # total_price field can be stored at creation time
#     total_price = models.DecimalField(max_digits=10, decimal_places=2)
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"Order {self.id} - {self.user.username}"

#     @property
#     def total_items(self):
#         """
#         Tổng số lượng sản phẩm trong đơn hàng
#         """
#         return sum(item.quantity for item in self.items.all())

#     @property
#     def computed_total(self):
#         """
#         Tính tổng tiền dựa trên các OrderItem để đảm bảo tính nhất quán
#         """
#         return sum(item.price * item.quantity for item in self.items.all())

# class OrderItem(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField()
#     price = models.DecimalField(max_digits=10, decimal_places=2)
    

#     def __str__(self):
#         return f"{self.quantity} x {self.product.name}"

#     @property
#     def image_url(self):
#         """
#         Trả về URL của ảnh đầu tiên của sản phẩm
#         """
#         first_image = self.product.images.first()
#         return first_image.image.url if first_image else ''

class Order(models.Model):
    PAYMENT_CHOICES = [
        ('cod', 'Cash on Delivery'),
        ('banking', 'Bank Transfer'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shipping_address = models.TextField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, default="Chưa cung cấp")  # Trường số điện thoại
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='cod')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

