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
const ChoiceHelper = () => import('../views/ChoiceHelper.vue')
const DailyFortune = () => import('../views/DailyFortune.vue')
const Naming = () => import('../views/Naming.vue')
const FortuneLove = () => import('../views/FortuneLove.vue')
const FortuneMoney = () => import('../views/FortuneMoney.vue')
const FortuneBusiness = () => import('../views/FortuneBusiness.vue')
const FortuneHealth = () => import('../views/FortuneHealth.vue')

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
    path: '/choice-helper',
    name: 'ChoiceHelper',
    component: ChoiceHelper,
    meta: { requiresAuth: false }
  },
  {
    path: '/daily-fortune',
    name: 'DailyFortune',
    component: DailyFortune,
    meta: { requiresAuth: false }
  },
  {
    path: '/naming',
    name: 'Naming',
    component: Naming,
    meta: { requiresAuth: false }
  },
  {
    path: '/fortune/love',
    name: 'FortuneLove',
    component: FortuneLove,
    meta: { requiresAuth: false }
  },
  {
    path: '/fortune/money',
    name: 'FortuneMoney',
    component: FortuneMoney,
    meta: { requiresAuth: false }
  },
  {
    path: '/fortune/business',
    name: 'FortuneBusiness',
    component: FortuneBusiness,
    meta: { requiresAuth: false }
  },
  {
    path: '/fortune/health',
    name: 'FortuneHealth',
    component: FortuneHealth,
    meta: { requiresAuth: false }
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
