<template>
    <div style="height: 375px" class="container-sig">
        <div class="form-sig">
            <form @submit.prevent="login">
                <h1>THÔNG TIN ĐĂNG NHẬP</h1>
                <div class="input">
                    <div class="form-item-sig">
                        <label class="title-sig" for="username">Tên đăng nhập</label>
                        <input v-model="form.username" class="nhap" type="text" id="username">
                    </div>
                    <div class="form-item">
                        <label class="title-sig" for="password">Mật khẩu</label>
                        <input v-model="form.password" class="nhap" type="password" id="password">
                    </div>
                </div>
                <div style="display: flex; justify-content: space-between; padding: 0 28px" class="forgot">
                    
                    <a style="color: #807373; text-decoration: underline; font-size: 1rem;" href="signup">Đăng kí tài khoản</a>

                </div>
                <div class="controls" style="margin-top: 20px;">
                    <button style="margin-bottom: 0.8rem;" class="gui">Đăng nhập</button>
                </div>
                <div v-if="errorMessage" style="color: red; text-align: center; margin-top: 10px;">
                    {{ errorMessage }}
                </div>
              
            </form>
        </div>
    </div>
</template>

<script>
import axios from "axios";

export default {
  name: "Signin",
  data() {
    return {
      form: {
        username: "",
        password: "",
      },
      errorMessage: "",
    };
  },
  mounted() {
    console.log("Reset form khi vào trang đăng nhập...");
    this.form.username = "";
    this.form.password = "";
    localStorage.removeItem("access_token");
  },
  methods: {
    async login() {
      console.log("Bắt đầu đăng nhập...");
      try {
        const response = await axios.post("http://127.0.0.1:8000/api/users/login/", this.form);
        if (response.status === 200) {
          alert("Đăng nhập thành công!");
           // Lưu token vào localStorage
          localStorage.setItem("access_token", response.data.access);
           // Lưu thông tin user vào localStorage
           localStorage.setItem("user", JSON.stringify(response.data.user));

          // Reset form sau khi đăng nhập
          this.form.username = "";
          this.form.password = "";

          this.$router.push("/");
        }
      } catch (error) {
        this.errorMessage = "Sai tài khoản hoặc mật khẩu!";
      }
    },
    logout() {
      localStorage.removeItem("access_token");
      this.$router.push("/signin");
    }
  },
};
</script>

<style>


/* form đăng kí tài khoản */


.form-sig {
    display: grid;
    margin-top: 200px;
    margin-left: 100px;
    background-color: RGB(231, 218, 202);
    border: solid 2px black;
    border-radius: 20px;
    padding: 20px;
    box-sizing: content-box;
    height: 300px;
    position: absolute;
    top: -49%;
    left: -14.5%;
    padding: 20px;
    

}

h1 {
    text-align: center;
  
}

.input{
    min-width: 516px;
}
.container-sig {
    background-color: RGB(231, 218, 202);
    width: 600px;
    height: 400px;
    position: relative;
    display: flex;
    margin: auto;
   
}

.form-item-sig {
    display: flex;
    margin: 15px;
    margin-bottom: 10px;
    padding: 0 16px;
    border-radius: 3px; 
    padding: 0 16px;
    border-radius: 3px;;
}

.title-sig {
    font-size: 20px;
   
    min-height: 20px;
    flex: 1;
    min-width: 200px;   /* Giữ độ rộng cố định cho label */
    text-align: left;
    
}

.nhap {
    min-width: 270px;
    height: 30px;
border-radius: 5px;
    border: solid 1px black;
    flex: 1;
    border-radius: 30px;
  
    
}

.nut {
    border-radius: 20px;
    min-width: 150px;
    
    min-height: 45px;
    font-size: 20px;
    cursor: pointer;
    width: 100px;
    height: 30px;
    margin: 15px auto;

}

.forgot,a {
    display: flex;
    padding-top: 1px;
    color: black;
   justify-content: space-around; 
    font-size: 1rem;
   
}

button.gui {
  padding: 8px 16px;
    border-radius: 5px;
    background-color: RGB(167, 110, 67);
    border: 1px solid RGB(167, 110, 67);
    margin-top: 5px;
    display: flex;
    margin: 0 auto;
    
}


.forgot{
    font-size: 0.5rem;
    color: #807373;

}

.controls{
    color: #646c6c9c;
}

.border{
    border-bottom: 1px solid;
}

@media (min-width: 1024px) {
  #app {
    grid-template-columns: unset !important;
  }
}


</style>