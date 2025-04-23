<template>
  <header class="menu-toggle">
    <div class="navbar">
      <div class="navbar-link">
        <ul class="navbar-link-item" :class="{ 'active': isOpen }">
          <li class="item-link"><a class="link" href="/">Trang chủ</a></li>
          <li class="item-link"><a class="link" href="/Product">Sản phẩm</a></li>
          <li class="item-link"><a class="link" href="/Blog">About</a></li>
          <li class="item-link"><a class="link" href="/contact">Liên hệ</a></li>
        </ul>
      </div>
      <div class="navbar-logo">
        <img class="logo" src="@/assets/IMG/logo1.jpg" alt="logo">
      </div>
      <div class="navbar-search">
        <input type="text" class="search-input" placeholder="Tìm kiếm">
        <div class="icon-search">
          <a class="link" href="#"><i class="fa-solid fa-magnifying-glass"></i></a>
        </div>
      </div>
      <div class="navbar-cart-login-icon">
        <a style="font-size: 2rem;" href="/cart">
          <i class="fa-solid fa-bag-shopping"></i>
        </a>
        <div v-if="user" class="user-info">
          <a class="user-hello" style="font-size: 2rem; cursor: pointer;" @click="logout">
            <i style="margin-top: 40px" class="fa-solid fa-user"></i>
            <span style="font-size: 1rem; display: inline-flex;">Xin chào, {{ user.username }}</span>
          </a>
        </div>
        <a v-else style="font-size: 2rem; padding-bottom: 10px;" href="/signin">
          <i class="fa-solid fa-user"></i>
        </a>
      </div>
    </div>
    <div class="hamburger" @click="toggleMenu">☰</div>
  </header>

  <div class="orders">
    <h1>Danh sách đơn hàng của bạn</h1>

    <!-- Debug: Hiển thị dữ liệu đơn hàng -->
    <!-- <pre v-if="orders.length">Dữ liệu đơn hàng: {{ orders }}</pre> -->

    <!-- Kiểm tra xem có đơn hàng không -->
    <div v-if="loading">Đang tải đơn hàng...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else-if="orders.length === 0">
      <p>Hiện tại bạn chưa có đơn hàng nào.</p>
      <router-link to="/Product" class="back-to-shop">🛍️ Tiếp tục mua sắm</router-link>
    </div>

    <!-- Danh sách đơn hàng -->
    <div v-else>
      <div v-for="order in orders" :key="order.id" class="order-item">
        <h2>Đơn hàng #{{ order.id }}</h2>
        <p><strong>Trạng thái:</strong> {{ order.status }}</p>
        <p><strong>Ngày tạo:</strong> {{ formatDate(order.created_at) }}</p>
        <p><strong>Tổng giá trị:</strong> {{ formatPrice(order.total_price) }}</p>

        <button @click="toggleDetails(order.id)">Chi tiết</button>

        <!-- Chi tiết đơn hàng -->
        <div v-if="order.showDetails" class="order-details">
          <h3>Chi tiết đơn hàng</h3>
          <ul>
            <li v-for="item in order.items_detail" :key="item.id">
              <div class="order-item-details">
                <img :src="getProductImage(item.product)" :alt="item.product.name || 'Sản phẩm'" class="order-item-image" />
                <div>
                  <p><strong>Sản phẩm:</strong> {{ item.product.name || 'Không có tên' }}</p>
                  <p><strong>Số lượng:</strong> {{ item.quantity }}</p>
                  <p><strong>Giá:</strong> {{ formatPrice(item.price) }}</p>
                </div>
              </div>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      orders: [],
      user: JSON.parse(localStorage.getItem("user")) || null,
      loading: true,
      error: null,
      isOpen: false,
    };
  },
  methods: {
    toggleMenu() {
      this.isOpen = !this.isOpen;
    },
    async fetchOrders() {
      const token = localStorage.getItem("access_token");
      if (!token || !this.user) {
        this.error = "Bạn cần đăng nhập để xem đơn hàng!";
        this.loading = false;
        this.$router.push("/signin");
        return;
      }

      try {
        const response = await axios.get("http://127.0.0.1:8000/api/orders/", {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        });
        this.orders = response.data.map(order => ({
          ...order,
          showDetails: false,
        }));
        console.log("Dữ liệu đơn hàng từ API:", this.orders);
      } catch (error) {
        console.error("Lỗi khi lấy danh sách đơn hàng:", error.response?.data || error);
        this.error = "Có lỗi xảy ra khi tải danh sách đơn hàng.";
      } finally {
        this.loading = false;
      }
    },
    formatDate(dateString) {
      const options = { year: "numeric", month: "2-digit", day: "2-digit", hour: "2-digit", minute: "2-digit" };
      return new Date(dateString).toLocaleString("vi-VN", options);
    },
    formatPrice(price) {
      return new Intl.NumberFormat("vi-VN", { style: "currency", currency: "VND" }).format(price);
    },
    getProductImage(product) {
      if (product && product.images && product.images.length > 0) {
        let imageUrl = product.images[0].image_url;
        return imageUrl.startsWith("http") ? imageUrl : `http://127.0.0.1:8000/product_images/${imageUrl.split('/').pop()}`;
      }
      return "/default-image.jpg";
    },
    toggleDetails(orderId) {
      const order = this.orders.find((order) => order.id === orderId);
      if (order) {
        order.showDetails = !order.showDetails;
      }
    },
    logout() {
      localStorage.removeItem("access_token");
      localStorage.removeItem("user");
      this.user = null;
      this.orders = [];
      this.$router.push("/signin");
    },
  },
  created() {
    if (this.user) {
      this.fetchOrders();
    } else {
      this.error = "Vui lòng đăng nhập để xem đơn hàng.";
      this.loading = false;
      this.$router.push("/signin");
    }
  },
};
</script>

<style scoped>
.orders {
  max-width: 1200px;
  margin: 20px auto;
  padding: 20px;
}

.order-item {
  margin-bottom: 20px;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #f9f9f9;
}

.order-item h2 {
  margin-top: 0;
}

.order-item p {
  margin: 5px 0;
}

button {
  padding: 8px 16px;
  border: none;
  background-color: #007bff;
  color: white;
  cursor: pointer;
  border-radius: 4px;
  margin-top: 10px;
}

button:hover {
  background-color: #0056b3;
}

.order-details {
  margin-top: 20px;
  padding: 15px;
  border-top: 1px solid #ddd;
}

.order-details ul {
  list-style-type: none;
  padding: 0;
}

.order-item-details {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
}

.order-item-image {
  width: 80px;
  height: 80px;
  object-fit: cover;
  margin-right: 15px;
  border-radius: 4px;
}

.order-details li p {
  margin: 5px 0;
}

.error {
  color: red;
  text-align: center;
}

.back-to-shop {
  display: inline-block;
  margin-top: 10px;
  color: #007bff;
  text-decoration: none;
}

.back-to-shop:hover {
  text-decoration: underline;
}

pre {
  background-color: #f0f0f0;
  padding: 10px;
  border-radius: 4px;
  font-size: 0.9rem;
}
</style>