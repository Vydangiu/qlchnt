<template>
   <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
  <div class="wrapper">
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
</div>
<main>

  <!-- banner -->
<div class="banner">
  <div class="button-signup">
                
                <a href="">Signup</a>
                </div>
    <section class="slider">
      <div class="slides">
        <img v-show="currentSlide === 1" class="banner-1" src="@/assets/IMG/bann1.jpg" alt="Hình 1">
        <img v-show="currentSlide === 2" class="banner-2" src="@/assets/IMG/bann2-1.jpg" alt="Hình 2">
      </div>
      <div class="button-container">
        <i @click="nextSlide" class="fa-solid fa-arrow-right"></i>
      </div>
    </section> 
  </div>

<div style="margin-bottom: 25px;" class="demo-product">
                <div class="demo-product">
                    <div class="demo-product-item">
                        <img class="img-demo" src="@/assets/IMG/ban-an.jpg" alt="Hình 1">
                    </div>
                    <div class="demo-product-item">
                        <img class="img-demo" src="@/assets/IMG/ghe1.jpg" alt="Hình 1">
                    </div>
                    <div class="demo-product-item">
                    <div class="box"><h3> Moda Casa</h3>  Nâng tầm phong cách sống với nội thất đẳng cấp, nơi mọi chi tiết đẳng cấp đều tạo nên sự khác biệt</div>
                     </div>
                    <div class="demo-product-item">
                        <img class="img-demo" src="@/assets/IMG/ghe2.jpg" alt="Hình 1">
                    </div>
                   
                
  </div>
</div>
<p class="title-product1">Gợi ý cho bạn</p>
<div class="product">
    
      
      <div v-if="loading">Đang tải sản phẩm...</div>
      <div v-else-if="error" class="error">{{ error }}</div>
      <div v-else class="product-item-container">
        <div v-for="product in products.slice(0, 4)" :key="product.id" class="product-item">
          <a @click.prevent="goToProductDetail(product.id)">
            <img class="img-product" :src="getProductImage(product)" :alt="product.name" />
            <div class="cost">
              <p class="float">{{ product.name }}<br>
                <span style="color: red;">{{ formatPrice(product.price) }}</span>
              </p>
              <div class="evaluate">
                <!-- <ul class="evaluate_star">
                  <li v-for="star in 5" :key="star">
                    <i :class="{'fa-solid fa-star': star <= product.rating, 'fa-regular fa-star': star > product.rating}" style="color: yellow;"></i>
                  </li>
                </ul> -->
                
                  <button class="cart-button" @click.stop="addToCart(product)">
                    🛒 Thêm vào giỏ
                 </button>
                
                <ul class="buy">
                  <li>Đã bán {{ product.sold }}</li>
                </ul>
              </div>
            </div>
          </a>
        </div>
      </div>
    </div>
  
  <footer>
      <div class="container-footer">
          <p class="title-footer">Vì sao nên chọn Moda Casa</p>

          <div >
              <div class="feature-footer" >
                  
                          <div class="feature-footer-item">
                              <i class="icon-feature fa-solid fa-truck-fast"></i>
                              <p class="text-feature">Giao hàng và lắp đặt miễn phí</p>
                          </div>
                      
                          <div class="feature-footer-item">
                              <i class="icon-feature fa-solid fa-arrows-rotate"></i>
                              <p class="text-feature">30 ngày đổi trả miễn phí</p>
                          </div>
                     
                          <div class="feature-footer-item">
                              <i class="icon-feature fa-solid fa-headphones"></i>
                              <p class="text-feature">Tư vấn thiết kế miễn phí</p>
                          </div>
                      
                         
                          <div class="feature-footer-item">
                              <i class="icon-feature fa-solid fa-circle-check"></i>
                              <p class="text-feature">Thương hiệu uy tín toàn cầu</p>
                          </div>
                   
              </div>
         </div>
      </div>


      <div class="blog-footer">
              <div style="padding-left: 1.7rem;" class="side sidebar1">
                  <p class="header-feature"> Moda Casa</p>
                  <p style="   line-height: 30px;
                              padding-top: 1rem;
                                  " class="text-header-feature">
              Nội thất Moda Casa là thương hiệu đến từ Việt Nam với hơn 20 năm kinh nghiệm trong việc sản xuất và xuất khẩu nội thất đạt chuẩn quốc tế</p>
              </div>
              <div class="side sidebar2">
                  <p style="    padding-left: 1rem;" class="header-feature">Dịch vụ</p>
                  <ul style="line-height: 30px;
                              padding-top: 1rem;
                              " class="text-header-feature">
                      <li>Chính sách bán hàng</li>
                      <li>Chính sách giao hàng & lắp đặt</li>
                      <li>Chính sách bảo hàng & bảo trì</li>
                      <li>Chính sách đổi trả</li>
                  </ul>
              </div>
              <div class="side sidebar3">
                  <p style="padding-left: 2rem;" class="header-feature">Thông tin liên hệ</p>
                  <ul class="text-header-feature">
                      <li class="text-header-feature-item">
                          <i  class="icon-item fa-solid fa-location-dot"></i>
                          <p>Địa chỉ: 140 đường Nguyễn Hữu Thọ, quận 7, TP.HCM</p>
                      </li>
                      <li class="text-header-feature-item">
                          <i  class="icon-item fa-solid fa-phone-volume"></i>
                          <p>0878786523</p>
                      </li>
                      <li class="text-header-feature-item">
                          <i  class="icon-item fa-regular fa-envelope"></i>
                          <p>cskh@gmail.vn</p>
                      </li>
                  </ul>
              </div>
          </div>
       
</footer>
</main> 

