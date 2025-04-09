// services/api.js
import axios from 'axios';
import { useAuthStore } from '@/store/auth'; // Import auth store

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/', // Base URL của API
  headers: {
    'Content-Type': 'application/json',
  },
});

// Thêm interceptor để tự động thêm token vào header
api.interceptors.request.use(
  (config) => {
    const authStore = useAuthStore();
    const token = authStore.token;
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Thêm interceptor để xử lý lỗi 401 (Unauthorized)
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      const authStore = useAuthStore();
      // Xử lý lỗi 401: có thể logout hoặc thử refresh token (nếu có)
      console.error("Lỗi 401: Unauthorized.  Bạn cần đăng nhập lại hoặc refresh token.");
      authStore.logout();
      // Chuyển hướng đến trang đăng nhập (nếu cần)
      window.location.href = '/login'; // Sử dụng window.location.href thay vì router.push bên ngoài component
    }
    return Promise.reject(error);
  }
);

export default api;