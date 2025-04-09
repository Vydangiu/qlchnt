<template>
  <div>
      <h1>Admin Dashboard</h1>
      <nav>
          <ul>
              <li><router-link to="/admin/dashboard">Dashboard</router-link></li>
              <li><router-link to="/admin/products">Products</router-link></li>
              <li><router-link to="/admin/categories">Categories</router-link></li>
              <li><router-link to="/admin/orders">Orders</router-link></li>
              <li><router-link to="/admin/users">Users</router-link></li>
              <li><button @click="logout">Logout</button></li>
          </ul>
      </nav>

      <router-view></router-view> <!-- Nơi hiển thị các component con -->
  </div>
</template>

<script setup>
import { useAuthStore } from '@/store/auth';
import { useRouter } from 'vue-router';

const authStore = useAuthStore();
const router = useRouter();

const logout = () => {
  authStore.logout();
  router.push('/login'); // Chuyển hướng về trang đăng nhập
};
</script>


<style scoped>
nav ul {
  list-style: none;
  padding: 0;
}

nav ul li {
  display: inline;
  margin-right: 20px;
}
</style>