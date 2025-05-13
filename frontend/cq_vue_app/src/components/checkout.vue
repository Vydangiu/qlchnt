<template>
  <div>
    <!-- Font Awesome for icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">

    <!-- Navbar from Order page -->
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
          <input type="text" v-model="navbarSearch" class="search-input" placeholder="Tìm kiếm" @keyup.enter="searchFromNavbar" />
          <div class="icon-search">
            <a class="link" href="#" @click.prevent="searchFromNavbar">
              <i class="fa-solid fa-magnifying-glass"></i>
            </a>
          </div>
        </div>
        <div class="navbar-cart-login-icon">
          <a style="font-size: 2rem;" href="/cart">
            <i class="fa-solid fa-bag-shopping"></i>
          </a>
          <a style="font-size: 2rem;" href="/orders">
            <i class="fa-solid fa-clipboard-list"></i>
          </a>
          <div v-if="user" class="user-info">
            <a class="user-hello" style="font-size: 2rem; cursor: pointer;" @click="logout">
              <i style="margin-top: 40px" class="fa-solid fa-user"></i>
              <span style="font-size: 1rem; display: inline-flex; margin-left: 5%;">Xin chào <br>{{ user.username }}</span>
            </a>
          </div>
          <a v-else style="font-size: 2rem; padding-bottom: 10px;" href="/signin">
            <i class="fa-solid fa-user"></i>
          </a>
        </div>
      </div>
    </header>

    <!-- Existing Checkout Content -->
    <div class="checkout-container">
      <h1 class="checkout-title">🛒 Thanh Toán</h1>

      <!-- Thông báo giỏ hàng trống -->
      <div v-if="displayedCart.length === 0" class="empty-cart">
        <p>Giỏ hàng của bạn đang trống!</p>
        <router-link to="/Product" class="back-to-shop">🛍️ Tiếp tục mua sắm</router-link>
      </div>

      <!-- Hiển thị giỏ hàng và form thanh toán -->
      <div v-else class="checkout-content">
        <!-- Bảng giỏ hàng -->
        <div class="cart-section">
          <table class="cart-table">
            <thead>
              <tr>
                <th>Sản phẩm</th>
                <th>Giá</th>
                <th>Số lượng</th>
                <th>Tổng</th>
                <th v-if="!isBuyNow">Hành động</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in displayedCart" :key="item.id">
                <td class="cart-item">
                  <img :src="getProductImage(item)" alt="Product image" class="cart-image">
                  <span>{{ item.name }}</span>
                </td>
                <td>{{ formatPrice(item.price) }}</td>
                <td class="quantity-controls">
                  <button @click="updateQuantity(item, -1)" :disabled="item.quantity <= 1">➖</button>
                  <span>{{ item.quantity }}</span>
                  <button @click="updateQuantity(item, 1)">➕</button>
                </td>
                <td>{{ formatPrice(item.price * item.quantity) }}</td>
                <td v-if="!isBuyNow">
                  <button @click="confirmRemove(item)" class="remove-button">❌ Xóa</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Form thông tin thanh toán -->
        <div class="checkout-form">
          <h3>Thông tin thanh toán</h3>
          <div class="form-group">
            <label for="name">Tên người nhận:</label>
            <input
              type="text"
              id="name"
              v-model="name"
              placeholder="Nhập tên người nhận"
              required
            />
          </div>
          <div class="form-group">
            <label for="phone">Số điện thoại:</label>
            <input
              type="tel"
              id="phone"
              v-model="phone"
              placeholder="Nhập số điện thoại"
              required
            />
          </div>
          <div class="form-group">
            <label for="shipping_address">Địa chỉ giao hàng:</label>
            <input
              type="text"
              id="shipping_address"
              v-model="shippingAddress"
              placeholder="Nhập địa chỉ giao hàng"
              required
            />
          </div>
          <div class="form-group">
            <label for="note">Ghi chú:</label>
            <textarea
              id="note"
              v-model="note"
              placeholder="Ghi chú cho đơn hàng (nếu có)"
              rows="3"
            ></textarea>
          </div>
          <div class="form-group">
            <label for="payment_method">Phương thức thanh toán:</label>
            <select id="payment_method" v-model="paymentMethod">
              <option value="cod">Thanh toán khi nhận hàng (COD)</option>
            </select>
          </div>
          <h2 class="total-price">Tổng tiền: {{ formatPrice(totalPrice) }}</h2>
          <button @click="confirmCheckout" class="confirm-button">✅ Xác nhận đơn hàng</button>
          <p v-if="error" class="error">{{ error }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "CheckoutView",
  data() {
    return {
      cart: [], // Giỏ hàng từ localStorage
      displayedCart: [], // Giỏ hàng hiển thị (có thể từ localStorage hoặc buyNow)
      user: null,
      name: "",
      phone: "",
      shippingAddress: "",
      note: "",
      paymentMethod: "cod",
      error: null,
      productId: null,
      isBuyNow: false, // Xác định xem có phải từ "Mua Ngay" không
      isOpen: false, // For navbar toggle
      navbarSearch: "", // For navbar search
    };
  },
  computed: {
    totalPrice() {
      return this.displayedCart.reduce((total, item) => total + item.price * item.quantity, 0);
    },
  },
  methods: {
    getProductImage(product) {
      if (product?.images?.length > 0) {
        const imageUrl = product.images[0].image_url;
        return imageUrl.startsWith("http") ? imageUrl : `http://127.0.0.1:8000/product_images/${imageUrl.split('/').pop()}`;
      }
      return "/default-image.jpg";
    },

    formatPrice(price) {
      return new Intl.NumberFormat("vi-VN", { style: "currency", currency: "VND" }).format(price);
    },

    updateQuantity(item, change) {
      const index = this.displayedCart.findIndex((p) => p.id === item.id);
      if (index === -1) return;

      const newQuantity = this.displayedCart[index].quantity + change;
      if (newQuantity <= 0) {
        if (!this.isBuyNow) {
          this.confirmRemove(item);
        } else {
          alert("Số lượng tối thiểu là 1!");
          return;
        }
      } else {
        this.displayedCart[index].quantity = newQuantity;
        this.displayedCart = [...this.displayedCart];

        if (!this.isBuyNow) {
          this.cart = [...this.displayedCart];
          this.saveCart();
        }
        alert(`Số lượng đã được cập nhật: ${newQuantity}`);
      }
    },

    confirmRemove(item) {
      if (confirm(`Bạn có chắc chắn muốn xóa "${item.name}" khỏi giỏ hàng không?`)) {
        this.cart = this.cart.filter((p) => p.id !== item.id);
        this.displayedCart = [...this.cart];
        this.saveCart();
        alert("Sản phẩm đã được xóa!");
      }
    },

    saveCart() {
      if (!this.user) return;
      try {
        localStorage.setItem(`cart_${this.user.id}`, JSON.stringify(this.cart));
      } catch (error) {
        console.error("Lỗi khi lưu giỏ hàng:", error);
        this.error = "Không thể lưu giỏ hàng. Vui lòng kiểm tra trình duyệt.";
      }
    },

    async fetchProductById(productId) {
      try {
        const response = await axios.get(`http://127.0.0.1:8000/api/products/${productId}/`);
        return response.data;
      } catch (error) {
        console.error("Lỗi khi lấy sản phẩm:", error);
        this.error = "Không thể lấy thông tin sản phẩm.";
        return null;
      }
    },

    async syncCartWithBackend() {
      const token = localStorage.getItem("access_token");
      if (!token || !this.user) {
        this.error = "Bạn cần đăng nhập để thanh toán!";
        this.$router.push("/signin");
        return false;
      }

      try {
        let cartResponse = await axios.get("http://127.0.0.1:8000/api/carts/", {
          headers: { Authorization: `Bearer ${token}` },
        });

        let cartId;
        if (Array.isArray(cartResponse.data) && cartResponse.data.length > 0) {
          cartId = cartResponse.data[0].id;
        } else if (cartResponse.data?.id) {
          cartId = cartResponse.data.id;
        } else {
          cartResponse = await axios.post(
            "http://127.0.0.1:8000/api/carts/",
            { user: this.user.id },
            { headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" } }
          );
          cartId = cartResponse.data.id;
        }

        if (!cartId) throw new Error("Không thể lấy hoặc tạo giỏ hàng!");

        const cartItemsResponse = await axios.get("http://127.0.0.1:8000/api/cart-items/", {
          headers: { Authorization: `Bearer ${token}` },
          params: { cart: cartId },
        });

        const cartItems = cartItemsResponse.data;
        for (const item of cartItems) {
          await axios.delete(`http://127.0.0.1:8000/api/cart-items/${item.id}/`, {
            headers: { Authorization: `Bearer ${token}` },
          });
        }

        for (const item of this.displayedCart) {
          await axios.post(
            "http://127.0.0.1:8000/api/cart-items/",
            {
              cart: cartId,
              product: item.id,
              quantity: item.quantity,
            },
            { headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" } }
          );
        }
        return true;
      } catch (error) {
        console.error("Lỗi khi đồng bộ giỏ hàng:", error.response?.data || error.message);
        this.error = "Không thể đồng bộ giỏ hàng với hệ thống.";
        return false;
      }
    },

    async confirmCheckout() {
      this.error = null;

      if (!this.user) {
        this.error = "Vui lòng đăng nhập để thanh toán!";
        this.$router.push("/signin");
        return;
      }

      if (!this.name.trim()) {
        this.error = "Vui lòng nhập tên người nhận!";
        return;
      }

      if (!this.phone.trim()) {
        this.error = "Vui lòng nhập số điện thoại!";
        return;
      }

      if (!this.shippingAddress.trim()) {
        this.error = "Vui lòng nhập địa chỉ giao hàng!";
        return;
      }

      if (this.displayedCart.length === 0) {
        this.error = "Giỏ hàng của bạn đang trống!";
        return;
      }

      const synced = await this.syncCartWithBackend();
      if (!synced) return;

      const token = localStorage.getItem("access_token");
      try {
        const payload = {
          name: this.name,
          phone_number: this.phone,
          shipping_address: this.shippingAddress,
          note: this.note,
          payment_method: this.paymentMethod,
        };
        if (this.isBuyNow && this.productId) {
          payload.product_id = this.productId;
        }

        const response = await axios.post(
          "http://127.0.0.1:8000/api/orders/checkout/",
          payload,
          {
            headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" },
          }
        );

        const customerInfo = {
          name: this.name,
          phone: this.phone,
          shipping_address: this.shippingAddress,
        };
        localStorage.setItem(`customer_info_${this.user.id}`, JSON.stringify(customerInfo));

        alert("Thanh toán thành công! Đơn hàng của bạn đã được tạo.");
        if (!this.isBuyNow) {
          localStorage.removeItem(`cart_${this.user.id}`);
        }
        this.$router.push("/orders");
      } catch (error) {
        console.error("Lỗi khi thanh toán:", error.response?.data || error.message);
        this.error = error.response?.data?.detail || "Có lỗi xảy ra khi thanh toán.";
      }
    },

    logout() {
      localStorage.removeItem("access_token");
      localStorage.removeItem("user");
      localStorage.removeItem(`cart_${this.user.id}`);
      localStorage.removeItem(`customer_info_${this.user.id}`);
      this.user = null;
      this.$router.push("/signin");
    },

    searchFromNavbar() {
      // Placeholder: Implement search logic if needed
      alert("Tìm kiếm: " + this.navbarSearch);
      this.navbarSearch = "";
    },
  },
  async created() {
    this.user = JSON.parse(localStorage.getItem("user")) || null;
    if (!this.user) {
      this.error = "Vui lòng đăng nhập để tiếp tục!";
      this.$router.push("/signin");
      return;
    }

    this.cart = JSON.parse(localStorage.getItem(`cart_${this.user.id}`)) || [];
    this.name = this.user.username || "";

    this.isBuyNow = this.$route.query.buyNow === 'true';
    this.productId = this.$route.query.productId ? parseInt(this.$route.query.productId) : null;

    if (this.isBuyNow && this.productId) {
      const product = await this.fetchProductById(this.productId);
      if (product) {
        this.displayedCart = [{ ...product, quantity: 1 }];
      } else {
        this.error = "Không thể tải sản phẩm để thanh toán!";
      }
    } else {
      this.displayedCart = [...this.cart];
    }
  },
};
</script>

<style scoped>
/* Navbar styles from Order page */
.navbar {
  width: 100%;
  height: 60px;
  background-color: RGB(138, 99, 68);
  display: flex;
  align-items: center;
  font-size: 1.75rem;
  border-radius: 10px;
  position: fixed;
  top: 0;
  left: 0;
  z-index: 1000;
  justify-content: space-between;
  padding: 0 20px;
}

.navbar-link {
  display: flex;
}

.navbar-link-item {
  display: flex;
  justify-content: space-between;
  margin: 0;
  font-size: 1.5rem;
}

.navbar-link-item.active {
  display: flex;
}

.item-link {
  list-style: none;
  margin: 0 20px;
}

.link {
  text-decoration: none;
  color: rgb(37, 36, 36);
  font-size: 1.5rem;
  white-space: nowrap;
  transition: color 0.3s;
}

.link:hover {
  color: white;
}

.logo {
  width: 175px;
  height: 38px;
  margin-right: 40px;
}

.navbar-search {
  display: flex;
  background-color: white;
  border-radius: 15px;
  outline-color: white;
  width: 30rem;
}

.search-input {
  border-style: none;
  border-radius: 15px;
  padding: 0 10px;
  width: 25rem;
  font-size: 1rem;
}

.icon-search {
  border-left: 2px solid #3333;
  padding: 3px 20px;
  width: 5rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.navbar-cart-login-icon {
  display: flex;
  align-items: center;
  gap: 15px;
}

.fa-bag-shopping,
.fa-clipboard-list,
.fa-user {
  margin: 0;
  color: rgb(37, 36, 36);
  transition: color 0.3s;
  font-size: 2rem;
}

.fa-bag-shopping:hover,
.fa-clipboard-list:hover,
.fa-user:hover {
  color: white;
}

.user-info {
  display: flex;
  align-items: center;
  position: relative;
}

.user-hello {
  display: flex;
  flex-direction: column;
  align-items: center;
  color: rgb(37, 36, 36);
  cursor: pointer;
  text-align: center;
}

.user-hello:hover {
  color: white;
}

.user-hello i {
  font-size: 2rem;
  margin: 0;
}

.user-hello span {
  font-size: 1rem;
  margin-top: 5px;
  white-space: nowrap;
}

/* Existing Checkout styles with adjustment for navbar */
.checkout-container {
  max-width: 900px;
  margin: 0 auto;
  padding: 20px;
  font-family: Arial, sans-serif;
  margin-top: 80px; /* Added to prevent overlap with fixed navbar */
}

.checkout-title {
  text-align: center;
  margin-bottom: 1.5rem;
  font-size: 2rem;
  color: #333;
}

.empty-cart {
  text-align: center;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
}

.empty-cart p {
  font-size: 1.2rem;
  margin-bottom: 10px;
}

.back-to-shop {
  color: #007bff;
  text-decoration: none;
  font-size: 1.1rem;
}

.back-to-shop:hover {
  text-decoration: underline;
}

.checkout-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.cart-section {
  overflow-x: auto;
}

.cart-table {
  width: 100%;
  border-collapse: collapse;
  background-color: #fff;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.cart-table th,
.cart-table td {
  padding: 12px 15px;
  text-align: center;
  border-bottom: 1px solid #ddd;
}

.cart-table th {
  background-color: #f5f5f5;
  font-weight: bold;
  color: #333;
}

.cart-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.cart-image {
  width: 80px;
  height: 60px;
  object-fit: cover;
  border-radius: 4px;
}

.quantity-controls {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
}

.quantity-controls button {
  padding: 5px 10px;
  font-size: 1rem;
  border: none;
  background-color: #f0f0f0;
  border-radius: 4px;
  cursor: pointer;
}

.quantity-controls button:hover {
  background-color: #e0e0e0;
}

.quantity-controls button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.quantity-controls span {
  font-size: 1.1rem;
}

.remove-button {
  padding: 5px 10px;
  font-size: 1rem;
  border: none;
  background-color: #ff4d4d;
  color: white;
  border-radius: 4px;
  cursor: pointer;
}

.remove-button:hover {
  background-color: #e60000;
}

.checkout-form {
  background-color: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.checkout-form h3 {
  margin-bottom: 15px;
  font-size: 1.5rem;
  color: #333;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
  color: #555;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 10px;
  font-size: 1rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-sizing: border-box;
}

.form-group textarea {
  resize: vertical;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #ff6600;
}

.total-price {
  font-size: 1.5rem;
  margin: 20px 0;
  color: #e60000;
}

.confirm-button {
  width: 100%;
  padding: 12px;
  font-size: 1.2rem;
  background-color: #ff6600;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}

.confirm-button:hover {
  background-color: #e65c00;
}

.error {
  color: #e60000;
  margin-top: 10px;
  font-size: 1rem;
  text-align: center;
}

/* Responsive styles for navbar */
@media screen and (max-width: 800px) {
  .navbar {
    height: 50px;
    justify-content: space-between;
  }

  .navbar-search {
    display: none !important;
  }

  .search-input {
    display: none;
  }

  .navbar-cart-login-icon {
    display: none !important;
  }

  .navbar-logo {
    display: none;
  }

  .navbar-link {
    background-color: RGB(138, 99, 68);
    width: 100% !important;
    position: fixed;
    top: 20px;
    left: 0;
    right: 0;
    flex-wrap: wrap;
  }

  .navbar-link-item {
    flex-direction: column;
    align-items: center;
  }

  .navbar-link-item.active {
    display: flex;
  }
}
</style>