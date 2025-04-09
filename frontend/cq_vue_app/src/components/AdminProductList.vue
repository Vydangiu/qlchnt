<template>
  <div class="p-6">
    <h2 class="text-2xl font-bold mb-4">Quản lý sản phẩm</h2>

    <!-- Form thêm/sửa sản phẩm -->
    <form @submit.prevent="submitForm" class="space-y-4 mb-8">
      <input v-model="form.name" placeholder="Tên sản phẩm" class="border p-2 w-full" />
      <input v-model="form.description" placeholder="Mô tả" class="border p-2 w-full" />
      <input v-model="form.price" type="number" placeholder="Giá" class="border p-2 w-full" />
      <input v-model="form.stock" type="number" placeholder="Số lượng" class="border p-2 w-full" />
      <input v-model="form.discount" type="number" placeholder="Giảm giá (%)" class="border p-2 w-full" />
      <input v-model="form.image" placeholder="URL ảnh" class="border p-2 w-full" />

      <button type="submit" class="bg-blue-600 text-white px-4 py-2 rounded">
        {{ isEditing ? 'Cập nhật' : 'Thêm mới' }}
      </button>
      <button v-if="isEditing" @click="cancelEdit" type="button" class="ml-2 text-gray-600">Huỷ</button>
    </form>

    <!-- Form tải ảnh lên (hiển thị sau khi thêm sản phẩm thành công) -->
    <ProductImageUploader v-if="newProductId" :productId="newProductId" @image-uploaded="handleImageUploaded" />

    <!-- Danh sách sản phẩm -->
    <table class="min-w-full border">
      <thead class="bg-gray-100">
        <tr>
          <th class="px-4 py-2 border">ID</th>
          <th class="px-4 py-2 border">Tên</th>
          <th class="px-4 py-2 border">Giá</th>
          <th class="px-4 py-2 border">Kho</th>
          <th class="px-4 py-2 border">Giảm giá</th>
          <th class="px-4 py-2 border">Ảnh</th>
          <th class="px-4 py-2 border">Hành động</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="product in products" :key="product.id">
          <td class="border px-4 py-2">{{ product.id }}</td>
          <td class="border px-4 py-2">{{ product.name }}</td>
          <td class="border px-4 py-2">{{ product.price }}</td>
          <td class="border px-4 py-2">{{ product.stock }}</td>
          <td class="border px-4 py-2">{{ product.discount }}%</td>
          <td class="border px-4 py-2">
            <img :src="product.images?.[0]?.image_url || 'URL_ẢNH_MẶC_ĐỊNH'" alt="ảnh" class="w-16 h-16 object-cover" />
          </td>
          <td class="border px-4 py-2">
            <button @click="editProduct(product)" class="text-blue-600 mr-2">Sửa</button>
            <button @click="deleteProduct(product.id)" class="text-red-600">Xoá</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/services/api'
import { useAuthStore } from '@/store/auth'
import ProductImageUploader from './ProductImageUploader.vue'; // Import ProductImageUploader

const API_URL = 'http://127.0.0.1:8000/api/products/'
const IMAGE_API_URL = 'http://127.0.0.1:8000/api/product-images/'

const products = ref([])
const images = ref([])

const form = ref({
  name: '',
  price: 0,
  stock: 0,
  discount: 0,
  description: '',
  image: ''
})

const isEditing = ref(false)
const editingId = ref(null)
const newProductId = ref(null) // State để lưu ID sản phẩm mới

const authStore = useAuthStore()

const fetchProducts = async () => {
  try {
    const res = await api.get(API_URL);
    products.value = res.data;
  } catch (error) {
    console.error("Lỗi khi lấy dữ liệu sản phẩm:", error);
  }
};

const fetchImages = async () => {
  try {
    const res = await api.get(IMAGE_API_URL);
    images.value = res.data;
  } catch (error) {
    console.error("Lỗi khi lấy dữ liệu ảnh:", error);
  }
};

const submitForm = async () => {
  try {
    let response;
    if (isEditing.value) {
      // Cập nhật sản phẩm
      response = await api.put(`${API_URL}${editingId.value}/`, form.value);
      console.log("Sản phẩm đã được cập nhật thành công!");
    } else {
      // Thêm sản phẩm mới
      response = await api.post(API_URL, form.value);
      console.log("Sản phẩm đã được thêm mới thành công!");
      newProductId.value = response.data.id; // Lưu ID sản phẩm mới
    }

    // Reset form và tải lại dữ liệu
    resetForm();
    await fetchProducts();
    await fetchImages();
  } catch (error) {
    console.error("Lỗi khi thêm/cập nhật sản phẩm:", error);
    alert("Đã có lỗi xảy ra khi thêm/cập nhật sản phẩm. Vui lòng kiểm tra console để biết thêm chi tiết.");
  }
};

const editProduct = (product) => {
  form.value = {
    name: product.name,
    description: product.description,
    price: product.price,
    stock: product.stock,
    discount: product.discount,
    image: product.images?.[0]?.image_url || ''
  };
  isEditing.value = true
  editingId.value = product.id
  newProductId.value = null; // Ẩn form tải ảnh
}

const deleteProduct = async (id) => {
  if (confirm('Bạn có chắc muốn xoá sản phẩm này?')) {
    try {
      await api.delete(`${API_URL}${id}/`);
      console.log("Sản phẩm đã được xóa thành công!");
      await fetchProducts();
      await fetchImages();
    } catch (error) {
      console.error("Lỗi khi xóa sản phẩm:", error);
      alert("Đã có lỗi xảy ra khi xóa sản phẩm. Vui lòng kiểm tra console để biết thêm chi tiết.");
    }
  }
}

const resetForm = () => {
  form.value = {
    name: '',
    price: 0,
    stock: 0,
    discount: 0,
    description: '',
    image: ''
  }
  isEditing.value = false
  editingId.value = null
  newProductId.value = null; // Ẩn form tải ảnh
}

const cancelEdit = () => {
  resetForm();
}

const handleImageUploaded = () => {
  // Gọi fetchImages để cập nhật danh sách ảnh sau khi tải lên thành công
  fetchImages();
};


onMounted(async () => {
  await fetchProducts()
  await fetchImages()
})
</script>