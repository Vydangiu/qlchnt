# 🛋️ Dự án Cửa Hàng Nội Thất - Backend Django + Frontend Vue

Trang web quản lý và hiển thị các sản phẩm nội thất như sofa, giường ngủ, bàn ăn,...  
Được xây dựng với:

- ✅ **Backend:** Django + Django REST Framework  
- ✅ **Frontend:** Vue.js + Vite  
- ✅ **Cơ sở dữ liệu:** PostgreSQL

---
## 🚀 TÍNH NĂNG CHÍNH

- Quản lý danh mục, sản phẩm, ảnh sản phẩm
- Giao diện người dùng thân thiện, hiển thị sản phẩm
- Tích hợp frontend Vue.js với backend Django REST
- CSDL PostgreSQL
- Hỗ trợ JWT Authentication
- CORS cho phép frontend truy cập backend

---

## 🗃️ Cấu hình DATABASE
```
Trong furniture_api/setting.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'cuahangnoithat',
        'USER': 'postgres',
        'PASSWORD': '123',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```
## 🏗️ Chạy backend Django
```
python manage.py migrate  
python manage.py runserver

```
## Inset dữ liệu vào PostgreSQL
Vào postgres --> Chuột phải cuahangnoithat --> Query Tool 
Nhập các dòng sau đây để có dữ liệu
```
--Insert dữ liệu cho bảng store_category
INSERT INTO store_category (name, description) VALUES
('Phòng khách', 'Các sản phẩm nội thất dành cho phòng khách như sofa, bàn trà, kệ tivi'),
('Phòng ngủ', 'Các sản phẩm nội thất dành cho phòng ngủ như giường, tủ quần áo, bàn trang điểm'),
('Phòng ăn', 'Các sản phẩm nội thất dành cho phòng ăn như bàn ăn, ghế ăn, tủ bếp'),
('Văn phòng', 'Các sản phẩm nội thất dành cho văn phòng như bàn làm việc, ghế văn phòng, tủ tài liệu'),
('Ngoài trời', 'Các sản phẩm nội thất dành cho không gian ngoài trời như bàn ghế sân vườn');

-- Insert dữ liệu cho bảng store_product (Product)
INSERT INTO store_product (category_id, name, description, price, stock, discount, created_at, updated_at) VALUES
(1, 'Sofa Bắc Âu', 'Sofa phong cách Bắc Âu với chất liệu vải bền đẹp, khung gỗ tự nhiên chắc chắn', 12500000, 10, 5.00, NOW(), NOW()),
(1, 'Bàn trà mặt đá', 'Bàn trà mặt đá cẩm thạch, chân kim loại sơn đen sang trọng', 4500000, 15, 0.00, NOW(), NOW()),
(1, 'Kệ tivi gỗ sồi', 'Kệ tivi được làm từ gỗ sồi tự nhiên, thiết kế hiện đại với nhiều ngăn chứa đồ', 6800000, 8, 10.00, NOW(), NOW()),
(2, 'Giường ngủ King size', 'Giường ngủ King size (1m8 x 2m) với khung gỗ tự nhiên, đầu giường bọc da cao cấp', 15900000, 5, 7.00, NOW(), NOW()),
(2, 'Tủ quần áo 4 cánh', 'Tủ quần áo 4 cánh làm từ gỗ MDF phủ melamine chống ẩm, thiết kế nhiều ngăn tiện dụng', 8500000, 7, 0.00, NOW(), NOW()),
(3, 'Bàn ăn mặt đá 6 người', 'Bàn ăn mặt đá cẩm thạch cho 6 người, chân kim loại sơn tĩnh điện', 9800000, 6, 8.00, NOW(), NOW()),
(3, 'Ghế ăn gỗ tự nhiên', 'Ghế ăn được làm từ gỗ tự nhiên, đệm ngồi bọc vải cao cấp', 1200000, 30, 0.00, NOW(), NOW()),
(4, 'Bàn làm việc gỗ', 'Bàn làm việc gỗ công nghiệp cao cấp, thiết kế nhiều ngăn kéo tiện lợi', 5500000, 10, 5.00, NOW(), NOW()),
(4, 'Ghế văn phòng ergonomic', 'Ghế văn phòng thiết kế theo công thái học, có thể điều chỉnh độ cao và độ ngả lưng', 3800000, 15, 0.00, NOW(), NOW()),
(5, 'Bộ bàn ghế sân vườn', 'Bộ bàn ghế sân vườn chất liệu nhựa giả mây cao cấp, chịu được mưa nắng', 8900000, 5, 12.00, NOW(), NOW());

-- Insert dữ liệu cho bảng store_productimage (ProductImage)
INSERT INTO store_productimage (product_id, image) VALUES
(1, 'product_images/sofa-bac-au-1.jpg'),
(1, 'product_images/sofa-bac-au-2.jpg'),
(2, 'product_images/ban-tra-mat-da-1.jpg'),
(3, 'product_images/ke-tivi-go-soi-1.jpg'),
(4, 'product_images/giuong-king-size-1.jpg'),
(5, 'product_images/tu-quan-ao-4-canh-1.jpg'),
(6, 'product_images/ban-an-mat-da-1.jpg'),
(7, 'product_images/ghe-an-go-1.jpg'),
(8, 'product_images/ban-lam-viec-1.jpg'),
(9, 'product_images/ghe-van-phong-1.jpg'),
(10, 'product_images/ban-ghe-san-vuon-1.jpg');
```
## ⚙️ Cài đặt môi trường
### 🐍 Cài đặt Python packages cho Django
```bash
pip install django==5.1.6                         # Framework Django phiên bản 5.1.6
pip install djangorestframework                   # Django REST Framework để xây dựng API
pip install djangorestframework-simplejwt         # Xác thực bằng JWT
pip install django-extensions                     # Các tiện ích mở rộng cho Django
pip install django-cors-headers                   # Cho phép frontend truy cập từ domain khác (CORS)
pip install psycopg2-binary                       # Driver kết nối PostgreSQL
pip install Pillow                                # Hỗ trợ xử lý ảnh trong ImageField

### 🔧 Nếu bị lỗi pip, hãy cài lại:
python -m ensurepip --upgrade
python -m pip install --upgrade pip

###📦 Cài đặt cho frontend (Vue 3 + Vite + Pinia)
npm install vite --save-dev
npm install pinia

```
## 💻 Chạy backend Django
python manage.py runserver
## 💻 Chạy frontend Vue
cd frontend : npm run dev
