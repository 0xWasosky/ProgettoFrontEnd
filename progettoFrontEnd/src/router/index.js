import { createRouter, createWebHistory } from 'vue-router'
import Login from '@/components/Login.vue'
import Register from '@/components/Register.vue'
import Home from '@/components/Home.vue'
import Settings from '@/components/Settings.vue'
import ChangePassword from '@/components/ChangePassword.vue'
import ChangeProfilePicture from '@/components/ChangeProfilePicture.vue'
import Classes from '@/components/Classes.vue'
import Admin from '@/components/Admin.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'Login', component: Login },
    { path: '/register', name: 'Register', component: Register },

    { path: '/home', name: 'Home', component: Home, meta: { requiresAuth: true}},
    { path: '/settings', name: 'Settings', component: Settings, meta: { requiresAuth: true}},
    { path: '/change_password', name: 'ChangePassword', component: ChangePassword, meta: { requiresAuth: true}},
    { path: '/change_profile_picture', name: 'ChangeProfilePicture', component: ChangeProfilePicture, meta: { requiresAuth: true} },
    { path: '/classes', name: 'Classes', component: Classes, meta: { requiresAuth: true}},
    { path: '/admin', name: 'Admin', component: Admin, meta: {requiresAuth: true} },
  ],
})

router.beforeEach((to, from, next) => {
  const isLogged = localStorage.getItem('username') != null
  if (to.meta.requiresAuth && !isLogged) {
    next('/')
  }
  else if((to.path == '/' || to.path == '/register') && isLogged){
    next('/home')
  }
  else{
    next()
  }
})

export default router
