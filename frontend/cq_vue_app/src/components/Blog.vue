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

<main>
    <div>
        <!-- <h1>--- Blog ---</h1> -->
        <h2 class="header-blog">Cửa hàng nội thất Moda Casa - <i style="color:brown">Nơi kiến tạo không gian sống hoàn hảo</i></h2>
        <p class="text-about">🏡 Moda Casa tự hào là thương hiệu nội thất cao cấp, mang đến những thiết kế tinh tế, hiện đại và đầy cảm hứng. Với sứ mệnh kiến tạo không gian sống lý tưởng, chúng tôi cung cấp đa dạng các sản phẩm nội thất từ phòng khách, phòng ngủ, đến nhà bếp – tất cả đều được chế tác từ chất liệu cao cấp, đảm bảo độ bền và tính thẩm mỹ vượt thời gian.</p>
        <p class="title-footer">Vì sao nên chọn Moda Casa ?</p>
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
</main>
</template>
<script>
const images = import.meta.glob('@/assets/IMG/*.jpg', { eager: true });

// Chuyển danh sách import thành một mảng đường dẫn ảnh
const imageList = Object.values(images).map(img => img.default);

console.log(imageList); // Kiểm tra danh sách ảnh được import

</script>
<style>

.header-blog{
   margin-top: 30px;
    font-size: 2rem;
    font-weight: 800;
    text-align: center;
}
.text-about{
   line-height: 3rem;
    font-size: 1.5rem;
    font-weight: 400;
    padding: 0 10rem;
    margin-top: 20px;
   
}
/* main{
    
    
} */
.feature-footer{
    /* margin-top: 50px; */
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
main{
    padding-top: 50px;
    margin-bottom: 30px;;
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

.title-footer{
    margin-top: 30px;
   text-align: center;
   font-size: 2rem;
   background-color: RGB(138, 99, 68);
   padding: 12px;
   color: white;


}
</style>