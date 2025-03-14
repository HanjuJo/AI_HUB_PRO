&lt;template&gt;
  &lt;nav class="navigation"&gt;
    &lt;div class="nav-brand"&gt;
      &lt;router-link to="/"&gt;AI Content Hub&lt;/router-link&gt;
    &lt;/div&gt;
    
    &lt;div class="nav-links"&gt;
      &lt;template v-if="isAuthenticated"&gt;
        &lt;router-link to="/dashboard"&gt;대시보드&lt;/router-link&gt;
        &lt;router-link to="/ai-tools"&gt;AI 도구&lt;/router-link&gt;
        &lt;router-link to="/tool-combinations"&gt;도구 조합&lt;/router-link&gt;
        &lt;router-link to="/youtube-data"&gt;YouTube 데이터&lt;/router-link&gt;
        &lt;router-link to="/content-optimization"&gt;콘텐츠 최적화&lt;/router-link&gt;
        &lt;router-link to="/profile"&gt;프로필&lt;/router-link&gt;
        &lt;a href="#" @click.prevent="logout"&gt;로그아웃&lt;/a&gt;
      &lt;/template&gt;
      &lt;template v-else&gt;
        &lt;router-link to="/login"&gt;로그인&lt;/router-link&gt;
        &lt;router-link to="/register"&gt;회원가입&lt;/router-link&gt;
      &lt;/template&gt;
    &lt;/div&gt;
  &lt;/nav&gt;
&lt;/template&gt;

&lt;script setup&gt;
import { computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const isAuthenticated = computed(() => {
  return !!localStorage.getItem('token')
})

const logout = () => {
  localStorage.removeItem('token')
  router.push('/login')
}
&lt;/script&gt;

&lt;style scoped&gt;
.navigation {
  background: #ffffff;
  padding: 1rem 2rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.nav-brand a {
  font-size: 1.5rem;
  font-weight: bold;
  color: #1976d2;
  text-decoration: none;
}

.nav-links {
  display: flex;
  gap: 1.5rem;
  align-items: center;
}

.nav-links a {
  color: #333;
  text-decoration: none;
  font-weight: 500;
  padding: 0.5rem;
  border-radius: 4px;
  transition: all 0.2s;
}

.nav-links a:hover {
  background: #f5f5f5;
}

.nav-links a.router-link-active {
  color: #1976d2;
  background: #e3f2fd;
}

@media (max-width: 768px) {
  .navigation {
    flex-direction: column;
    padding: 1rem;
  }
  
  .nav-brand {
    margin-bottom: 1rem;
  }
  
  .nav-links {
    flex-direction: column;
    width: 100%;
    gap: 0.5rem;
  }
  
  .nav-links a {
    width: 100%;
    text-align: center;
    padding: 0.75rem;
  }
}
&lt;/style&gt;
