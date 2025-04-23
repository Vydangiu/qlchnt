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

  <div class="checkout-container">
    <h1>Thanh Toán</h1>
    <div v-if="!user" class="login-prompt">
      <p>Vui lòng đăng nhập để tiếp tục thanh toán.</p>
      <router-link to="/signin" class="login-link">Đăng nhập</router-link>
    </div>
    <div v-else>
      <div class="checkout-form">
        <h2>Thông tin giao hàng</h2>
        <div class="form-group">
          <label for="fullName">Họ và tên</label>
          <input type="text" id="fullName" v-model="form.fullName" required />
        </div>
        <div class="form-group">
          <label for="address">Địa chỉ giao hàng</label>
          <input type="text" id="address" v-model="form.address" required />
        </div>
        <div class="form-group">
          <label for="phone">Số điện thoại</label>
          <input type="tel" id="phone" v-model="form.phone" required />
        </div>
        <div class="form-group">
          <label for="paymentMethod">Phương thức thanh toán</label>
          <select id="paymentMethod" v-model="form.paymentMethod" required>
            <option value="cod">Thanh toán khi nhận hàng (COD)</option>
            <option value="banking">Chuyển khoản ngân hàng</option>
          </select>
        </div>
        <div class="form-group">
          <label for="note">Ghi chú (tùy chọn)</label>
          <textarea id="note" v-model="form.note"></textarea>
        </div>
      </div>

      <div class="order-summary">
        <h2>Tóm tắt đơn hàng</h2>
        <!-- <pre v-if="cart.length">Dữ liệu giỏ hàng: {{ cart }}</pre> -->
        <div v-if="cart.length === 0" class="empty-cart">
          <p>Giỏ hàng trống!</p>
          <router-link to="/Product">Tiếp tục mua sắm</router-link>
        </div>
        <div v-else>
          <div v-for="item in cart" :key="item.id" class="cart-item">
            <img :src="getProductImage(item)" :alt="item.name" class="cart-item-image" />
            <div class="cart-item-details">
              <p>{{ item.name }}</p>
              <p>Số lượng: {{ item.quantity }}</p>
              <p>Giá: {{ formatPrice(item.price * item.quantity) }}</p>
            </div>
          </div>
          <div class="total">
            <strong>Tổng cộng:</strong> {{ formatPrice(totalPrice) }}
          </div>
          <button @click="placeOrder" class="place-order-button">Đặt hàng</button>
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
      user: JSON.parse(localStorage.getItem("user")) || null,
      cart: [],
      form: {
        fullName: "",
        address: "",
        phone: "",
        paymentMethod: "cod", // Giá trị mặc định
        note: "",
      },
      isOpen: false,
    };
  },
  computed: {
    totalPrice() {
      return this.cart.reduce((total, item) => total + item.price * item.quantity, 0);
    },
  },
  methods: {
    toggleMenu() {
      this.isOpen = !this.isOpen;
    },
    getProductImage(product) {
      if (product && product.images && product.images.length > 0) {
        let imageUrl = product.images[0].image_url;
        return imageUrl.startsWith("http") ? imageUrl : `http://127.0.0.1:8000/product_images/${imageUrl.split('/').pop()}`;
      }
      return "/default-image.jpg";
    },
    formatPrice(price) {
      return new Intl.NumberFormat("vi-VN", { style: "currency", currency: "VND" }).format(price);
    },
    async fetchProductForCheckout(productId) {
      try {
        const response = await axios.get(`http://127.0.0.1:8000/api/products/${productId}/`);
        const product = response.data;
        this.cart = [{ ...product, quantity: 1 }];
        localStorage.setItem(`cart_${this.user.id}`, JSON.stringify(this.cart));
        console.log("Sản phẩm được thêm từ API:", this.cart);
      } catch (error) {
        console.error("Lỗi khi lấy sản phẩm:", error);
        alert("Không thể tải sản phẩm!");
      }
    },
    async placeOrder() {
      if (!this.form.fullName || !this.form.address || !this.form.phone || !this.form.paymentMethod) {
        alert("Vui lòng điền đầy đủ thông tin giao hàng và phương thức thanh toán!");
        return;
      }

      const token = localStorage.getItem("access_token");
      if (!token) {
        alert("Bạn cần đăng nhập để đặt hàng!");
        this.$router.push("/signin");
        return;
      }

      if (this.cart.length === 0) {
        alert("Giỏ hàng trống, không thể đặt hàng!");
        return;
      }

      try {
        const orderData = {
          user: this.user.id,
          shipping_address: `${this.form.fullName}, ${this.form.address}, ${this.form.phone}`, // Kết hợp thông tin giao hàng
          payment_method: this.form.paymentMethod,
          items: this.cart.map((item) => ({
            product: item.id,
            quantity: item.quantity,
            price: item.price,
          })),
          total_price: this.totalPrice,
        };

        console.log("Dữ liệu gửi lên API:", orderData);

        const response = await axios.post("http://127.0.0.1:8000/api/orders/", orderData, {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        });

        console.log("Phản hồi từ API:", response.data);
        alert("Đặt hàng thành công!");
        localStorage.removeItem(`cart_${this.user.id}`);
        this.cart = [];
        this.$router.push("/orders");
      } catch (error) {
        console.error("Lỗi khi đặt hàng:", error.response?.data || error);
        alert("Có lỗi xảy ra khi đặt hàng: " + JSON.stringify(error.response?.data));
      }
    },
    logout() {
      localStorage.removeItem("access_token");
      localStorage.removeItem("user");
      this.user = null;
      this.cart = [];
      this.$router.push("/signin");
    },
  },
  created() {
    if (this.user) {
      const cartKey = `cart_${this.user.id}`;
      this.cart = JSON.parse(localStorage.getItem(cartKey)) || [];
      console.log("Giỏ hàng trong Checkout.vue:", this.cart);

      const productId = this.$route.params.productId;
      if (productId && this.cart.length === 0) {
        this.fetchProductForCheckout(productId);
      }
    } else {
      this.$router.push("/signin");
    }
  },
};
</script>

<style scoped>
.checkout-container {
  max-width: 1200px;
  margin: 20px auto;
  padding: 20px;
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.checkout-form,
.order-summary {
  flex: 1;
  min-width: 300px;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.cart-item {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
  border-bottom: 1px solid #eee;
  padding-bottom: 10px;
}

.cart-item-image {
  width: 80px;
  height: 80px;
  object-fit: cover;
  margin-right: 15px;
}

.cart-item-details p {
  margin: 5px 0;
}

.total {
  margin-top: 20px;
  font-size: 1.2rem;
  text-align: right;
}

.place-order-button {
  width: 100%;
  padding: 12px;
  background-color: #ff6600;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1.2rem;
  margin-top: 20px;
}

.place-order-button:hover {
  background-color: #e65c00;
}

.login-prompt {
  text-align: center;
}

.login-link {
  color: #007bff;
  text-decoration: none;
}

.login-link:hover {
  text-decoration: underline;
}

.empty-cart {
  text-align: center;
}
</style>