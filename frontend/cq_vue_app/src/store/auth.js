import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { ref } from 'vue' 

export const useAuthStore = defineStore('auth', () => { // Arrow function syntax
  const token = ref(localStorage.getItem('token') || null)
  const isAuthenticated = ref(!!token.value)
  const loading = ref(false)
  const error = ref(null)
  const router = useRouter()

  const setToken = (newToken) => {
    token.value = newToken
    localStorage.setItem('token', newToken)
    isAuthenticated.value = true
    axios.defaults.headers.common['Authorization'] = `Bearer ${newToken}` // Set Axios header
  }

  const clearToken = () => {
    token.value = null
    localStorage.removeItem('token')
    isAuthenticated.value = false
    delete axios.defaults.headers.common['Authorization'] // Clear Axios header
  }

  const login = async (username, password) => {
    loading.value = true
    error.value = null
    try {
      const res = await axios.post('http://127.0.0.1:8000/api/token/', { username, password })
      const accessToken = res.data.access
      setToken(accessToken) // Lưu access token
      router.push('/admin/dashboard') // Điều hướng sau khi đăng nhập thành công
      return true // Trả về true khi đăng nhập thành công
    } catch (err) {
      error.value = err.response?.data?.detail || 'Đăng nhập thất bại' // Lấy thông báo lỗi từ API
      console.error('Lỗi đăng nhập:', err)
      clearToken() // Xóa token nếu đăng nhập thất bại
      return false // Trả về false khi đăng nhập thất bại
    } finally {
      loading.value = false
    }
  }

  const logout = () => {
    clearToken()
    router.push('/login') // Điều hướng sau khi đăng xuất
  }

  return { token, isAuthenticated, loading, error, login, logout }
})