&lt;template&gt;
  &lt;div class="content-optimization"&gt;
    &lt;div class="header"&gt;
      &lt;h1&gt;콘텐츠 최적화&lt;/h1&gt;
      &lt;button @click="createContent" class="primary-button"&gt;새 콘텐츠 작성&lt;/button&gt;
    &lt;/div&gt;

    &lt;div v-if="showForm" class="content-form"&gt;
      &lt;h2&gt;{{ editMode ? '콘텐츠 수정' : '새 콘텐츠 작성' }}&lt;/h2&gt;
      &lt;form @submit.prevent="submitContent"&gt;
        &lt;div class="form-group"&gt;
          &lt;label for="title"&gt;제목&lt;/label&gt;
          &lt;input
            id="title"
            v-model="contentForm.title"
            type="text"
            required
            placeholder="콘텐츠 제목을 입력하세요"
          &gt;
        &lt;/div&gt;

        &lt;div class="form-group"&gt;
          &lt;label for="content-type"&gt;콘텐츠 유형&lt;/label&gt;
          &lt;select id="content-type" v-model="contentForm.content_type" required&gt;
            &lt;option value="video"&gt;비디오&lt;/option&gt;
            &lt;option value="blog"&gt;블로그&lt;/option&gt;
            &lt;option value="social"&gt;소셜 미디어&lt;/option&gt;
          &lt;/select&gt;
        &lt;/div&gt;

        &lt;div class="form-group"&gt;
          &lt;label for="description"&gt;본문&lt;/label&gt;
          &lt;textarea
            id="description"
            v-model="contentForm.description"
            required
            rows="10"
            placeholder="콘텐츠 내용을 입력하세요"
          &gt;&lt;/textarea&gt;
        &lt;/div&gt;

        &lt;div class="form-group"&gt;
          &lt;label for="keywords"&gt;키워드 (쉼표로 구분)&lt;/label&gt;
          &lt;input
            id="keywords"
            v-model="contentForm.keywords"
            type="text"
            required
            placeholder="예: AI, 콘텐츠 제작, 최적화"
          &gt;
        &lt;/div&gt;

        &lt;div class="form-group"&gt;
          &lt;label for="meta-description"&gt;메타 설명&lt;/label&gt;
          &lt;textarea
            id="meta-description"
            v-model="contentForm.meta_description"
            rows="3"
            placeholder="검색 결과에 표시될 설명을 입력하세요"
          &gt;&lt;/textarea&gt;
        &lt;/div&gt;

        &lt;div class="form-actions"&gt;
          &lt;button type="submit" class="primary-button"&gt;
            {{ editMode ? '수정하기' : '작성하기' }}
          &lt;/button&gt;
          &lt;button type="button" @click="cancelForm" class="secondary-button"&gt;
            취소
          &lt;/button&gt;
        &lt;/div&gt;
      &lt;/form&gt;
    &lt;/div&gt;

    &lt;div v-else class="content-list"&gt;
      &lt;div v-for="content in contents" :key="content.id" class="content-card"&gt;
        &lt;div class="content-header"&gt;
          &lt;h3&gt;{{ content.title }}&lt;/h3&gt;
          &lt;div class="content-type-badge" :class="content.content_type"&gt;
            {{ getContentTypeLabel(content.content_type) }}
          &lt;/div&gt;
        &lt;/div&gt;

        &lt;div class="scores"&gt;
          &lt;div class="score-item"&gt;
            &lt;div class="score-label"&gt;SEO 점수&lt;/div&gt;
            &lt;div class="score-value" :class="getScoreClass(content.seo_score)"&gt;
              {{ content.seo_score }}
            &lt;/div&gt;
          &lt;/div&gt;
          &lt;div class="score-item"&gt;
            &lt;div class="score-label"&gt;가독성&lt;/div&gt;
            &lt;div class="score-value" :class="getScoreClass(content.readability_score)"&gt;
              {{ content.readability_score }}
            &lt;/div&gt;
          &lt;/div&gt;
          &lt;div class="score-item"&gt;
            &lt;div class="score-label"&gt;참여도&lt;/div&gt;
            &lt;div class="score-value" :class="getScoreClass(content.engagement_score)"&gt;
              {{ content.engagement_score }}
            &lt;/div&gt;
          &lt;/div&gt;
          &lt;div class="score-item"&gt;
            &lt;div class="score-label"&gt;기술 점수&lt;/div&gt;
            &lt;div class="score-value" :class="getScoreClass(content.technical_score)"&gt;
              {{ content.technical_score }}
            &lt;/div&gt;
          &lt;/div&gt;
        &lt;/div&gt;

        &lt;div class="suggestions" v-if="content.optimization_suggestions.length"&gt;
          &lt;h4&gt;개선 제안&lt;/h4&gt;
          &lt;ul&gt;
            &lt;li v-for="suggestion in content.optimization_suggestions" :key="suggestion.id"
                :class="['suggestion', `priority-${suggestion.priority}`]"&gt;
              {{ suggestion.suggestion }}
            &lt;/li&gt;
          &lt;/ul&gt;
        &lt;/div&gt;

        &lt;div class="content-actions"&gt;
          &lt;button @click="editContent(content)" class="edit-button"&gt;수정&lt;/button&gt;
          &lt;button @click="deleteContent(content.id)" class="delete-button"&gt;삭제&lt;/button&gt;
        &lt;/div&gt;
      &lt;/div&gt;
    &lt;/div&gt;
  &lt;/div&gt;
