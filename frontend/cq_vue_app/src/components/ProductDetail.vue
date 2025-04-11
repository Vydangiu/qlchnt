<template>
  <header class="menu-toggle" >
      <div class="navbar" >
          <div class="navbar-link" >
              <ul class="navbar-link-item"  :class="{ 'active': isOpen }">
                  <li class="item-link"> <a class="link" href="/"> Trang chủ</a></li>
                  <li class="item-link"> <a class="link" href="Product">Sản phẩm</a> </li>
                  <li class="item-link"> <a class="link" href="Blog"> About</a></li>
                  <li class="item-link"> <a class="link" href="contact">Liên hệ</a> </li>
              </ul>
          </div>
          <div class="navbar-logo">
              <img class="logo" src="@/assets/IMG/logo1.jpg" alt="logo">
          </div>
          <div class="navbar-search">
            <input type="text" v-model="navbarSearch" class="search-input" placeholder="Tìm kiếm" @keyup.enter="searchFromNavbar" />
            <div class="icon-search">
              <a class="link" href="#" @click.prevent="searchFromNavbar">
                <i class="fa-solid fa-magnifying-glass"></i>
              </a>
            </div>
          </div>
          <div class="navbar-cart-login-icon">
            <a style="font-size: 2rem;" href="/cart"> 
                <i class="fa-solid fa-bag-shopping"></i>
            </a>
            
            <div v-if="user" class="user-info">
              
                <a class="user-hello" style="font-size: 2rem;  cursor: pointer;" @click="logout">
                    <i style="margin-top: 40px" class="fa-solid fa-user"></i>
                    <span style="font-size: 1rem; display: inline-flex;margin-left: 20%;"> Xin chào, {{ user.username }} </span>
                  
                </a>  
            </div>
            <a v-else style="font-size: 2rem; padding-bottom: 10px;" href="signin">
                <i class="fa-solid fa-user"></i>
            </a>
          </div>



      </div>
      <div class="hamburger" @click="toggleMenu">☰</div>
  </header>
    <div class="product-detail" v-if="product">
        
          <img class="product-image" :src="getProductImage(product)" :alt="product.name" />
        
        <div class="product-info">
          <h1>{{ product.name }}</h1>
          <div class="cost-container">
          <p>Giá bán:</p>
          <p class="price">{{ formatPrice(product.price) }}</p>
        </div>
          <p class="product-description" v-if="product.description">{{ product.description }}</p>
          <p><i>Đã bán: {{ product.sold }}</i></p>
          <button class="cart-button2" @click="addToCart(product)">THÊM VÀO GIỎ HÀNG</button>
          <button class="button-group__buy" type="submit"><a style="text-decoration: none; color: white" href="/shop_cart">MUA NGAY</a> </button>
         </div>
    </div>

    <div v-else-if="loading">Đang tải...</div>
    <div v-else>Lỗi khi tải sản phẩm.</div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        product: null,
        loading: true,
      };
    },
    methods: {
      async fetchProduct() {
        try {
          const id = this.$route.params.id;
          const response = await axios.get(`http://127.0.0.1:8000/api/products/${id}/`);
          this.product = response.data;
        } catch (err) {
          console.error('Lỗi khi lấy thông tin sản phẩm:', err);
        } finally {
          this.loading = false;
        }
      },
      getProductImage(product) {
        if (product && product.images && product.images.length > 0) {
          let imageUrl = product.images[0].image_url;
          if (imageUrl.startsWith('http')) return imageUrl;
          return `http://127.0.0.1:8000/product_images/${imageUrl.split('/').pop()}`;
        }
        return '/default-image.jpg';
      },
      formatPrice(price) {
        return new Intl.NumberFormat("vi-VN", { style: "currency", currency: "VND" }).format(price);
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
      }
    },
    created() {
      this.fetchProduct();
    }
  };
  </script>
  
  <style scoped>
  .button-group__buy {
    border-style: none;
    display: flex
;
    margin: 1rem auto;
    padding: 7px 46px;
    background-color:RGB(240, 104, 56);
    color: white;
    cursor: pointer;
    font-weight: bold;
    border-radius: 5px;


    
  }
  .button-group__buy:hover {
    background-color: rgba(240, 104, 56, 0.8);
  }
  .cost-container{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 1rem;
  }
  .product-detail {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    padding: 2rem;
   
  }
  
  .product-image{
    width: 35rem;
    height: 35rem;
  }
  
  .product-info {
    max-width: 35rem;
    padding: 0 2rem;
    height: 35rem;
  }
  
  .price {
    color: red;
    font-size: 1.5rem;
    font-weight: bold;
  }
  
  .cart-button2 {
    display: flex;
    margin: 1rem auto;
    padding: 10px 20px;
    background-color: RGB(140, 70, 19);
    color: white;
    border: none;
    cursor: pointer;
    font-weight: bold;
    border-radius: 5px;
  }
  
  .cart-button2:hover {
    background-color:RGBA(140, 70, 19, 0.8);
  }
  
  .product-description{
    margin: 2rem;
  }

  @media screen and (max-width: 800px) 
{

    .navbar-search{
        display: none !important;
    }
    .search-input{
        display: none;
    }
    .navbar-cart-login-icon{
        display: none !important;
    }
    .navbar-logo{

        display: none;
    }

    main{
    padding-top: 200px;
  }
  .navbar-link {
   
   
    background-color: var(--color-primary);
    width: 100% !important;; /* Chiều rộng 100% */
    /* padding-top: 30px; */
    position: fixed; /* Tuyệt đối */
    top: 20px; /* Cách top 50px */
    left: 0; /* Cách trái 0px */
    right: 0;
    flex-wrap: wrap;
  }
  .navbar-link-item {
    flex-direction: column;
    align-items: center; /* Căn giữa nội dung */
   
  }
   
  .navbar-link-item.active {
     display: flex;
    
    }

 
}



