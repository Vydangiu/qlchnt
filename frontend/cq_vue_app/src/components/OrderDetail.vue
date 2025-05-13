<template>
    <div class="order-detail">
      <h1>Chi tiết đơn hàng #{{ orderId }}</h1>
      <div v-if="order">
        <p><strong>Khách hàng:</strong> {{ order.name }}</p>
        <p><strong>Số điện thoại:</strong> {{ order.phone_number }}</p>
        <p><strong>Địa chỉ giao hàng:</strong> {{ order.shipping_address }}</p>
        <p><strong>Ghi chú:</strong> {{ order.note || 'Không có' }}</p>
        <p><strong>Phương thức thanh toán:</strong> {{ order.payment_method === 'cod' ? 'Thanh toán khi nhận hàng' : 'Chuyển khoản' }}</p>
        <p><strong>Trạng thái:</strong> {{ order.status }}</p>
        <h3>Sản phẩm:</h3>
        <table class="items-table">
          <thead>
            <tr>
              <th>Sản phẩm</th>
              <th>Số lượng</th>
              <th>Giá</th>
              <th>Tổng</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in order.items" :key="item.id">
              <td>{{ item.product.name }}</td>
              <td>{{ item.quantity }}</td>
              <td>{{ formatPrice(item.product.price) }}</td>
              <td>{{ formatPrice(item.product.price * item.quantity) }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <p v-else>Lỗi: Không thể tải chi tiết đơn hàng!</p>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        orderId: this.$route.params.id,
        order: null,
      };
    },
    methods: {
      async fetchOrder() {
        try {
          const token = localStorage.getItem('access_token');
          const response = await axios.get(`http://127.0.0.1:8000/api/orders/${this.orderId}/`, {
            headers: { Authorization: `Bearer ${token}` },
          });
          this.order = response.data;
        } catch (error) {
          console.error('Lỗi khi lấy chi tiết đơn hàng:', error);
        }
      },
      formatPrice(price) {
        return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(price);
      },
    },
    created() {
      this.fetchOrder();
    },
  };
  </script>
  
  <style scoped>
  .order-detail {
    max-width: 900px;
    margin: 0 auto;
    padding: 20px;
  }
  
  .items-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 10px;
  }
  
  .items-table th,
  .items-table td {
    padding: 10px;
    border: 1px solid #ddd;
    text-align: center;
  }
  </style>