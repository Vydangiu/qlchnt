<template>
  <header class="menu-toggle">
    <div class="navbar">
      <div class="navbar-link">
        <ul class="navbar-link-item" :class="{ 'active': isOpen }">
          <li class="item-link"><a class="link" href="/">Trang chủ</a></li>
          <li class="item-link"><a class="link" href="Product">Sản phẩm</a></li>
          <li class="item-link"><a class="link" href="Blog">About</a></li>
          <li class="item-link"><a class="link" href="contact">Liên hệ</a></li>
        </ul>
      </div>
      <div class="navbar-logo">
        <img class="logo" src="@/assets/IMG/logo1.jpg" alt="logo">
      </div>
      <div class="navbar-search">
        <input type="text" class="search-input" placeholder="Tìm kiếm">
        <div class="icon-search">
          <a class="link" href=""><i class="fa-solid fa-magnifying-glass"></i></a>
        </div>
      </div>
      <div class="navbar-cart-login-icon">
        <a style="font-size: 2rem;" href="/cart">
          <i class="fa-solid fa-bag-shopping"></i>
        </a>

        <div v-if="user" class="user-info">
          <a class="user-hello" style="font-size: 2rem; cursor: pointer;" @click="logout">
            <i style="margin-top: 40px" class="fa-solid fa-user"></i>
            <span style="font-size: 1rem; display: inline-flex; margin-left: -20px;">Xin chào, {{ user.username }}</span>
          </a>
        </div>
        <a v-else style="font-size: 2rem; padding-bottom: 10px;" href="/signin">
          <i class="fa-solid fa-user"></i>
        </a>
      </div>
    </div>
    <div class="hamburger" @click="toggleMenu">☰</div>
  </header>

  <div class="cart-container">
    <h1 style="padding-bottom: 1.5rem;">🛒 Giỏ Hàng Của Bạn</h1>

    <div v-if="cart.length === 0" class="empty-cart">
      <p>Giỏ hàng của bạn đang trống!</p>
      <router-link to="/Product" class="back-to-shop">🛍️ Tiếp tục mua sắm</router-link>
    </div>

    <div v-else>
      <table class="cart-table">
        <thead>
          <tr>
            <th>Sản phẩm</th>
            <th>Giá</th>
            <th>Số lượng</th>
            <th>Tổng</th>
            <th>Hành động</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in cart" :key="item.id">
            <td style="display: flex; flex-direction: column;" class="cart-item">
              <img :src="getProductImage(item)" alt="Product image" class="cart-image">
              <span>{{ item.name }}</span>
            </td>
            <td>{{ formatPrice(item.price) }}</td>
            <td>
              <button @click="updateQuantity(item, -1)">➖</button>
              <span style="margin: 0 10px">{{ item.quantity }}</span>
              <button @click="updateQuantity(item, 1)">➕</button>
            </td>
            <td>{{ formatPrice(item.price * item.quantity) }}</td>
            <td><button @click="removeFromCart(item)">❌ Xóa</button></td>
          </tr>
        </tbody>
      </table>

      <div class="cart-total">
        <h2>Tổng tiền: {{ formatPrice(totalPrice) }}</h2>
        <button @click="proceedToCheckout" class="checkout-button">🛍️ Thanh Toán</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      cart: [],
      user: JSON.parse(localStorage.getItem("user")) || null,
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
    updateQuantity(item, change) {
      const index = this.cart.findIndex((p) => p.id === item.id);
      if (index !== -1) {
        this.cart[index].quantity += change;
        if (this.cart[index].quantity <= 0) {
          this.cart.splice(index, 1);
        }
        this.saveCart();
      }
    },
    removeFromCart(item) {
      this.cart = this.cart.filter((p) => p.id !== item.id);
      this.saveCart();
    },
    saveCart() {
      if (this.user) {
        localStorage.setItem(`cart_${this.user.id}`, JSON.stringify(this.cart));
      }
    },
    proceedToCheckout() {
      if (!this.user) {
        this.$router.push("/signin");
        return;
      }
      // Chuyển hướng đến trang checkout
      this.$router.push("/checkout");
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
      this.cart = JSON.parse(localStorage.getItem(`cart_${this.user.id}`)) || [];
    } else {
      this.$router.push("/signin");
    }
  },
};
</script>

<style>
.cart-container {
  max-width: 800px;
  margin: auto;
  padding: 20px;
  text-align: center;
}
.cart-table {
  width: 100%;
  border-collapse: collapse;
}
.cart-table th,
.cart-table td {
  border: 2px solid #dddd;
  padding: 10px 20px;
}
.cart-image {
  width: 100px;
  height: 80px;
  margin: 0 auto;
}
.cart-total {
  margin-top: 20px;
  font-size: 1.2rem;
}
.checkout-button {
  background-color: #ff6600;
  color: white;
  padding: 10px;
  border: none;
  cursor: pointer;
  font-size: 1.2rem;
  margin-top: 1.5rem;
  border-radius: 8px;
}
.empty-cart {
  font-size: 1.2rem;
}
.back-to-shop {
  display: inline-block;
  margin-top: 10px;
  font-size: 1rem;
  color: blue;
}
</style>