<template>
    <div class="wrapper">
        <header class="menu-toggle">
            <div class="navbar">
                <div class="navbar-link">
                    <ul class="navbar-link-item" :class="{ 'active': isOpen }">
                        <li class="item-link"><a class="link" href="/"> Trang chủ</a></li>
                        <li class="item-link"><a class="link" href="Product">Sản phẩm</a></li>
                        <li class="item-link"><a class="link" href="Blog"> About</a></li>
                        <li class="item-link"><a class="link" href="contact">Liên hệ</a></li>
                    </ul>
                </div>
                <div class="navbar-logo">
                    <img class="logo" src="@/assets/IMG/logo1.jpg" alt="logo">
                </div>
                <div class="navbar-search">
                    <input type="text" class="search-input" placeholder="Tìm kiếm">
                    <div class="icon-search">
                        <a class="link" href=""><i class="fa-solid fa-magnifying-glass"></i></a>
                    </div>
                </div>
                <div class="navbar-cart-login-icon">
                    <a style="font-size: 2rem;" href="/cart">
            <i class="fa-solid fa-bag-shopping"></i>
          </a>
          <!-- Thêm icon đơn hàng -->
          <a style="font-size: 2rem;" href="/orders">
            <i class="fa-solid fa-clipboard-list"></i>
          </a>
          <div v-if="user" class="user-info">
            <a class="user-hello" style="font-size: 2rem; cursor: pointer;" @click="logout">
              <i style="margin-top: 40px" class="fa-solid fa-user"></i>
              <span style="font-size: 1rem; display: inline-flex; margin-left: 5%;">Xin chào <br>
                {{ user.username }}</span>
            </a>
          </div>
          <a v-else style="font-size: 2rem; padding-bottom: 10px;" href="signin">
            <i class="fa-solid fa-user"></i>
          </a>
                </div>
            </div>

        </header>
    </div>

    <!-- product -->
    <div class="product-list">
        <h1 class="title-product">Danh Sách Sản Phẩm</h1>
        <div class="filters">
            <label>
                <input type="text" v-model="searchQuery" placeholder="Tìm kiếm sản phẩm..." @input="fetchProducts" />
            </label>
            <label>
                <select v-model="selectedCategory" @change="fetchProducts">
                    <option value="">Tất cả danh mục</option>
                    <option v-for="category in categories" :key="category.id" :value="category.id">{{ category.name }}
                    </option>
                </select>
            </label>
            <label>
                <input type="number" v-model="minPrice" placeholder="Giá tối thiểu" @input="fetchProducts" />
            </label>
            <label>
                <input type="number" v-model="maxPrice" placeholder="Giá tối đa" @input="fetchProducts" />
            </label>
        </div>

        <div v-if="loading">Đang tải sản phẩm...</div>
        <div v-else-if="error" class="error">{{ error }}</div>
        <div v-else class="products-container">
            <div v-for="product in products" :key="product.id" class="product-card">
                <img class="product-image" :src="getProductImage(product)" :alt="product.name"
                    @click="goToProductDetail(product.id)" />
                <div class="product-info">
                    <h3 style="line-height: none" @click="goToProductDetail(product.id)">{{ product.name }}</h3>
                    <p class="price">{{ formatPrice(product.price) }}</p>
                    <p class="bought"><i>Đã bán: {{ product.sold }}</i></p>

                    <div class="product-actionst">
                    <button class="cart-button" @click.stop="addToCart(product)">
                        🛒 Thêm vào giỏ
                    </button>
                    <button class="buy-now-button" @click.stop="buyNow(product)">
                        ⚡ Mua Ngay
                    </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from "axios";

