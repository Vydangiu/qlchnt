// components/Login.vue
<template>
  <div>
    <h1>Đăng nhập</h1>
    <div v-if="authStore.error" class="error-message">
      {{ authStore.error }}
    </div>
    <form @submit.prevent="handleSubmit">
      <div>
        <label for="username">Tên đăng nhập:</label>
        <input type="text" id="username" v-model="username" />
      </div>
      <div>
        <label for="password">Mật khẩu:</label>
        <input type="password" id="password" v-model="password" />
      </div>
      <button type="submit" :disabled="authStore.loading">
        {{ authStore.loading ? 'Đang đăng nhập...' : 'Đăng nhập' }}
      </button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useAuthStore } from '@/store/auth';

const username = ref('');
const password = ref('');
const authStore = useAuthStore();

const handleSubmit = async () => {
  // Đăng nhập và kiểm tra kết quả
  const success = await authStore.login(username.value, password.value);
  if (!success) {
    // Xử lý lỗi nếu đăng nhập thất bại (ví dụ: hiển thị thông báo)
    console.error('Đăng nhập thất bại');
  }
};
</script>

<style scoped>
.error-message {
  color: red;
}
</style>