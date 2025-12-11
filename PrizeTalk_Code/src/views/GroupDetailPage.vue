<template>
  <div class="group-detail-page">
    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>Loading group...</p>
    </div>

    <div v-else-if="!group" class="error-state">
      <p>Group not found or you don't have access.</p>
      <button class="btn-primary" @click="$router.push('/groups')">Back to Groups</button>
    </div>

    <template v-else>
      <div class="group-header">
        <div class="header-top">
          <button class="back-btn" @click="$router.push('/groups')">
            ← Back to Groups
          </button>
        </div>

        <div class="group-info">
          <div class="group-icon-large">𖠋𖠋</div>
          <div class="group-details">
            <h1>{{ group.name }}</h1>
            <p v-if="group.description" class="group-description">
              {{ group.description }}
            </p>
            <div class="group-stats">
              <span class="stat">𖠋𖠋 {{ group.member_count }} members</span>
              <span class="stat">✉︎ {{ posts.length }} posts</span>
              <span class="stat" v-if="group.user_role">
                {{ getRoleLabel(group.user_role) }}
              </span>
            </div>
          </div>
        </div>

        <div class="header-actions">
          <button 
            v-if="isMember"
            class="create-post-btn" 
            @click="showCreatePostModal = true"
          >
            <span class="icon">✎</span> New Post
          </button>
          
          <button 
            v-if="canDelete"
            class="delete-group-btn"
            @click="handleDeleteGroup"
          >
            ⌦ Delete Group
          </button>
        </div>
      </div>

      <div class="posts-container">
        <div v-if="postsLoading" class="loading-state">
          <div class="spinner"></div>
          <p>Loading posts...</p>
        </div>

        <div v-else-if="posts.length === 0" class="empty-state">
          <div class="empty-icon">✎˖ᝰ✧˖°</div>
          <p>No posts yet. Be the first to start a discussion!</p>
          <button 
            v-if="isMember"
            class="create-post-btn" 
            @click="showCreatePostModal = true"
          >
            Create First Post
          </button>
        </div>

        <GroupPostCard 
          v-else
          v-for="post in posts" 
          :key="post.id"
          :post="post"
          :groupId="groupId"
          :currentUserId="loggedInUserId"
          :currentUserRole="loggedInUserRole"
          :userGroupRole="group.user_role"
          @deleted="handlePostDeleted"
          @updated="fetchPosts"
        />
      </div>

      <CreateGroupPostModal 
        v-if="showCreatePostModal"
        :groupId="groupId"
        :userId="loggedInUserId"
        @close="showCreatePostModal = false"
        @created="handlePostCreated"
      />
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import GroupPostCard from './GroupPostCard.vue'
import CreateGroupPostModal from './CreateGroupPostModal.vue'

const route = useRoute()
const router = useRouter()

const API_BASE_URL = (
  import.meta.env.VITE_API_BASE_URL ||
  import.meta.env.VITE_API_PROXY_TARGET ||
  ''
).replace(/\/+$/, '')

const groupId = computed(() => parseInt(route.params.id))
const group = ref(null)
const posts = ref([])
const loading = ref(true)
const postsLoading = ref(true)
const showCreatePostModal = ref(false)
const loggedInUserId = ref(null)
const loggedInUserRole = ref('user')

const isMember = computed(() => {
  return group.value?.is_member
})

const canDelete = computed(() => {
  if (loggedInUserRole.value === 'staff_admin') return true
  return group.value?.user_role === 'admin' || 
         group.value?.created_by === loggedInUserId.value
})

const getRoleLabel = (role) => {
  const labels = {
    admin: '♛ Admin',
    moderator: '⛊ Moderator',
    member: '✓ Member'
  }
  return labels[role] || role
}

const fetchGroup = async () => {
  loading.value = true
  try {
    const { data } = await axios.get(
      `${API_BASE_URL}/api/groups/${groupId.value}/`,
      { params: { user_id: loggedInUserId.value } }
    )
    group.value = data
  } catch (error) {
    console.error('Failed to fetch group:', error)
    group.value = null
  } finally {
    loading.value = false
  }
}

