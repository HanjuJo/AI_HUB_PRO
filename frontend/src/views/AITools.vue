<template>
  <div class="ai-tools">
    <h2 class="mb-4">AI 도구 목록</h2>
    
    <div class="row mb-4">
      <div class="col-md-6">
        <div class="input-group">
          <input 
            type="text" 
            class="form-control" 
            placeholder="AI 도구 검색..." 
            v-model="searchQuery"
            @input="filterTools"
          >
          <button class="btn btn-primary" type="button">
            <i class="bi bi-search"></i> 검색
          </button>
        </div>
      </div>
      <div class="col-md-6">
        <div class="d-flex justify-content-end">
          <div class="btn-group">
            <button 
              v-for="category in categories" 
              :key="category.id"
              class="btn" 
              :class="selectedCategory === category.id ? 'btn-primary' : 'btn-outline-primary'"
              @click="selectCategory(category.id)"
            >
              {{ category.name }}
            </button>
            <button 
              class="btn" 
              :class="selectedCategory === null ? 'btn-primary' : 'btn-outline-primary'"
              @click="selectCategory(null)"
            >
              전체
            </button>
          </div>
        </div>
      </div>
    </div>

    <div class="row">
      <div v-for="tool in filteredTools" :key="tool.id" class="col-md-4 mb-4">
        <div class="card h-100">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-start mb-2">
              <h5 class="card-title">{{ tool.name }}</h5>
              <button 
                class="btn btn-sm" 
                :class="tool.favorite ? 'btn-warning' : 'btn-outline-warning'"
                @click="toggleFavorite(tool)"
              >
                <i class="bi" :class="tool.favorite ? 'bi-star-fill' : 'bi-star'"></i>
              </button>
            </div>
            <p class="card-text">{{ tool.description }}</p>
            <div class="mb-3">
              <span 
                v-for="category in tool.categories" 
                :key="category.id" 
                class="badge bg-secondary me-1 mb-1"
              >
                {{ category.name }}
              </span>
            </div>
            <div class="d-flex justify-content-between">
              <a :href="tool.url" target="_blank" class="btn btn-sm btn-primary">
                공식 사이트
              </a>
              <button 
                class="btn btn-sm btn-outline-primary" 
                @click="addToToolCombination(tool)"
              >
                도구 조합에 추가
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="filteredTools.length === 0" class="text-center py-5">
      <p class="mb-3">검색 결과가 없습니다.</p>
      <button class="btn btn-primary" @click="resetFilters">필터 초기화</button>
    </div>

    <!-- 도구 조합에 추가 모달 -->
    <div class="modal fade" :class="{ 'show d-block': showAddToCombinationModal }" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">도구 조합에 추가</h5>
            <button type="button" class="btn-close" @click="showAddToCombinationModal = false"></button>
          </div>
          <div class="modal-body">
            <p><strong>{{ selectedTool?.name }}</strong>을(를) 도구 조합에 추가합니다.</p>
            
            <div class="mb-3">
              <label class="form-label">기존 도구 조합 선택</label>
              <select class="form-select" v-model="selectedCombinationId">
                <option value="">새 도구 조합 만들기</option>
                <option 
                  v-for="combo in toolCombinations" 
                  :key="combo.id" 
                  :value="combo.id"
                >
                  {{ combo.name }}
                </option>
              </select>
            </div>
            
            <div v-if="!selectedCombinationId" class="mb-3">
              <label for="newComboName" class="form-label">새 도구 조합 이름</label>
              <input 
                type="text" 
                class="form-control" 
                id="newComboName"
                v-model="newCombinationName" 
                placeholder="도구 조합 이름을 입력하세요"
              >
            </div>
            
            <div v-if="!selectedCombinationId" class="mb-3">
              <label for="newComboDesc" class="form-label">새 도구 조합 설명</label>
              <textarea 
                class="form-control" 
                id="newComboDesc"
                v-model="newCombinationDescription" 
                placeholder="도구 조합에 대한 설명을 입력하세요"
                rows="3"
              ></textarea>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="showAddToCombinationModal = false">취소</button>
            <button type="button" class="btn btn-primary" @click="confirmAddToToolCombination">추가</button>
          </div>
        </div>
      </div>
    </div>
    <div class="modal-backdrop fade" :class="{ 'show': showAddToCombinationModal }" v-if="showAddToCombinationModal"></div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { aiToolsApi, toolCombinationsApi } from '../services/api'

