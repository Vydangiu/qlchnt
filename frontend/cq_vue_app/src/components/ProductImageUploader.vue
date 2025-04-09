<template>
    <div>
      <h3>Thêm ảnh cho sản phẩm ID: {{ productId }}</h3>
      <form @submit.prevent="uploadImage">
        <input type="file" @change="handleFileChange" accept="image/*" />
        <button type="submit">Tải ảnh lên</button>
      </form>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import api from '@/services/api';
  
  const props = defineProps({
    productId: {
      type: Number,
      required: true,
    },
  });
  
  const emit = defineEmits(['image-uploaded']);
  
  const selectedFile = ref(null);
  
  const handleFileChange = (event) => {
    selectedFile.value = event.target.files[0];
  };
  
  const uploadImage = async () => {
    const formData = new FormData();
    formData.append('image', selectedFile.value);
    formData.append('product', props.productId); // Sử dụng props.productId
  
    try {
      await api.post('/product-images/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
  
      emit('image-uploaded');
    } catch (error) {
      console.error(error);
    }
  };
  </script>