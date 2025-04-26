<template>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
    <div class="wrapper">
    <header class="menu-toggle" >
    <!-- Mobile menu button -->
   
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
                <input type="text" class="search-input" placeholder="Tìm kiếm">
                <div class="icon-search">
                    <a class="link" href=""><i class="fa-solid fa-magnifying-glass"></i></a>
                </div>
            </div>
            <div class="navbar-cart-login-icon">
                <a style="font-size: 2rem;" href="/cart"> 
                <i class="fa-solid fa-bag-shopping"></i>
                </a>
            
                 <div v-if="user" class="user-info">
              
                    <a class="user-hello" style="font-size: 2rem;  cursor: pointer;" @click="logout">
                        <i style="margin-top: 40px" class="fa-solid fa-user"></i>
                        <span style="font-size: 1rem; display: inline-flex;"> Xin chào, {{ user.username }} </span>
                    
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
<h1 class="header-contact"><i>Bạn muốn liên hệ để giải đáp thắc mắc ?</i></h1>

    <div style="background-color: RGB(239, 226, 209);"  class="blog-footer">
      
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

</template>
<script>
const images = import.meta.glob('@/assets/IMG/*.jpg', { eager: true });

// Chuyển danh sách import thành một mảng đường dẫn ảnh
const imageList = Object.values(images).map(img => img.default);

console.log(imageList); // Kiểm tra danh sách ảnh được import

</script>
<style>
body{
    background-color: RGB(239, 226, 209);
}


.header-contact{
    text-align: center;
    font-size: 3rem;
    font-weight: 400;
    padding-top: 3.5rem;
    color: brown;
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




body{
    background-color: #d2c5b6;
    color: black;
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




.navbar-link-item{
   display: flex;
   justify-content: space-between;
   margin: 0 ;
   font-size: 1.5rem;


}


.item-link{
   list-style: none;
   margin: 0 20px;


}
.link{
   text-decoration: none;
   color: rgb(37, 36, 36);
   font-size: 1.5rem;


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
  width: 30rem;


}
.search-input{
   border-style: none;
   border-radius: 15px;
   padding: 0 10px;
   width: 25rem;
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
.blog-footer{
   display: flex;
   justify-content: space-around;
   margin: 0 3rem;
   flex-wrap: wrap;
   flex-basis: 40%;
}
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
   /* margin-top: 16px; */
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