.banner {
  margin-top: 20px;
}
.slider {
  position: relative;
  max-width: 100%;
  overflow: hidden;
}

.slides img {
  width: 100%;
  transition: opacity 0.5s ease-in-out;
}

.button-container {
  position: absolute;
  top: 50%;
  right: 20px;
  transform: translateY(-50%);
  cursor: pointer;
  font-size: 24px;
  color: black;
  background: rgba(255, 255, 255, 0.5);
  padding: 10px;
  border-radius: 50%;
}


*{
   
   /* padding: 0; */
   box-sizing: border-box;
 
}


body{
   background-color: RGB(243, 238, 234);
}
:root{
   /* màu nâu */
   --color-primary: RGB(138, 99, 68);


   --background-color: RGB(216, 206, 199);
}


/* header */
.navbar{
   width: 100%;
   height:50px;
   background-color: var(--color-primary);
   display: flex;
   align-items: center;
   font-size: 1.75rem;
   border-radius: 10px;
   position: fixed;  /* Cố định menu trên cùng */
    top: 0;           /* Gán vị trí trên cùng */
    left: 0;
    width: 100%;      /* Kéo dài toàn bộ chiều rộng */
    z-index: 1000;  /* Đặt lớp z-index cao nhất */
   
  

}
.product{
   display: flex;
   justify-content: space-around;
   margin-top: 2rem;
}




.navbar-link-item{
   display: flex;
   justify-content: space-between;
   margin: 0 ;
   font-size: 1.5rem;


}
.user-info{
  margin-top: 20px;
}

.item-link{
   list-style: none;
   margin: 0 20px;


}
.link{
   text-decoration: none;
   color: rgb(37, 36, 36);
   font-size: 1.5rem;
   white-space: nowrap;


}


.logo{
   width: 175px;
   height: 38px;
   margin-right: 40px;
}


.navbar-search{


  display: flex;
  background-color: white;;
  border-radius: 15px;
  outline-color: white;
  width: 35rem;


}
.search-input{
   border-style: none;
   border-radius: 15px;
   padding: 0 10px;
   width: 30rem;
}
.icon-search{
   border-left: 2px solid #3333;
   padding: 3px 20px;
   width: 5rem;
   
   
}
.navbar-cart-login-icon{
   margin: 1rem;
   margin: 1rem;
    display: flex;
    align-items: center;



}
.fa-bag-shopping{
   margin: 1rem;
}


/* main */


/* main{
   margin-top: 30px;
} */
.slider{
   width: 100%;
   height: 500px;;
   position: relative;
}
.banner-1{
   width: 100%;
   height: 500px;
   border-radius: 10px;
   
   
}



.button-container{
   display: flex;
   justify-content: space-between;
   color:rgb(105, 105, 104);
   font-size: 3rem;
   position:absolute ;
   top: 50%;
   right: 0;




}
.banner-2{
   width: 100%;
   height: 500px;
    border-radius: 10px;


}


/* demo product */


.demo-product{
    margin-top: 20px;
   display: flex;
   justify-content: space-between;
   flex-wrap: wrap;
   margin-left: 5px;
   
   
    
   
}
.demo-product-item{
   display: flex;
   justify-content: space-around;
   margin: 0 25px;
  

}


.img-demo{
    max-width: 315px;
    min-height: 10%;
    border-radius: 5px;
    margin-left: 9px;
}


.box{
   background-color: var(--color-primary);
   color: RGB(243, 238, 234);
   width: 20rem;
   height: 20rem;
   font-size: 1.5rem;
   line-height: 10px;
   margin-top: 5px;
   line-height: 2rem;
   padding:10px;
   border-style: 5px solid RGB(243, 238, 234);
   border-radius: 5px;


}
h3{
   margin:0;
   padding-bottom: 10px;


}


  </style>
  