</template>  

<script>
import axios from "axios";

export default {
  data() {
    return {
      products: [],
      loading: true,
      error: null,
      currentSlide: 1, // Bắt đầu từ slide 1
      totalSlides: 2 ,  // Có tổng cộng 2 slide
      navbarSearch: "", // input thanh search navbar

    };
    
  },
  mounted() {
    // Chuyển tự động sang slide 2 sau 5 giây
    setTimeout(() => {
      this.currentSlide = 2;
    }, 5000);
  },

  methods: {
    async searchFromNavbar() {
  if (!this.navbarSearch.trim()) {
    this.fetchProducts(); // nếu không nhập gì thì load lại tất cả
    return;
  }

  this.loading = true;
  try {
    const response = await axios.get("http://127.0.0.1:8000/api/products/", {
      params: {
        search: this.navbarSearch
      }
    });
    this.products = response.data;
  } catch (err) {
    this.error = "Lỗi khi tìm kiếm sản phẩm!";
  } finally {
    this.loading = false;
  }
},

    async fetchProducts() {
      this.loading = true;
      try {
        const response = await axios.get("http://127.0.0.1:8000/api/products/");
        this.products = response.data;
      } catch (err) {
        this.error = "Lỗi khi tải sản phẩm!";
      } finally {
        this.loading = false;
      }
    },
    nextSlide() {
      console.log("Before Click:", this.currentSlide);
      this.currentSlide = this.currentSlide === 1 ? 2 : 1;
      console.log("After Click:", this.currentSlide);
    },
    getProductImage(product) {
      if (product && product.images && product.images.length > 0) {
        let imageUrl = product.images[0].image_url;
        return imageUrl.startsWith("http") ? imageUrl : `http://127.0.0.1:8000/product_images/${imageUrl.split('/').pop()}`;
      }
      return "/default-image.jpg";
    },
    goToProductDetail(productId) {
      this.$router.push(`/products/${productId}`);
    },
    formatPrice(price) {
      return new Intl.NumberFormat("vi-VN", { style: "currency", currency: "VND" }).format(price);
    },
    addToCart(product) {
    const token = localStorage.getItem("access_token");
    const user = JSON.parse(localStorage.getItem("user")); // Lấy thông tin user từ localStorage

    if (!token || !user) {
      alert("Bạn cần đăng nhập để thêm vào giỏ hàng!");
      this.$router.push("/signin");
      return;
    }

    let cartKey = `cart_${user.id}`; // Tạo giỏ hàng riêng cho user
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
    this.fetchProducts();
    
  },
};
</script>




<style>
.button-signup{
  display: flex;
  justify-content: flex-end;
  text-decoration: underline;
}

.cart-button{
  
  padding: 8px;
    background-color: #ff6600;
    color: white;
    border: none;
    cursor: pointer;
    font-weight: bold;
    border-radius: 5px;
    margin-bottom: 10px;
}
.cart-button:hover {
  background-color: #ff4500;
}
.user-hello{
  display: inline;
  position: absolute;
  top: -70%;
}
main{
    padding-top: 50px;
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


/* product */




.title-product1{
  margin-bottom: 0;
    background-color: rgb(234, 206, 172);
    padding: 0.5rem 3rem;
    font-size: 2rem;
    margin-top: 3rem;



   


}
.img-product{
   width: 20rem;
   height: 16rem;
 
}


.product-item{
   margin-top: 30px;
   padding: 5px;
   display: inline-block;
   margin: 0 10px;
   flex-wrap: wrap;
}


.product-item-contaner{
   display: flex;
   flex-wrap: wrap;
   justify-content: space-around;
  


}


.evaluate{
   display: flex;
   justify-content: space-between;
   padding: 0 10px;
}


.buy{
   display: flex;
   list-style: none;
   font-size: 1.1rem;
}
.evaluate_star{
   display: flex;
   list-style: none;
   padding: 0;
}


.float{
   padding: 10px;
   margin: 0;
   font-size: 1.3rem;
   text-align: left;
}
.cost{
   
   background-color: rgb(239, 226, 209);


}


/* footer */
footer{
   margin-top: 70px;
   
}


.title-footer{
   text-align: center;
   font-size: 2rem;
   background-color: RGB(138, 99, 68);
   padding: 12px;
   color: white;


}


.feature-footer{
    margin-top: 50px;
   display: flex;
   justify-content: space-around;
    flex-wrap: wrap;

   
}


.text-feature{
   text-align: center;
   font-size: 1.7rem;
   font-weight: 400;


}

.feature-footer-item{
   background-color:RGB(239, 226, 209);
   width: 20rem;
   height: 15rem;
   border: 5px solid #7a5b2f;
   font-weight: 900;
   font-size: 1.3rem;
 
}
.icon-feature{
   text-align: center;
   font-size: 3rem;
   margin: 3rem 8rem;
}


.blog-footer{
   display: flex;
   justify-content: space-around;
   margin: 0 3rem;
   flex-wrap: wrap;
   flex-basis: 40%;
}
  
/* .sidebar1{
 
 




}
.sidebar2{
 
   


}
.sidebar3{
   
   
   


} */
.header-feature{
   font-size: 2rem;
   font-weight: 800;
}
.side{
   padding: 10px;
   height: 20rem;
   margin-top: 3rem;
   width: 20rem;

  
}
.text-header-feature{
   font-size: 1.2rem;
   margin-top: 16px;
}
.text-header-feature-item{
   display: flex;
   padding: 10px;
   line-height: 30px;
   
}
.icon-item {
   margin-right: 20px;
   
   text-align: center;
   align-items: center;
   display: flex;
   padding-top: 7px;


}

</style>