const fetchPosts = async () => {
  if (!loggedInUserId.value) return
  
  postsLoading.value = true
  try {
    const { data } = await axios.get(
      `${API_BASE_URL}/api/groups/${groupId.value}/posts/`,
      { params: { user_id: loggedInUserId.value } }
    )
    posts.value = data
  } catch (error) {
    console.error('Failed to fetch posts:', error)
    if (error.response?.status === 403) {
      // Not a member
      posts.value = []
    }
  } finally {
    postsLoading.value = false
  }
}

const handlePostCreated = (newPost) => {
  showCreatePostModal.value = false
  posts.value.unshift(newPost)
}

const handlePostDeleted = (postId) => {
  posts.value = posts.value.filter(p => p.id !== postId)
}

const handleDeleteGroup = async () => {
  if (!confirm('Are you sure you want to delete this group? All posts and comments will be permanently deleted.')) {
    return
  }

  try {
    await axios.delete(
      `${API_BASE_URL}/api/groups/${groupId.value}/`,
      { data: { user_id: loggedInUserId.value } }
    )
    alert('Group deleted successfully')
    router.push('/groups')
  } catch (error) {
    console.error('Failed to delete group:', error)
    alert(error.response?.data?.error || 'Failed to delete group')
  }
}

onMounted(async () => {
  try {
    const userData = JSON.parse(localStorage.getItem('loggedInUser') || '{}')
    loggedInUserId.value = userData.userId
    loggedInUserRole.value = userData.role || 'user'
  } catch (e) {
    console.error('Failed to get user data:', e)
  }

  await fetchGroup()
  if (group.value?.is_member) {
    await fetchPosts()
  } else {
    postsLoading.value = false
  }
})
</script>

<style scoped>
.group-detail-page {
  max-width: 900px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

.loading-state,
.error-state {
  text-align: center;
  padding: 4rem 2rem;
  color: var(--color-text-muted);
}

.spinner {
  width: 50px;
  height: 50px;
  border: 4px solid var(--color-border);
  border-top-color: var(--color-button-bg);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.group-header {
  margin-bottom: 2rem;
}

.header-top {
  margin-bottom: 1rem;
}

.back-btn {
  padding: 0.5rem 1rem;
  border: 2px solid var(--color-border);
  background: transparent;
  color: var(--color-text);
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.back-btn:hover {
  border-color: var(--color-border-hover);
  background: var(--color-background-mute);
}

.group-info {
  display: flex;
  gap: 1.5rem;
  align-items: flex-start;
  margin-bottom: 1.5rem;
  padding: 1.5rem;
  background: var(--color-background-soft);
  border-radius: 12px;
  border: 1px solid var(--color-border);
}

.group-icon-large {
  width: 80px;
  height: 80px;
  background: var(--color-background-mute);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2.5rem;
  flex-shrink: 0;
}

.group-details {
  flex: 1;
}

.group-details h1 {
  color: var(--color-heading);
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

.group-description {
  color: var(--color-text);
  line-height: 1.6;
  margin-bottom: 1rem;
}

.group-stats {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.stat {
  padding: 0.375rem 0.75rem;
  background: var(--color-background-mute);
  border-radius: 6px;
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--color-text-muted);
}

.header-actions {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
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

.delete-group-btn {
  padding: 0.5rem 1.25rem;
  background: #dc2626;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.delete-group-btn:hover {
  background: #b91c1c;
  transform: translateY(-1px);
}

.posts-container {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  color: var(--color-text-muted);
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
  opacity: 0.5;
}

.btn-primary {
  padding: 0.75rem 1.5rem;
  background: var(--color-button-bg);
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-primary:hover {
  background: var(--color-button-hover-bg);
}

@media (max-width: 768px) {
  .group-info {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }

  .group-details h1 {
    font-size: 1.5rem;
  }
}

@media (prefers-color-scheme: dark) {
  .group-icon-large {
    background: rgba(59, 130, 246, 0.1);
  }
}
</style>