<template>
    <div class="container">
        <div class="form">
            <form @submit.prevent="signup">
                <h1>ĐĂNG KÍ TÀI KHOẢN</h1>
                <div class="form-item">
                    <label class="title" for="username">Tên</label>
                    <input v-model="form.username" class="nhap" type="text" id="username">
                </div>
                <div class="form-item">
                    <label class="title" for="email">Email</label>
                    <input v-model="form.email" class="nhap" type="email" id="email">
                </div>
                <div class="form-item">
                    <label class="title" for="phone">Số điện thoại</label>
                    <input v-model="form.phone" class="nhap" type="text" id="phone">
                </div>
                <div class="form-item">
                    <label class="title" for="password">Mật khẩu</label>
                    <input v-model="form.password" class="nhap" type="password" id="password">
                </div>
                <div class="form-item">
                    <label class="title" for="password2">Xác nhận mật khẩu</label>
                    <input v-model="form.password2" class="nhap" type="password" id="password2">
                </div>
                <div class="nut">
                    <button class="gui">Đăng ký</button>
                </div>
                <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
            </form>
        </div>
    </div>
</template>

<script>
import axios from "axios";

export default {
    name: "Signup",
    data() {
        return {
            form: {
                username: "",  
                email: "",
                phone: "",
                password: "",
                password2: ""
            },
            errorMessage: "",
        };
    },
    methods: {
    //     async signup() {
    //         // Kiểm tra mật khẩu nhập lại có trùng không
    //         if (this.form.password !== this.form.password2) {
    //             this.errorMessage = "Mật khẩu không khớp!";
    //             return;
    //         }

    //         // Kiểm tra các trường không được để trống
    //         if (!this.form.email || !this.form.password || !this.form.password2 || !this.form.phone) {
    //             this.errorMessage = "Vui lòng nhập đầy đủ thông tin!";
    //             return;
    //         }

    //         try {
    //             const csrfToken = this.getCookie("csrftoken");

    //             // Nếu username rỗng, tự động tạo từ email
    //             if (!this.form.username) {
    //                 this.form.username = this.form.email.split("@")[0];
    //             }

    //             const response = await axios.post(
    //                 "http://127.0.0.1:8000/api/users/register/",
    //                 this.form,
    //                 {
    //                     headers: {
    //                         "X-CSRFToken": csrfToken,
    //                         "Content-Type": "application/json",
    //                     },
    //                 }
    //             );

    //             if (response.status === 201) {
    //                 alert("Đăng ký thành công! Hệ thống sẽ tự động đăng nhập.");

    //                 // Lưu token vào localStorage nếu có
    //                 if (response.data.access) {
    //                     localStorage.setItem("access_token", response.data.access);
    //                     localStorage.setItem("refresh_token", response.data.refresh);
    //                 }

    //                 // Chuyển hướng sang trang chủ hoặc đăng nhập
    //                 this.$router.push("/");
    //             }
    //         } catch (error) {
    //             console.error(error.response);
    //             this.errorMessage = error.response?.data?.error || "Có lỗi xảy ra!";
    //         }
    //     },

    //     getCookie(name) {
    //         let cookieValue = null;
    //         if (document.cookie && document.cookie !== "") {
    //             const cookies = document.cookie.split(";");
    //             for (let i = 0; i < cookies.length; i++) {
    //                 const cookie = cookies[i].trim();
    //                 if (cookie.startsWith(name + "=")) {
    //                     cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
    //                     break;
    //                 }
    //             }
    //         }
    //         return cookieValue;
    //     }
    // }
    async signup() {
    if (this.form.password !== this.form.password2) {
        this.errorMessage = "Mật khẩu không khớp!";
        return;
    }

    if (!this.form.email || !this.form.password || !this.form.password2 || !this.form.phone) {
        this.errorMessage = "Vui lòng nhập đầy đủ thông tin!";
        return;
    }

    try {
        if (!this.form.username) {
            this.form.username = this.form.email.split("@")[0];
        }

        const response = await axios.post(
            "http://127.0.0.1:8000/api/users/register/",
            this.form,
            {
                headers: {
                    "Content-Type": "application/json",
                },
            }
        );

        console.log("Response status:", response.status);
        console.log("Response data:", response.data);

        if (response.status === 201) {
            alert("Đăng ký thành công! Hệ thống sẽ tự động đăng nhập.");

            if (response.data.access && response.data.refresh) {
                localStorage.setItem("access_token", response.data.access);
                localStorage.setItem("refresh_token", response.data.refresh);
                console.log("Token đã được lưu:", {
                    access: localStorage.getItem("access_token"),
                    refresh: localStorage.getItem("refresh_token")
                });
            } else {
                console.warn("Không tìm thấy token trong response:", response.data);
                this.errorMessage = "Đăng ký thành công nhưng không nhận được token!";
            }

            this.$router.push("/");
        }
    } catch (error) {
        console.error("Lỗi chi tiết:", error.response?.data); // Log toàn bộ lỗi
        this.errorMessage = error.response?.data?.error || JSON.stringify(error.response?.data) || "Có lỗi xảy ra!";
    }
}
    }
};
</script>

<style>


/* form đăng kí tài khoản */

.input{
 
    text-align: center;
    border: none;
    font-size: 16px;
    margin-top: 50px;
}
.form {
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
    top: -43%;
    left: -13%;
    padding: 20px;

}

h1 {
    text-align: center;
  
}

.container {
    background-color: RGB(231, 218, 202);
    width: 600px;
    height: 400px;
    position: relative;
    display: flex;
    margin: auto;
   
}

.form-item {
    display: flex;
    margin: 15px;
    margin-bottom: 10px;
    padding: 0 16px;
    border-radius: 3px; 
    padding: 0 16px;
    border-radius: 3px;;
}

.title {
    font-size: 20px;
    margin-right: 10px;
    min-height: 20px;
    flex: 1;
}

.nhap {
    min-width: 270px;
    height: 30px;
    border-radius: 5px;
    border: solid 1px black;
    flex: 1;
    border-radius: 30px;
    padding: 0 16px;
  
    
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
    display: block;
    padding-top: 1px;
    color: black;
    text-align: center;  
    font-size: 1rem;
   
}

button.gui {
   

    padding: 8px 16px;
    border-radius: 5px;
    background-color: RGB(167, 110, 67);
    border: 1px solid RGB(167, 110, 67);
    margin-top: 5px;
    display: flex;
    color: white;
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