export default {
  name: 'AITools',
  setup() {
    const tools = ref([])
    const categories = ref([])
    const searchQuery = ref('')
    const selectedCategory = ref(null)
    const toolCombinations = ref([])
    const showAddToCombinationModal = ref(false)
    const selectedTool = ref(null)
    const selectedCombinationId = ref('')
    const newCombinationName = ref('')
    const newCombinationDescription = ref('')
    const isLoading = ref(false)
    const error = ref(null)

    // 필터링된 도구 목록
    const filteredTools = computed(() => {
      let result = [...tools.value]
      
      // 검색어 필터링
      if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase()
        result = result.filter(tool => 
          tool.name.toLowerCase().includes(query) || 
          tool.description.toLowerCase().includes(query)
        )
      }
      
      // 카테고리 필터링
      if (selectedCategory.value !== null) {
        result = result.filter(tool => 
          tool.categories.some(cat => cat.id === selectedCategory.value)
        )
      }
      
      return result
    })

    // 도구 목록 로드
    const loadTools = async () => {
      isLoading.value = true
      error.value = null
      
      try {
        const response = await aiToolsApi.getTools()
        tools.value = response.data
        
        // 데이터가 없을 경우 테스트 데이터 사용
        if (!tools.value || tools.value.length === 0) {
          tools.value = [
            {
              id: 1,
              name: 'ChatGPT',
              description: '자연어 처리 AI 모델로 텍스트 생성 및 대화가 가능합니다.',
              url: 'https://chat.openai.com',
              favorite: true,
              categories: [
                { id: 1, name: '텍스트 생성' },
                { id: 2, name: '콘텐츠 기획' }
              ]
            },
            {
              id: 2,
              name: 'Midjourney',
              description: '텍스트 프롬프트를 기반으로 고품질 이미지를 생성합니다.',
              url: 'https://www.midjourney.com',
              favorite: false,
              categories: [
                { id: 3, name: '이미지 생성' }
              ]
            },
            {
              id: 3,
              name: 'Descript',
              description: 'AI를 활용한 오디오 및 비디오 편집 도구입니다.',
              url: 'https://www.descript.com',
              favorite: true,
              categories: [
                { id: 4, name: '오디오 편집' },
                { id: 5, name: '비디오 편집' }
              ]
            },
            {
              id: 4,
              name: 'Grammarly',
              description: 'AI 기반 문법 및 맞춤법 검사 도구입니다.',
              url: 'https://www.grammarly.com',
              favorite: false,
              categories: [
                { id: 1, name: '텍스트 생성' },
                { id: 6, name: '교정' }
              ]
            },
            {
              id: 5,
              name: 'Canva',
              description: 'AI 기능이 포함된 그래픽 디자인 플랫폼입니다.',
              url: 'https://www.canva.com',
              favorite: false,
              categories: [
                { id: 3, name: '이미지 생성' },
                { id: 7, name: '디자인' }
              ]
            },
            {
              id: 6,
              name: 'Runway',
              description: 'AI 기반 비디오 편집 및 생성 도구입니다.',
              url: 'https://runwayml.com',
              favorite: false,
              categories: [
                { id: 5, name: '비디오 편집' },
                { id: 8, name: '비디오 생성' }
              ]
            }
          ]
        }
      } catch (err) {
        console.error('AI 도구를 가져오는 중 오류가 발생했습니다:', err)
        error.value = '도구 목록을 가져오는데 실패했습니다.'
      } finally {
        isLoading.value = false
      }
    }

    // 카테고리 목록 로드
    const loadCategories = async () => {
      try {
        const response = await aiToolsApi.getCategories()
        categories.value = response.data
        
        // 데이터가 없을 경우 테스트 데이터 사용
        if (!categories.value || categories.value.length === 0) {
          categories.value = [
            { id: 1, name: '텍스트 생성' },
            { id: 2, name: '콘텐츠 기획' },
            { id: 3, name: '이미지 생성' },
            { id: 4, name: '오디오 편집' },
            { id: 5, name: '비디오 편집' },
            { id: 6, name: '교정' },
            { id: 7, name: '디자인' },
            { id: 8, name: '비디오 생성' }
          ]
        }
      } catch (err) {
        console.error('카테고리를 가져오는 중 오류가 발생했습니다:', err)
      }
    }

    // 도구 조합 목록 로드
    const loadToolCombinations = async () => {
      try {
        const response = await toolCombinationsApi.getCombinations()
        toolCombinations.value = response.data
        
        // 데이터가 없을 경우 테스트 데이터 사용
        if (!toolCombinations.value || toolCombinations.value.length === 0) {
          toolCombinations.value = [
            {
              id: 1,
              name: '유튜브 쇼츠 제작 세트',
              description: '유튜브 쇼츠 제작을 위한 최적의 AI 도구 조합입니다.',
              tools: [1, 2, 3]
            },
            {
              id: 2,
              name: '블로그 콘텐츠 제작 세트',
              description: 'SEO에 최적화된 블로그 콘텐츠 제작을 위한 AI 도구 조합입니다.',
              tools: [1, 4, 5]
            }
          ]
        }
      } catch (err) {
        console.error('도구 조합을 가져오는 중 오류가 발생했습니다:', err)
      }
    }

    // 검색어 필터링
    const filterTools = () => {
      // 이미 computed 속성에서 처리됨
    }

    // 카테고리 선택
    const selectCategory = (categoryId) => {
      selectedCategory.value = categoryId
    }

    // 필터 초기화
    const resetFilters = () => {
      searchQuery.value = ''
      selectedCategory.value = null
    }

    // 즐겨찾기 토글
    const toggleFavorite = async (tool) => {
      try {
        // API 호출은 실제 즐겨찾기 API가 구현되었을 때 추가
        // 임시 UI 업데이트
        tool.favorite = !tool.favorite
      } catch (err) {
        console.error('즐겨찾기 업데이트 중 오류가 발생했습니다:', err)
      }
    }

    // 도구 조합에 추가 모달 열기
    const addToToolCombination = (tool) => {
      selectedTool.value = tool
      selectedCombinationId.value = ''
      newCombinationName.value = ''
      newCombinationDescription.value = ''
      showAddToCombinationModal.value = true
    }

    // 도구 조합에 추가 확인
    const confirmAddToToolCombination = async () => {
      try {
        if (selectedCombinationId.value) {
          // 기존 도구 조합에 추가
          await toolCombinationsApi.updateCombination(selectedCombinationId.value, {
            tool_ids: [...toolCombinations.value.find(c => c.id === parseInt(selectedCombinationId.value)).tools, selectedTool.value.id]
          })
          
          // UI 업데이트
          const combo = toolCombinations.value.find(c => c.id === parseInt(selectedCombinationId.value))
          if (combo && !combo.tools.includes(selectedTool.value.id)) {
            combo.tools.push(selectedTool.value.id)
          }
        } else {
          // 새 도구 조합 생성
          if (!newCombinationName.value) {
            alert('도구 조합 이름을 입력해주세요.')
            return
          }
          
          const newCombination = {
            name: newCombinationName.value,
            description: newCombinationDescription.value,
            tool_ids: [selectedTool.value.id]
          }
          
          const response = await toolCombinationsApi.createCombination(newCombination)
          
          // UI 업데이트
          toolCombinations.value.push(response.data)
        }
        
        showAddToCombinationModal.value = false
        alert('도구 조합에 추가되었습니다.')
      } catch (err) {
        console.error('도구 조합 업데이트 중 오류가 발생했습니다:', err)
        alert('도구 조합 저장 중 오류가 발생했습니다.')
      }
    }

    onMounted(() => {
      loadTools()
      loadCategories()
      loadToolCombinations()
    })

    return {
      tools,
      categories,
      searchQuery,
      selectedCategory,
      filteredTools,
      toolCombinations,
      showAddToCombinationModal,
      selectedTool,
      selectedCombinationId,
      newCombinationName,
      newCombinationDescription,
      isLoading,
      error,
      filterTools,
      selectCategory,
      resetFilters,
      toggleFavorite,
      addToToolCombination,
      confirmAddToToolCombination
    }
  }
}
</script>

<style scoped>
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  z-index: 1040;
  width: 100vw;
  height: 100vh;
  background-color: #000;
}

.modal-backdrop.fade {
  opacity: 0;
}

.modal-backdrop.show {
  opacity: 0.5;
}

.modal.fade {
  z-index: 1050;
  background-color: rgba(0, 0, 0, 0.4);
}

.modal.show {
  display: block;
}
</style>
