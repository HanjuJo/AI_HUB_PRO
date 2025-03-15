import { createRouter, createWebHistory } from 'vue-router'

// 페이지 컴포넌트 가져오기
const Home = () => import('../views/Home.vue')
const Login = () => import('../views/Login.vue')
const Register = () => import('../views/Register.vue')
const Dashboard = () => import('../views/Dashboard.vue')
const Profile = () => import('../views/Profile.vue')
const AITools = () => import('../views/AITools.vue')
const ToolCombinations = () => import('../views/ToolCombinations.vue')
const YoutubeAnalysis = () => import('../views/YoutubeAnalysis.vue')
const Support = () => import('../views/Support.vue')

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
    component: Dashboard
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
    component: ToolCombinations
  },
  {
    path: '/youtube-analysis',
    name: 'YoutubeAnalysis',
    component: YoutubeAnalysis
  },
  {
    path: '/support',
    name: 'Support',
    component: Support
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: NotFound
  }
]

// 라우터 생성
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

// 네비게이션 가드 설정
import store from '../store'

router.beforeEach((to, from, next) => {
  const currentUser = store.getters.currentUser
  
  if (to.meta.requiresAuth && !currentUser) {
    next('/login')
  } else {
    next()
  }
})

export default router
