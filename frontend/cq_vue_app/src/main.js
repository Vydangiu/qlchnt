// import './assets/main.css'
// import '@fortawesome/fontawesome-free/css/all.css';
// import '@fortawesome/fontawesome-free/js/all.js';

// import { createApp } from 'vue'
// import App from './App.vue'
// import router from './route'


// createApp(App).use(router).mount('#app')

import './assets/main.css'
import '@fortawesome/fontawesome-free/css/all.css';
import '@fortawesome/fontawesome-free/js/all.js';

import { createApp } from 'vue'
import { createPinia } from 'pinia' // Thêm Pinia
import App from './App.vue'
import router from './route'

const app = createApp(App)
app.use(createPinia()) // Khởi tạo Pinia
app.use(router)
app.mount('#app')