// import { createRouter, createWebHistory } from 'vue-router'
// import { useAuthStore } from '@/store/auth'

// // --- Khách hàng ---
// import Home from './components/Home.vue'
// import signin from './components/signin.vue'
// import signup from './components/signup.vue'
// import detail from './components/detail.vue'
// import Product from './components/Product.vue'
// import contact from './components/contact.vue'
// import Blog from './components/Blog.vue'
// import shop_cart from './components/shop_cart.vue'
// import CartView from "@/components/CartView.vue"

// // --- Admin ---
// import Login from '@/components/Login.vue'
// import Dashboard from '@/components/Dashboard.vue'
// import Categories from '@/components/Categories.vue'
// import Orders from '@/components/Orders.vue'
// import Users from '@/components/Users.vue'
// import AdminProductList from '@/components/AdminProductList.vue'

// const routes = [
//   // --- Khách hàng ---
//   { name: 'Home', path: '/', component: Home },
//   { name: 'signin', path: '/signin', component: signin },
//   { name: 'signup', path: '/signup', component: signup },
//   { name: 'detail', path: '/detail', component: detail },
//   { name: 'Product', path: '/Product', component: Product },
//   { name: 'contact', path: '/contact', component: contact },
//   { name: 'Blog', path: '/Blog', component: Blog },
//   { name: 'shop_cart', path: '/shop_cart', component: shop_cart },
//   { name: 'Cart', path: '/cart', component: CartView },

//   // --- Admin ---
//   { path: '/login', component: Login },
//   {
//     path: '/admin',
//     children: [
//       { path: '', redirect: '/admin/dashboard' }, // nếu vào /admin thì chuyển sang dashboard
//       { path: 'dashboard', component: Dashboard },
//       { path: 'products', component: AdminProductList },
//       { path: 'categories', component: Categories },
//       { path: 'orders', component: Orders },
//       { path: 'users', component: Users },
//     ]
//   }
// ]

// const router = createRouter({
//   history: createWebHistory(),
//   routes,
// })

// // --- Middleware bảo vệ admin ---
// router.beforeEach((to, from, next) => {
//   const store = useAuthStore()
//   const isAdminRoute = to.path.startsWith('/admin')

//   if (isAdminRoute && !store.token) {
//     next('/login')
//   } else {
//     next()
//   }
// })

// export default router




import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/store/auth'

// --- Khách hàng ---
import Home from './components/Home.vue'
import signin from './components/signin.vue'
import signup from './components/signup.vue'
import detail from './components/detail.vue'
import Product from './components/Product.vue'
import contact from './components/contact.vue'
import Blog from './components/Blog.vue'
import shop_cart from './components/shop_cart.vue'
import CartView from "@/components/CartView.vue"
import ProductDetail from './components/ProductDetail.vue'


// --- Admin ---
import ProductImageUploader from '@/components/ProductImageUploader.vue'
import Dashboard from '@/components/Dashboard.vue'
import Categories from '@/components/Categories.vue'
import Orders from '@/components/Orders.vue'
import Users from '@/components/Users.vue'
import AdminProductList from '@/components/AdminProductList.vue'
import Login from './components/Login.vue'
import Checkout from './components/checkout.vue'

const routes = [
    // --- Khách hàng ---
    { name: 'Home', path: '/', component: Home },
    { name: 'signin', path: '/signin', component: signin },
    { name: 'signup', path: '/signup', component: signup },
    { name: 'detail', path: '/detail', component: detail },
    // { name: 'ProductDetail', path: '/products/:id', component: ProductDetail },
    { name: 'ProductDetail', path: '/products/:id', component: ProductDetail,  props: true  },
    { name: 'Product', path: '/Product', component: Product },
    { name: 'contact', path: '/contact', component: contact },
    { name: 'Blog', path: '/Blog', component: Blog },
    { name: 'shop_cart', path: '/shop_cart', component: shop_cart },
    { name: 'Cart', path: '/cart', component: CartView },
    { name: 'Checkout',path: `/checkout/:productId/`, component: Checkout,  props: true   },
    { name: 'Orders', path: '/orders', component: Orders},
 // Luồng thanh toán giỏ hàng
 {
    path: "/checkout/",
    name: "CheckoutCart",
    component: Checkout,
    props: false
  },
    //   // --- Admin ---
    { path: '/login', component: Login },
    //   {
    //     path: '/admin',
    //     component: Dashboard, // Dashboard làm layout
    //     children: [
    //       { path: '', redirect: 'admin/dashboard' },
    //      // Không có component riêng, sẽ hiển thị nội dung của Dashboard
    //       { path: 'products', component: AdminProductList },
    //       { path: 'categories', component: Categories },
    //       { path: 'orders', component: Orders },
    //       { path: 'users', component: Users },
    //     ]
    //   }
    // ]

    // const router = createRouter({
    //   history: createWebHistory(),
    //   routes,
    // })

    // // --- Middleware bảo vệ admin ---
    // router.beforeEach((to, from, next) => {
    //   const store = useAuthStore()
    //   const isAdminRoute = to.path.startsWith('/admin')

    //   if (isAdminRoute && !store.token) {
    //     next('/login')
    //   } else {
    //     next()
    //   }
    // })

    // export default router
    // Admin routes
    {
        path: '/admin/dashboard',
        name: 'Dashboard',
        component: Dashboard,
        meta: { requiresAuth: true }, // Yêu cầu xác thực
    },
    {
        path: '/admin/products',
        name: 'AdminProductList',
        component: AdminProductList,
        meta: { requiresAuth: true }, // Yêu cầu xác thực
    },
    {
        path: '/admin/product-images',
        name: 'ProductImageUploader',
        component: ProductImageUploader,
        meta: { requiresAuth: true }, // Yêu cầu xác thực
    },
    {
        path: '/admin/categories',
        name: 'Categories',
        component: Categories,
        meta: { requiresAuth: true }, // Yêu cầu xác thực
    },
  
    {
        path: '/admin/users',
        name: 'Users',
        component: Users,
        meta: { requiresAuth: true }, // Yêu cầu xác thực
    },

];

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes,
});

router.beforeEach((to, from, next) => {
    const authStore = useAuthStore();
    const requiresAuth = to.meta.requiresAuth;

    if (requiresAuth && !authStore.isAuthenticated) {
        // Nếu route yêu cầu xác thực và chưa đăng nhập, chuyển hướng đến trang đăng nhập
        next('/login');
    } else {
        next(); // Cho phép truy cập route
    }
});

export default router;