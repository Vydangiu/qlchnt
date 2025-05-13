<template>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
  <div class="wrapper">
    <!-- Thanh điều hướng (navbar) -->
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

    <!-- Phần danh sách đơn hàng -->
    <div class="buy-now">
      <!-- Phần thông tin người dùng -->
      <div style="background-color: RGB(242, 239, 234); border-right: 1px solid black" class="buy-now-item">
  <h1 class="buy-now-item__title">Nội thất Modo Casa</h1>
  <div class="buy-now-item__form">
    <h2 class="header--inf">Thông tin người dùng</h2>
    <div class="buy-now-item__form--inf">
      <div class="name-gender">
        <input type="text" class="input-buy-now input--name--buy-now" :value="customerInfo.name" placeholder="Họ và tên" readonly>
        <div class="form-gender">
          <a class="button-order" @click="logout" v-if="user">Đăng xuất</a>
          <a class="button-order" href="/signin" v-else>Đăng nhập</a>
        </div>
      </div>
      <div class="email-phone">
        <input type="text" class="input-buy-now input--email--buy-now" :value="user ? user.email : ''" placeholder="Email" readonly>
        <input type="text" class="input-buy-now input--phone--buy-now" :value="customerInfo.phone_number" placeholder="Số điện thoại" readonly>
      </div>
      <input type="text" class="input-buy-now input--address--buy-now" :value="customerInfo.shipping_address" placeholder="Địa chỉ" readonly>
    </div>
  </div>
      </div>
      <!-- Phần danh sách đơn hàng -->
      <div class="buy-now-item">
        <h2 class="header--inf">Danh sách đơn hàng</h2>

        <!-- Kiểm tra trạng thái -->
        <div v-if="loading" class="status-message">Đang tải đơn hàng...</div>
        <div v-else-if="error" class="status-message error">{{ error }}</div>
        <div v-else-if="orders.length === 0" class="status-message">
          <p>Hiện tại bạn chưa có đơn hàng nào.</p>
          <router-link to="/Product" class="button-continue-shopping">🛍️ Tiếp tục mua sắm</router-link>
        </div>

        <!-- Danh sách đơn hàng -->
        <div v-else class="scrollbar" id="style-1">
          <div class="force-overflow">
            <div v-for="order in orders" :key="order.id" class="order-item">
              <div class="img-package-container">
                <div class="buy-now-item__img--package">
                  <img :src="getProductImage(order.items_detail[0]?.product)" :alt="order.items_detail[0]?.product.name || 'Sản phẩm'" class="img--package">
                  <div class="amount-img-package">{{ order.items_detail.length }}</div>
                </div>
                <div class="buy-now-item__name--package">
                  <p class="name--package">Đơn hàng #{{ order.id }}</p>
                  <p><strong>Trạng thái:</strong> {{ order.status }}</p>
                  <p><strong>Ngày tạo:</strong> {{ formatDate(order.created_at) }}</p>
                </div>
                <div class="buy-now-item__cost--package">
                  <p class="cost--package">{{ formatPrice(order.total_price) }}</p>
                </div>
              </div>
              <hr>
              <div class="payment-detail-container">
                <button @click="toggleDetails(order.id)" class="button-order">Chi tiết</button>
                <div v-if="order.showDetails" class="payment-detail-content">
                  <div v-for="item in order.items_detail" :key="item.id" class="img-package-container">
                    <div class="buy-now-item__img--package">
                      <img :src="getProductImage(item.product)" :alt="item.product.name || 'Sản phẩm'" class="img--package">
                      <div class="amount-img-package">{{ item.quantity }}</div>
                    </div>
                    <div class="buy-now-item__name--package">
                      <p class="name--package">{{ item.product.name || 'Không có tên' }}</p>
                    </div>
                    <div class="buy-now-item__cost--package">
                      <p class="cost--package">{{ formatPrice(item.price) }}</p>
                    </div>
                  </div>
                  <hr>
                  <div class="payment-detail-content__item">
                    <p class="payment-detail-content__item--name">Tổng cộng</p>
                    <p class="payment-detail-content__item--cost">{{ formatPrice(order.total_price) }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
  const storedUser = JSON.parse(localStorage.getItem("user"));
  return {
    isOpen: false,
    user: storedUser,
    orders: [],
    customerInfo: JSON.parse(localStorage.getItem(`customer_info_${storedUser?.id}`)) || {
      name: '',
      phone: '',
      shipping_address: '',
    },
    loading: true,
    error: null,
    navbarSearch: "",
  };
},
  methods: {
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

      if (response.data.length > 0) {
        this.orders = response.data.map(order => ({
          ...order,
          showDetails: false,
        }));

        // Cập nhật thông tin khách hàng từ đơn hàng mới nhất
        const latestOrder = this.orders[0];
        this.customerInfo = {
          name: this.user.username || 'Chưa cung cấp',  // Hoặc this.user.first_name nếu bạn lưu tên trong đó
          phone_number: latestOrder.phone_number || 'Chưa cung cấp',
          shipping_address: latestOrder.shipping_address || 'Chưa cung cấp',
        };
        localStorage.setItem(`customer_info_${this.user.id}`, JSON.stringify(this.customerInfo));

      } else {
        this.error = "Không có đơn hàng nào!";
      }
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
      this.customerInfo = { name: '', phone_number: '', shipping_address: '' };
      this.$router.push("/signin");
    },

    async searchFromNavbar() {
      if (!this.navbarSearch.trim()) {
        this.fetchOrders();
        return;
      }

      this.loading = true;
      try {
        const token = localStorage.getItem("access_token");
        const response = await axios.get("http://127.0.0.1:8000/api/orders/", {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
          params: {
            search: this.navbarSearch,
          },
        });

        if (response.data.length > 0) {
          this.orders = response.data.map(order => ({
            ...order,
            showDetails: false,
          }));

          // Cập nhật thông tin khách hàng dựa trên kết quả tìm kiếm
          const latestOrder = this.orders[0];
          this.customerInfo = {
            name: latestOrder.name || this.user.username || 'Chưa cung cấp',
            phone_number: latestOrder.phone_number || 'Chưa cung cấp',
            shipping_address: latestOrder.shipping_address || 'Chưa cung cấp',
          };
        } else {
          this.error = "Không tìm thấy đơn hàng khớp với từ khóa tìm kiếm.";
        }
      } catch (err) {
        this.error = "Lỗi khi tìm kiếm đơn hàng!";
      } finally {
        this.loading = false;
      }
    },
  },

  created() {
  const storedUser = JSON.parse(localStorage.getItem("user"));
  if (storedUser) {
    this.user = storedUser;
    this.fetchOrders();
  } else {
    this.loading = false;
    this.error = "Vui lòng đăng nhập để xem đơn hàng.";
    // setTimeout để tránh gọi redirect ngay trong lifecycle hook
    setTimeout(() => this.$router.push("/signin"), 500);
  }
  this.user = JSON.parse(localStorage.getItem("user")) || null;
    if (this.user) {
    const storedInfo = JSON.parse(localStorage.getItem(`customer_info_${this.user.id}`));
    if (storedInfo) {
      this.customerInfo = storedInfo;
  }
}
},
};
</script>

