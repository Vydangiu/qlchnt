<template>
    <div class="product-detail" v-if="product">
      <div class="product-image">
        <img :src="getProductImage(product)" :alt="product.name" />
      </div>
      <div class="product-info">
        <h1>{{ product.name }}</h1>
        <p class="price">{{ formatPrice(product.price) }}</p>
        <p v-if="product.description">{{ product.description }}</p>
        <p><i>Đã bán: {{ product.sold }}</i></p>
        <button class="cart-button" @click="addToCart(product)">🛒 Thêm vào giỏ hàng</button>
      </div>
    </div>
    <div v-else-if="loading">Đang tải...</div>
    <div v-else>Lỗi khi tải sản phẩm.</div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        product: null,
        loading: true,
      };
    },
    methods: {
      async fetchProduct() {
        try {
          const id = this.$route.params.id;
          const response = await axios.get(`http://127.0.0.1:8000/api/products/${id}/`);
          this.product = response.data;
        } catch (err) {
          console.error('Lỗi khi lấy thông tin sản phẩm:', err);
        } finally {
          this.loading = false;
        }
      },
      getProductImage(product) {
        if (product && product.images && product.images.length > 0) {
          let imageUrl = product.images[0].image_url;
          if (imageUrl.startsWith('http')) return imageUrl;
          return `http://127.0.0.1:8000/product_images/${imageUrl.split('/').pop()}`;
        }
        return '/default-image.jpg';
      },
      formatPrice(price) {
        return new Intl.NumberFormat("vi-VN", { style: "currency", currency: "VND" }).format(price);
      },
      addToCart(product) {
        const token = localStorage.getItem("access_token");
        const user = JSON.parse(localStorage.getItem("user"));
        if (!token || !user) {
          alert("Bạn cần đăng nhập để thêm vào giỏ hàng!");
          this.$router.push("/signin");
          return;
        }
        let cartKey = `cart_${user.id}`;
        let cart = JSON.parse(localStorage.getItem(cartKey)) || [];
        let existingItem = cart.find((item) => item.id === product.id);
        if (existingItem) {
          existingItem.quantity += 1;
        } else {
          cart.push({ ...product, quantity: 1 });
        }
        localStorage.setItem(cartKey, JSON.stringify(cart));
        alert("Đã thêm vào giỏ hàng!");
      }
    },
    created() {
      this.fetchProduct();
    }
  };
  </script>
  
  <style scoped>
  .product-detail {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    padding: 2rem;
    margin-top: 100px;
  }
  
  .product-image img {
    width: 400px;
    height: auto;
    margin-right: 2rem;
  }
  
  .product-info {
    max-width: 500px;
  }
  
  .price {
    color: red;
    font-size: 1.5rem;
    font-weight: bold;
  }
  
  .cart-button {
    margin-top: 1rem;
    padding: 10px 20px;
    background-color: #ff6600;
    color: white;
    border: none;
    cursor: pointer;
    font-weight: bold;
    border-radius: 5px;
  }
  
  .cart-button:hover {
    background-color: #ff4500;
  }
  </style>
  