export default {
    data() {
        return {
            products: [],
            categories: [],
            searchQuery: "",
            selectedCategory: "",
            minPrice: "",
            maxPrice: "",
            loading: true,
            error: null,
            cart: [],
            isOpen: false,
        };
    },
    computed: {
        user() {
            return JSON.parse(localStorage.getItem("user"));
        },
        token() {
            return localStorage.getItem("access_token");
        }
    },
    methods: {
        toggleMenu() {
            this.isOpen = !this.isOpen;
        },

        async fetchProducts() {
            this.loading = true;
            try {
                const params = {
                    category: this.selectedCategory,
                    search: this.searchQuery,
                    min_price: this.minPrice,
                    max_price: this.maxPrice,
                };
                const response = await axios.get("http://127.0.0.1:8000/api/products/", { params });
                this.products = response.data;
            } catch (err) {
                this.error = "Lỗi khi tải sản phẩm!";
            } finally {
                this.loading = false;
            }
        },

        async fetchCategories() {
            try {
                const response = await axios.get("http://127.0.0.1:8000/api/categories/");
                this.categories = response.data;
            } catch (err) {
                console.error("Lỗi khi tải danh mục sản phẩm", err);
            }
        },

        getProductImage(product) {
            if (product && product.images && product.images.length > 0) {
                let imageUrl = product.images[0].image_url;
                if (imageUrl.startsWith("http")) return imageUrl;
                return `http://127.0.0.1:8000/product_images/${imageUrl.split("/").pop()}`;
            }
            return "/default-image.jpg";
        },

        formatPrice(price) {
            return new Intl.NumberFormat("vi-VN", { style: "currency", currency: "VND" }).format(price);
        },

        goToProductDetail(productId) {
            this.$router.push(`/products/${productId}/`);
        },

        addToCart(product) {
            const token = localStorage.getItem("access_token");
            const user = JSON.parse(localStorage.getItem("user"));

            if (!token || !user) {
                alert("Bạn cần đăng nhập để thêm vào giỏ hàng!");
                this.$router.push("/signin");
                return;
            }

            let cartKey = `cart_${user.id}`;
            let cart = JSON.parse(localStorage.getItem(cartKey)) || [];
            let existingItem = cart.find((item) => item.id === product.id);

            if (existingItem) {
                existingItem.quantity += 1;
            } else {
                cart.push({ ...product, quantity: 1 });
            }

            localStorage.setItem(cartKey, JSON.stringify(cart));
            alert("Đã thêm vào giỏ hàng!");
        },

        async buyNow(product) {
            const token = localStorage.getItem("access_token");
            const user = JSON.parse(localStorage.getItem("user"));

            if (!token || !user) {
                alert("Bạn cần đăng nhập để mua sản phẩm!");
                this.$router.push("/signin");
                return;
            }

            // Chuyển hướng đến checkout với productId và buyNow=true
            this.$router.push({
                path: '/checkout',
                query: { buyNow: 'true', productId: product.id }
            });
        }
    },
    created() {
        this.fetchProducts();
        this.fetchCategories();
        const user = this.user;
        const cartKey = user ? `cart_${user.id}` : "cart";
        this.cart = JSON.parse(localStorage.getItem(cartKey)) || [];
    },
    watch: {
        $route(to, from) {
            this.fetchProducts();
        }
    }
};
</script>

<style>
.buy-now-button{
    padding: 0 1rem;
    color: RGB(255, 102, 0);
    font-weight: 700;
    border: 1px solid RGB(255, 102, 0);
    border-radius: 5px;

}
.buy-now-button:hover{
    background-color:rgba(233, 226, 175, 0.5);
    
}
.product-actionst {
    display: flex;
    justify-content: space-evenly;
    margin-top: 1rem;
   
}
.bought {
    margin-top: 0.5rem;
}

.product-list {
    padding: 1rem;
    position: relative;
    top: 8rem;
}

.product-info {
    background-color: RGB(239, 226, 209);
    padding: 12px 0;
}

.title-product {
    text-align: center;
    font-size: 2rem;
    font-weight: 600;
    margin-bottom: 1rem;
    padding: 0.5rem;
    margin-top: 30px;
    position: absolute;
    top: -7rem;
    display: block;
    width: 100%;
}

.filters {
    display: flex;
    justify-content: center;
    gap: 1rem;
    margin-bottom: 1rem;
}

.filters input,
.filters select {
    padding: 0.5rem;
    font-size: 1rem;
}

.products-container {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
    justify-content: center;
}

.product-card {
    border: 1px solid #ccc;
    padding: 1rem;
    width: 20rem;
    text-align: center;
    cursor: pointer;
    position: relative;
}

.product-image {
    width: 18rem;
    height: 17rem;
}

.product-info h3 {
    margin: 0;
    padding: 6px;
    font-size: 1.4rem;
    font-weight: 500;
}

.price {
    color: red;
    font-weight: bold;
}

.error {
    color: red;
    text-align: center;
}

.cart-button {
    padding: 8px;
    background-color: #ff6600;
    color: white;
    border: none;
    cursor: pointer;
    font-weight: bold;
    border-radius: 5px;
}

@media screen and (max-width: 800px) {
    .navbar-search {
        display: none !important;
    }

    .search-input {
        display: none;
    }

    .navbar-cart-login-icon {
        display: none !important;
    }

    .navbar-logo {
        display: none;
    }

    .product-list {
        margin-top: 120px;
    }

    main {
        padding-top: 200px;
    }

    .navbar-link {
        background-color: var(--color-primary);
        width: 100% !important;
        position: fixed;
        top: 20px;
        left: 0;
        right: 0;
        flex-wrap: wrap;
    }

    .navbar-link-item {
        flex-direction: column;
        align-items: center;
    }

    .navbar-link-item.active {
        display: flex;
    }
}

.cart-button:hover {
    background-color: #ff4500;
}
</style>