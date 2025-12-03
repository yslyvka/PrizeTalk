<template>
  <div class="community-page">
    <div class="community-header">
      <h1>Community Discussions</h1>
      <p class="subtitle">Share insights and discuss award winners with the community</p>
      
      <div class="filters-row">
        <div class="filter-tabs">
          <button 
            v-for="tab in feedTabs" 
            :key="tab.value"
            :class="['tab-btn', { active: activeTab === tab.value }]"
            @click="activeTab = tab.value"
          >
            <span class="icon" style="font-size: 1.5em;">{{ tab.icon }}</span> {{ tab.text }}
          </button>
        </div>
        
        <button class="create-post-btn" @click="showCreateModal = true">
          <span class="icon" style="font-size: 1.5em;">✐ᝰ</span> New Post
        </button>
      </div>

      <div class="secondary-filters">
        <select v-model="postTypeFilter" class="filter-select">
          <option value="">All Types</option>
          <option value="1">Discussion</option>
          <option value="2">Analysis</option>
          <option value="3">Opinion</option>
          <option value="4">News</option>
          <option value="5">Question</option>
        </select>

        <input 
          v-model="searchQuery" 
          type="search" 
          placeholder="Search posts..." 
          class="search-input"
        />
      </div>
    </div>

    <!-- Posts Feed -->
    <div class="posts-container">
      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
        <p>Loading posts...</p>
      </div>

      <div v-else-if="filteredPosts.length === 0" class="empty-state">
        <p>No posts found. Be the first to start a discussion!</p>
      </div>

      <PostCard
        v-for="post in filteredPosts"
        :key="post.id"
        :post="post"
        :currentUserId="loggedInUserId"
        :currentUserRole="loggedInUserRole"
        @comment="handleComment"
        @deleted="handlePostDeleted"
      />

    </div>

    <!-- Create Post Modal -->
    <CreatePostModal 
      v-if="showCreateModal"
      @close="showCreateModal = false"
      @created="handlePostCreated"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import axios from 'axios'
import PostCard from './postcard.vue'
import CreatePostModal from './createpost.vue'

const API_BASE_URL = (
  import.meta.env.VITE_API_BASE_URL ||
  import.meta.env.VITE_API_PROXY_TARGET ||
  ''
).replace(/\/+$/, '')

const posts = ref([])
const loading = ref(true)
const activeTab = ref('trending')
const postTypeFilter = ref('')
const searchQuery = ref('')
const showCreateModal = ref(false)
const loggedInUserId = ref(null)
const loggedInUserRole = ref('user')

const feedTabs = [
  { icon: '☕︎', text: 'Trending', value: 'trending' },
  { icon: '⏱', text: 'Recent', value: 'recent' },
  { icon: '𐦂𖨆𐀪𖠋', text: 'Following', value: 'following' },
]

const handlePostDeleted = (postId) => {
  posts.value = posts.value.filter(p => p.id !== postId)
}

const filteredPosts = computed(() => {
  let filtered = posts.value

  watch([postTypeFilter, activeTab], () => {
    fetchPosts()
  })

  // Search
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(p =>
      (p.title && p.title.toLowerCase().includes(query)) ||
      (p.content && p.content.toLowerCase().includes(query)) ||
      (Array.isArray(p.tags) && p.tags.some(tag => tag && tag.toLowerCase().includes(query)))
    )
  }

  // Sort based on active tab
  if (activeTab.value === 'trending') {
    filtered.sort((a, b) => (b.likes_count + b.comments_count) - (a.likes_count + a.comments_count))
  } else if (activeTab.value === 'recent') {
    filtered.sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
  }

  return filtered
})


const fetchPosts = async () => {
  loading.value = true
  try {
    const params = {}
    
    if (activeTab.value === 'following') {
      params.following = 'true'
      if (loggedInUserId.value) {
        params.current_user_id = loggedInUserId.value 
      } else {
        console.warn('Cannot fetch "following" posts without a logged in user ID.')
        loading.value = false;
        return;
      }
    }

    if (postTypeFilter.value) {
      params.category_id = postTypeFilter.value
    }

    const { data } = await axios.get(`${API_BASE_URL}/api/community/`, { params })
    posts.value = data
  } catch (error) {
    console.error('Failed to fetch posts:', error)
  } finally {
    loading.value = false
  }
}


const handleComment = (postId) => {
  console.log('Comment on post:', postId)
}

const handlePostCreated = (newPost) => {
  showCreateModal.value = false
  posts.value.unshift(newPost)
}

const fetchLoggedInUser = async () => {
  try {
    const userData = JSON.parse(localStorage.getItem('loggedInUser') || '{}')
    loggedInUserId.value = userData.userId
    loggedInUserRole.value = userData.role
    console.log('Logged in user ID set to:', loggedInUserId.value)
    console.log('Logged in user role set to:', loggedInUserRole.value)
  } catch (error) {
    console.error('Failed to fetch logged-in user data:', error)
  }
};

onMounted(async () => {
  await fetchLoggedInUser();
  fetchPosts();
})
</script>


<style scoped>
.community-page {
  max-width: 900px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

.community-header {
  margin-bottom: 2rem;
}

.community-header h1 {
  color: var(--color-heading);
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

.subtitle {
  color: var(--color-text-muted);
  margin-bottom: 1.5rem;
}

.filters-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  gap: 1rem;
  flex-wrap: wrap;
}

.filter-tabs {
  display: flex;
  gap: 0.5rem;
}

.tab-btn {
  padding: 0.5rem 1rem;
  border: 2px solid var(--color-border);
  background: transparent;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  color: var(--color-text);
  transition: all 0.3s ease;
}

.tab-btn:hover {
  border-color: var(--color-border-hover);
}

.tab-btn.active {
  background: var(--color-button-bg);
  color: white;
  border-color: var(--color-button-bg);
}

.create-post-btn {
  padding: 0.5rem 1.25rem;
  background: var(--color-button-bg);
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.3s ease;
}

.create-post-btn:hover {
  background: var(--color-button-hover-bg);
  transform: translateY(-1px);
}

.secondary-filters {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
}

.filter-select,
.search-input {
  padding: 0.5rem 1rem;
  border: 2px solid var(--color-border);
  border-radius: 8px;
  font-size: 0.95rem;
  background: var(--color-background-soft);
}

.search-input {
  flex: 1;
}

.posts-container {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.loading-state,
.empty-state {
  text-align: center;
  padding: 3rem;
  color: var(--color-text-muted);
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid var(--color-border);
  border-top-color: var(--color-button-bg);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

@media (max-width: 640px) {
  .filters-row {
    flex-direction: column;
    align-items: stretch;
  }

  .secondary-filters {
    flex-direction: column;
  }
}

.tab-label span.icon {
  font-size: 1.5em;
}

</style>