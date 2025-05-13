<template>
    <div class="admin-orders">
      <h1>Quản lý đơn hàng</h1>
      <table class="orders-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Khách hàng</th>
            <th>Tổng tiền</th>
            <th>Trạng thái</th>
            <th>Ngày đặt</th>
            <th>Hành động</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="order in orders" :key="order.id">
            <td>{{ order.id }}</td>
            <td>{{ order.name }}</td>
            <td>{{ formatPrice(order.total) }}</td>
            <td>
              <select v-model="order.status" @change="updateOrderStatus(order)">
                <option value="Pending">Chờ xử lý</option>
                <option value="Processing">Đang xử lý</option>
                <option value="Shipped">Đã giao hàng</option>
                <option value="Completed">Hoàn thành</option>
                <option value="Cancelled">Đã hủy</option>
              </select>
            </td>
            <td>{{ order.created_at }}</td>
            <td>
              <button @click="viewOrderDetails(order.id)">Xem chi tiết</button>
              <button @click="notifyCustomer(order.id)">Gửi thông báo</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  
  export default {
    data() {
      return {
        orders: [],
        error: null,
      };
    },
    methods: {
      async fetchOrders() {
        try {
          const token = localStorage.getItem("access_token");
          const response = await axios.get("http://127.0.0.1:8000/api/orders/", {
            headers: { Authorization: `Bearer ${token}` },
          });
          this.orders = response.data;
        } catch (error) {
          this.error = "Không thể tải danh sách đơn hàng!";
        }
      },
  
      async updateOrderStatus(order) {
        try {
          const token = localStorage.getItem("access_token");
          await axios.patch(
            `http://127.0.0.1:8000/api/orders/${order.id}/`,
            { status: order.status },
            { headers: { Authorization: `Bearer ${token}` } }
          );
          alert(`Cập nhật trạng thái đơn hàng ${order.id} thành công!`);
        } catch (error) {
          this.error = "Không thể cập nhật trạng thái!";
        }
      },
  
      viewOrderDetails(orderId) {
        this.$router.push(`/admin/orders/${orderId}`);
      },
  
      async notifyCustomer(orderId) {
        try {
          const token = localStorage.getItem("access_token");
          await axios.post(
            `http://127.0.0.1:8000/api/orders/${orderId}/notify/`,
            {},
            { headers: { Authorization: `Bearer ${token}` } }
          );
          alert(`Đã gửi thông báo cho khách hàng!`);
        } catch (error) {
          this.error = "Không thể gửi thông báo!";
        }
      },
  
      formatPrice(price) {
        return new Intl.NumberFormat("vi-VN", { style: "currency", currency: "VND" }).format(price);
      },
    },
    created() {
      this.fetchOrders();
    },
  };
  </script>
  
  <style scoped>
  .admin-orders {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
  }
  
  .orders-table {
    width: 100%;
    border-collapse: collapse;
  }
  
  .orders-table th,
  .orders-table td {
    padding: 10px;
    border: 1px solid #ddd;
    text-align: center;
  }
  
  .orders-table th {
    background-color: #f5f5f5;
  }
  
  button {
    padding: 5px 10px;
    background-color: #ff6600;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  button:hover {
    background-color: #e65c00;
  }
  </style>