<style scoped>
/* Thanh điều hướng (navbar) */
.navbar {
  width: 100%;
  height: 60px; /* Increased height slightly for better spacing */
  background-color: RGB(138, 99, 68);
  display: flex;
  align-items: center;
  font-size: 1.75rem;
  border-radius: 10px;
  position: fixed;
  top: 0;
  left: 0;
  z-index: 1000;
  justify-content: space-between; /* Changed to space-between for better distribution */
  padding: 0 20px; /* Added padding for better spacing */
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
  gap: 15px; /* Added gap for consistent spacing between icons */
}

.fa-bag-shopping,
.fa-clipboard-list,
.fa-user {
  margin: 0; /* Removed individual margins for consistent alignment */
  color: rgb(37, 36, 36);
  transition: color 0.3s;
  font-size: 2rem; /* Consistent font size for all icons */
}

.fa-bag-shopping:hover,
.fa-clipboard-list:hover,
.fa-user:hover {
  color: white;
}

.user-info {
  display: flex;
  align-items: center;
  position: relative; /* Added to control text positioning */
}

.user-hello {
  display: flex;
  flex-direction: column; /* Stack icon and text vertically */
  align-items: center;
  color: rgb(37, 36, 36);
  cursor: pointer;
  text-align: center;
}

.user-hello:hover {
  color: white;
}

.user-hello i {
  font-size: 2rem; /* Match other icons */
  margin: 0; /* Remove margin-top to align with other icons */
}

.user-hello span {
  font-size: 1rem;
  margin-top: 5px; /* Space below icon for username */
  white-space: nowrap;
}

/* Phần nội dung chính */
.buy-now {
  display: flex;
  background-color: RGB(252, 248, 239);
  margin-top: 80px; /* Increased to account for taller navbar */
  justify-content: center; /* Center the two sections */
  gap: 20px; /* Add spacing between sections */
  padding: 20px; /* Add padding for better aesthetics */
}

.buy-now-item {
  padding: 20px;
  flex: 1;
  min-width: 300px;
  max-width: 600px; /* Limit max width for balance */
  box-sizing: border-box; /* Ensure padding doesn’t affect width */
}

.buy-now-item__title {
  font-size: 2rem;
  font-weight: 500;
  color: RGB(151, 99, 62);
  text-align: center;
  margin-bottom: 20px;
}

.buy-now-item__form {
  background-color: RGB(242, 239, 234);
}

.buy-now-item__form--inf {
  margin: 20px 0;
}

