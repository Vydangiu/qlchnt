<template>
    <div>
      <h3>{{ isEditMode ? 'Sửa Sản phẩm' : 'Thêm Sản phẩm' }}</h3>
      <form @submit.prevent="submitForm">
        <label for="name">Tên sản phẩm:</label>
        <input v-model="product.name" id="name" required />
        
        <label for="price">Giá:</label>
        <input v-model="product.price" id="price" type="number" required />
        
        <label for="stock">Kho:</label>
        <input v-model="product.stock" id="stock" type="number" required />
        
        <label for="discount">Giảm giá:</label>
        <input v-model="product.discount" id="discount" type="number" />
        
        <label for="description">Mô tả:</label>
        <textarea v-model="product.description" id="description"></textarea>
        
        <button type="submit">{{ isEditMode ? 'Cập nhật' : 'Thêm' }}</button>
      </form>
      <button @click="$emit('closeForm')">Đóng</button>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      product: {
        type: Object,
        required: true,
      },
    },
    computed: {
      isEditMode() {
        return !!this.product.id
      }
    },
    methods: {
      submitForm() {
        this.$emit('saveProduct', this.product)
      },
    }
  }
  </script>
  