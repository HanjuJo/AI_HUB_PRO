import { createRouter, createWebHistory } from 'vue-router'

// 페이지 컴포넌트 가져오기
const Home = () => import('../views/Home.vue')
const Login = () => import('../views/Login.vue')
const Register = () => import('../views/Register.vue')
const Dashboard = () => import('../views/Dashboard.vue')
const Profile = () => import('../views/Profile.vue')
const AITools = () => import('../views/AITools.vue')
const ToolCombinations = () => import('../views/ToolCombinations.vue')
const YoutubeData = () => import('../views/YoutubeData.vue')

const NotFound = () => import('../views/NotFound.vue')

// 라우트 정의
const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/register',
    name: 'Register',
    component: Register
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard,
    meta: { requiresAuth: true }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: Profile,
    meta: { requiresAuth: true }
  },
  {
    path: '/ai-tools',
    name: 'AITools',
    component: AITools
  },
  {
    path: '/tool-combinations',
    name: 'ToolCombinations',
    component: ToolCombinations,
    meta: { requiresAuth: true }
  },
  {
    path: '/youtube-data',
    name: 'YoutubeData',
    component: YoutubeData
  },

  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: NotFound
  }
]

// 라우터 생성
const router = createRouter({
  history: createWebHistory(),
  routes
})

// 네비게이션 가드 설정
import store from '../store'

router.beforeEach((to, from, next) => {
  const isAuthenticated = store.getters.isAuthenticated
  
  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login')
  } else if ((to.path === '/login' || to.path === '/register') && isAuthenticated) {
    next('/dashboard')
  } else {
    next()
  }
})

export default router