.name-gender {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.input-buy-now {
  padding: 8px 16px;
  margin: 5px 0;
  border-radius: 15px;
  border: 1px solid #989696;
  font-size: 1.2rem;
  background-color: white;
  color: black;
  width: 100%;
}

.input--name--buy-now {
  flex: 1;
  margin-right: 10px;
}

.input--email--buy-now,
.input--phone--buy-now {
  width: 48%;
}

.email-phone {
  display: flex;
  justify-content: space-between;
  gap: 10px;
}

.input--address--buy-now {
  width: 100%;
}

.form-gender {
  display: flex;
  align-items: center;
  gap: 10px;
}

.header--inf {
  padding: 8px 10px;
  text-align: center;
  background-color: RGB(213, 184, 152);
  border-radius: 5px;
  margin: 10px 0;
  color: RGB(151, 99, 62);
  font-size: 1.5rem;
}

.scrollbar {
  background-color: RGB(252, 248, 239);
  max-height: 400px;
  margin: 20px 0;
  padding-right: 10px; /* Add padding to move scrollbar outward */
  overflow-y: auto;
  scrollbar-width: thin; /* For Firefox */
  scrollbar-color: RGB(151, 99, 62) RGB(252, 248, 239); /* Custom scrollbar color */
}

/* Custom scrollbar for WebKit browsers (Chrome, Safari) */
.scrollbar::-webkit-scrollbar {
  width: 8px; /* Thinner scrollbar */
}

.scrollbar::-webkit-scrollbar-track {
  background: RGB(252, 248, 239); /* Match background */
  border-radius: 10px;
}

.scrollbar::-webkit-scrollbar-thumb {
  background-color: RGB(151, 99, 62); /* Scrollbar color */
  border-radius: 10px;
  border: 2px solid RGB(252, 248, 239); /* Add border for spacing */
}

.force-overflow {
  min-height: 100px;
}

.order-item {
  margin-bottom: 20px;
}

.img-package-container {
  display: flex;
  align-items: center;
  margin-top: 20px;
}

.buy-now-item__img--package {
  position: relative;
  margin-right: 20px;
}

.img--package {
  width: 100px;
  height: 100px;
  object-fit: cover;
  border-radius: 10px;
}

.amount-img-package {
  position: absolute;
  top: -10%;
  right: -8%;
  background-color: RGB(135, 100, 68);
  color: #fff;
  padding: 2px 8px;
  border-radius: 100%;
  font-size: 0.9rem;
}

.buy-now-item__name--package {
  flex: 1;
  font-size: 1.2rem;
}

.name--package {
  font-weight: bold;
  color: RGB(151, 99, 62);
  margin-bottom: 5px;
}

.buy-now-item__name--package p {
  margin: 5px 0;
}

.buy-now-item__cost--package {
  font-size: 1.2rem;
  color: brown;
}

.cost--package {
  color: brown;
  font-weight: bold;
}

.button-order {
  display: block;
  margin: 10px auto;
  padding: 10px 20px;
  border: none;
  border-radius: 15px;
  background-color: RGB(151, 99, 62);
  color: white;
  cursor: pointer;
  font-size: 1.2rem;
  transition: background-color 0.3s;
}

.button-order:hover {
  background-color: RGB(135, 100, 68);
}

.payment-detail-container {
  margin-top: 20px;
}

.payment-detail-content__item {
  display: flex;
  justify-content: space-between;
  font-size: 1.2rem;
  margin: 15px 0;
}

.payment-detail-content__item--cost {
  color: brown;
  font-weight: bold;
}

hr {
  width: 85%;
  border: 1px solid rgb(117, 110, 110);
  margin: 20px auto;
}

.status-message {
  text-align: center;
  font-size: 1.2rem;
  padding: 20px;
  color: RGB(151, 99, 62);
}

.status-message.error {
  color: red;
}

.button-continue-shopping {
  display: inline-block;
  margin: 10px auto;
  padding: 10px 20px;
  border-radius: 15px;
  background-color: RGB(151, 99, 62);
  color: white;
  text-decoration: none;
  font-size: 1.2rem;
  transition: background-color 0.3s;
}

.button-continue-shopping:hover {
  background-color: RGB(135, 100, 68);
}

/* Responsive */
@media screen and (max-width: 800px) {
  .navbar {
    height: 50px; /* Revert height for mobile */
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

  .navbarವ

  .navbar-logo {
    display: none;
  }

  main {
    padding-top: 200px;
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

  .buy-now {
    flex-direction: column;
    gap: 10px;
  }

  .buy-now-item {
    border-right: none;
    border-bottom: 1px solid black;
    max-width: 100%; /* Full width on mobile */
  }

  .email-phone {
    flex-direction: column;
  }

  .input--email--buy-now,
  .input--phone--buy-now {
    width: 100%;
  }

  .img-package-container {
    flex-direction: column;
    align-items: flex-start;
  }

  .buy-now-item__img--package {
    margin-bottom: 10px;
  }
}
</style>