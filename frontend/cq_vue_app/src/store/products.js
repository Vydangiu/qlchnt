import { defineStore } from 'pinia'
import axios from 'axios'

export const useProductStore = defineStore('products', {
  state: () => ({
    products: [],
    loading: false,
  }),
  actions: {
    async fetchProducts() {
      try {
        this.loading = true
        const response = await axios.get('/api/products/')
        this.products = response.data
      } catch (error) {
        console.error("Lỗi khi lấy sản phẩm:", error)
      } finally {
        this.loading = false
      }
    },
    async addProduct(newProduct) {
      try {
        await axios.post('/api/products/', newProduct)
        this.fetchProducts()  // Cập nhật danh sách sản phẩm sau khi thêm
      } catch (error) {
        console.error("Lỗi khi thêm sản phẩm:", error)
      }
    },
    async updateProduct(id, updatedProduct) {
      try {
        await axios.put(`/api/products/${id}/`, updatedProduct)
        this.fetchProducts()  // Cập nhật danh sách sau khi chỉnh sửa
      } catch (error) {
        console.error("Lỗi khi chỉnh sửa sản phẩm:", error)
      }
    },
    async deleteProduct(id) {
      try {
        await axios.delete(`/api/products/${id}/`)
        this.fetchProducts()  // Cập nhật lại danh sách sản phẩm
      } catch (error) {
        console.error("Lỗi khi xóa sản phẩm:", error)
      }
    },
  },
})