&lt;/template&gt;

&lt;script setup&gt;
import { ref, onMounted } from 'vue'
import axios from 'axios'

const contents = ref([])
const showForm = ref(false)
const editMode = ref(false)
const contentForm = ref({
  title: '',
  content_type: 'blog',
  description: '',
  keywords: '',
  meta_description: '',
  meta_keywords: ''
})

const getContentTypeLabel = (type) => {
  const labels = {
    video: '비디오',
    blog: '블로그',
    social: '소셜 미디어'
  }
  return labels[type] || type
}

const getScoreClass = (score) => {
  if (score >= 80) return 'excellent'
  if (score >= 60) return 'good'
  if (score >= 40) return 'fair'
  return 'poor'
}

const loadContents = async () => {
  try {
    const response = await axios.get('http://localhost:8004/api/v1/content/me', {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`
      }
    })
    contents.value = response.data
  } catch (error) {
    console.error('콘텐츠 로딩 실패:', error)
  }
}

const createContent = () => {
  editMode.value = false
  contentForm.value = {
    title: '',
    content_type: 'blog',
    description: '',
    keywords: '',
    meta_description: '',
    meta_keywords: ''
  }
  showForm.value = true
}

const editContent = (content) => {
  editMode.value = true
  contentForm.value = { ...content }
  showForm.value = true
}

const submitContent = async () => {
  try {
    if (editMode.value) {
      await axios.put(
        `http://localhost:8004/api/v1/content/${contentForm.value.id}`,
        contentForm.value,
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        }
      )
    } else {
      await axios.post(
        'http://localhost:8000/api/v1/content/',
        contentForm.value,
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        }
      )
    }
    showForm.value = false
    await loadContents()
  } catch (error) {
    console.error('콘텐츠 저장 실패:', error)
  }
}

const deleteContent = async (contentId) => {
  if (!confirm('정말로 이 콘텐츠를 삭제하시겠습니까?')) return
  
  try {
    await axios.delete(`http://localhost:8000/api/v1/content/${contentId}`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`
      }
    })
    await loadContents()
  } catch (error) {
    console.error('콘텐츠 삭제 실패:', error)
  }
}

const cancelForm = () => {
  showForm.value = false
}

onMounted(() => {
  loadContents()
})
&lt;/script&gt;

&lt;style scoped&gt;
.content-optimization {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.content-form {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.form-actions {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
}

.content-card {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-bottom: 1.5rem;
}

.content-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.content-type-badge {
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.875rem;
  font-weight: 500;
}

.content-type-badge.video {
  background: #e3f2fd;
  color: #1976d2;
}

.content-type-badge.blog {
  background: #f3e5f5;
  color: #7b1fa2;
}

.content-type-badge.social {
  background: #e8f5e9;
  color: #388e3c;
}

.scores {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;
  margin: 1.5rem 0;
}

.score-item {
  text-align: center;
  padding: 1rem;
  background: #f5f5f5;
  border-radius: 8px;
}

.score-label {
  font-size: 0.875rem;
  color: #666;
  margin-bottom: 0.5rem;
}

.score-value {
  font-size: 1.5rem;
  font-weight: 600;
}

.score-value.excellent {
  color: #2e7d32;
}

.score-value.good {
  color: #1976d2;
}

.score-value.fair {
  color: #f57c00;
}

.score-value.poor {
  color: #d32f2f;
}

.suggestions {
  margin-top: 1.5rem;
}

.suggestions h4 {
  margin-bottom: 1rem;
}

.suggestion {
  padding: 0.75rem;
  margin-bottom: 0.5rem;
  border-radius: 4px;
  font-size: 0.875rem;
}

.suggestion.priority-1 {
  background: #ffebee;
  color: #c62828;
}

.suggestion.priority-2 {
  background: #fff3e0;
  color: #ef6c00;
}

.suggestion.priority-3 {
  background: #e8f5e9;
  color: #2e7d32;
}

.content-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1.5rem;
}

.primary-button {
  background: #1976d2;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 4px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
}

.primary-button:hover {
  background: #1565c0;
}

.secondary-button {
  background: #f5f5f5;
  color: #333;
  border: 1px solid #ddd;
  padding: 0.75rem 1.5rem;
  border-radius: 4px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
}

.secondary-button:hover {
  background: #eeeeee;
}

.edit-button {
  background: #2196f3;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
}

.delete-button {
  background: #f44336;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
}
&lt;/style&gt;
