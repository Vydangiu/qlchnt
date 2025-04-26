<template >
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
              <a style="font-size: 2rem;" href=""> <i  class="fa-solid fa-bag-shopping"></i></a>
              <a style="font-size: 2rem; padding-bottom: 10px;" href="signin"><i  class="fa-solid fa-user"></i></a>


            </div>
        </div>
        <div class="hamburger" @click="toggleMenu">☰</div>
   
</header>
<main>
    <div class="product-detail">
        <div class="product-detail-item">
            <img  class="product-detail-img" src="@/assets/IMG/ban-an.jpg" alt="">
        </div>
        <div class="product-detail__img-detail">
            <h3 class="title-detail__h3">Bộ bàn gỗ tự nhiên phong cách hiện đại</h3>
            <p>Giá bán: <span style="color:brown">8 triệu</span> <br> Đã bán: <span style="color:brown">45</span></p>
            <h4 class="title-detail">Kích thước</h4>
            <ul>
                <li>Bàn ăn: chiều dài 140cm x Chiều rộng 70cm x Chiều cao 75cm</li>
                <li>Ghế ăn: chiều dài 140cm x Chiều rộng 70cm x Chiều cao 75cm</li>
            </ul>
            <h4 class="title-detail">Mô tả</h4>
            <ul>
                <li>Bộ bàn ăn gỗ tự nhiên phong cách hiện đại gồm 1 bàn ăn và 6 ghế, thiết kế tố giản nhưng tinh tế. Mặt bàn đen sang trọng kết hợp với khung gỗ chắc chắn, tạo nên điểm nhấn cho không gian phòng ăn.</li>
                <li>Ghế có đệm bọc vải mềm mại, mang lại cảm giác thoải mái khi sử dụng</li>
                <li>Sản phẩm phù hợp với nhiều phong cách nội thất từ hiện đại đến tối giản, giúp bữa ăn gia đình thêm ấm cúng và sang trọng</li>
            </ul>
            <div class="quantity-control">
                <button @click="decrease" class="btn--sub">-</button>
                <input type="text" v-model="quantity" class="input--number" readonly />
                <button @click="increase" class="btn--add">+</button>
            </div>
            <div class="button-group">
                <button class="button-group-item button-group__bag" type="submit">THÊM VÀO GIỎ HÀNG</button>
                <button class="button-group-item button-group__buy" type="submit">MUA NGAY</button>
            </div>

        </div>

    </div>
</main>
</div>

</template>
<script>
export default {
  data() {
    return {
      quantity: 1, // Số lượng mặc định
    };
  },
  methods: {
    increase() {
      this.quantity++;
    },
    decrease() {
      if (this.quantity > 1) this.quantity--;
    },
  },
};


const images = import.meta.glob('@/assets/IMG/*.jpg', { eager: true });

// Chuyển danh sách import thành một mảng đường dẫn ảnh
const imageList = Object.values(images).map(img => img.default);

console.log(imageList); // Kiểm tra danh sách ảnh được import
</script>
<style>


.button-group-item{
    
    border-style: none;
    padding: 15px 20px;
    width: 15rem;
    margin: 0 auto;
    border-radius: 7px;
    font-size: 1rem;
    color:white;
}
.button-group__bag{
   margin-bottom: 20px;
   background-color: RGB(140, 70, 19);
}
.button-group__buy{
    background-color:RGB(240, 104, 56);
    
}

.button-group {
  display: flex;
  flex-direction: column;
  margin-top: 20px;
 
}

.quantity-control {
  display: flex;
  align-items: center;
  border: 1px solid #ccc;
  width: 100px;
  border-radius: 5px;
  overflow: hidden;
  margin-top: 12px;
  margin-left: 20px;
}

.btn--sub
 {
  width: 30px;
  height: 30px;
  border: none;
  background-color: #f8f8f8;
  cursor: pointer;
  font-size: 18px;
}
.btn--add{
  width: 30px;
  height: 30px;
  border: none;
  background-color: #f8f8f8;
  cursor: pointer;
  font-size: 18px;
}

.input--number {
  width: 40px;
  text-align: center;
  border: none;
  font-size: 16px;
}

.btn:hover {
  background-color: #ddd;
}


/* header */
.title-detail{
    font-size: 1.5rem;
    font-weight: bold;
}

.title-detail__h3{
    font-size: 2rem;
    
    font-weight: bold;
}
.product-detail{
    display: flex;
    margin-top: 20px 50px;
    justify-content: center;
    flex-wrap: wrap;
    font-size: 1.3rem;
    
  
}
.product-detail-item{
   
    margin: 0 20px;
  
}
.product-detail-img{
    width: 40rem;
    height:40rem;
    margin: 15px;
}

.product-detail__img-detail{
    flex: 1;
    width:40rem;
    height:30rem;
    margin: 15px;
  
  
}
main{
    background-color: RGB(242, 239, 234);
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
</style>