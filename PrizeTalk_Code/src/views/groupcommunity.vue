<template>
  <div class="groups-page">
    <div class="groups-header">
      <h1>Discussion Groups</h1>
      <p class="subtitle">Join groups to discuss awards with like-minded enthusiasts</p>

      <div class="header-actions">
        <div class="filter-tabs">
          <button 
            :class="['tab-btn', { active: viewMode === 'all' }]"
            @click="viewMode = 'all'"
          >
            <span class="icon">⛱</span> All Groups
          </button>
          <button 
            :class="['tab-btn', { active: viewMode === 'my-groups' }]"
            @click="viewMode = 'my-groups'"
          >
            <span class="icon">𖠋𖠋</span> My Groups
          </button>
        </div>

        <button class="create-group-btn" @click="showCreateModal = true">
          <span class="icon">⊹ ࣪ ˖</span> Create Group
        </button>
      </div>

      <div class="search-bar">
        <input 
          v-model="searchQuery" 
          type="search" 
          placeholder="Search groups..." 
          class="search-input"
        />
      </div>
    </div>

    <div class="groups-container">
      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
        <p>Loading groups...</p>
      </div>

      <div v-else-if="filteredGroups.length === 0" class="empty-state">
        <div class="empty-icon">𖠋𖠋</div>
        <p>{{ viewMode === 'my-groups' ? 'You haven\'t joined any groups yet' : 'No groups found' }}</p>
        <button class="create-group-btn" @click="showCreateModal = true">
          Create Your First Group
        </button>
      </div>

      <div v-else class="groups-grid">
        <GroupCard 
          v-for="group in filteredGroups" 
          :key="group.id"
          :group="group"
          :currentUserId="loggedInUserId"
          :currentUserRole="loggedInUserRole"
          @join="handleJoinGroup"
          @leave="handleLeaveGroup"
          @delete="handleDeleteGroup"
          @view="viewGroup"
        />
      </div>
    </div>

    <CreateGroupModal 
      v-if="showCreateModal"
      :userId="loggedInUserId"
      @close="showCreateModal = false"
      @created="handleGroupCreated"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import GroupCard from './GroupCard.vue'
import CreateGroupModal from './CreateGroupModal.vue'

const API_BASE_URL = (
  import.meta.env.VITE_API_BASE_URL ||
  import.meta.env.VITE_API_PROXY_TARGET ||
  ''
).replace(/\/+$/, '')

const router = useRouter()

const groups = ref([])
const loading = ref(true)
const viewMode = ref('all')
const searchQuery = ref('')
const showCreateModal = ref(false)
const loggedInUserId = ref(null)
const loggedInUserRole = ref('user')

const filteredGroups = computed(() => {
  let filtered = groups.value

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(g =>
      g.name.toLowerCase().includes(query) ||
      (g.description && g.description.toLowerCase().includes(query))
    )
  }

  return filtered
})

const fetchGroups = async () => {
  loading.value = true
  try {
    const params = viewMode.value === 'my-groups' && loggedInUserId.value
      ? { user_id: loggedInUserId.value }
      : {}

    const { data } = await axios.get(`${API_BASE_URL}/api/groups/`, { params })
    groups.value = data
  } catch (error) {
    console.error('Failed to fetch groups:', error)
  } finally {
    loading.value = false
  }
}

const handleJoinGroup = async (groupId) => {
  if (!loggedInUserId.value) {
    alert('Please log in to join groups')
    return
  }

  try {
    await axios.post(`${API_BASE_URL}/api/groups/${groupId}/join/`, {
      user_id: loggedInUserId.value
    })
    await fetchGroups()
  } catch (error) {
    console.error('Failed to join group:', error)
    alert(error.response?.data?.error || 'Failed to join group')
  }
}

const handleLeaveGroup = async (groupId) => {
  if (!confirm('Are you sure you want to leave this group?')) return

  try {
    await axios.post(`${API_BASE_URL}/api/groups/${groupId}/leave/`, {
      user_id: loggedInUserId.value
    })
    await fetchGroups()
  } catch (error) {
    console.error('Failed to leave group:', error)
    alert(error.response?.data?.error || 'Failed to leave group')
  }
}

const handleDeleteGroup = async (groupId) => {
  if (!confirm('Are you sure you want to delete this group? All posts and comments will be lost.')) return

  try {
    await axios.delete(`${API_BASE_URL}/api/groups/${groupId}/`, {
      data: { user_id: loggedInUserId.value }
    })
    await fetchGroups()
  } catch (error) {
    console.error('Failed to delete group:', error)
    alert(error.response?.data?.error || 'Failed to delete group')
  }
}

const viewGroup = (groupId) => {
  router.push(`/groups/${groupId}`)
}

const handleGroupCreated = () => {
  showCreateModal.value = false
  fetchGroups()
}

onMounted(async () => {
  try {
    const userData = JSON.parse(localStorage.getItem('loggedInUser') || '{}')
    loggedInUserId.value = userData.userId
    loggedInUserRole.value = userData.role || 'user'
  } catch (e) {
    console.error('Failed to get user data:', e)
  }
  
  await fetchGroups()
})

// Watch viewMode changes
import { watch } from 'vue'
watch(viewMode, () => {
  fetchGroups()
})
</script>

<style scoped>
.groups-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

.groups-header {
  margin-bottom: 2rem;
}

.groups-header h1 {
  color: var(--color-heading);
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

.subtitle {
  color: var(--color-text-muted);
  margin-bottom: 1.5rem;
}

.header-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
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
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.tab-btn:hover {
  border-color: var(--color-border-hover);
  transform: translateY(-1px);
}

.tab-btn.active {
  background: var(--color-button-bg);
  color: white;
  border-color: var(--color-button-bg);
}

.icon {
  font-size: 1.2rem;
}

.create-group-btn {
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

.create-group-btn:hover {
  background: var(--color-button-hover-bg);
  transform: translateY(-1px);
}

.search-bar {
  margin-top: 1rem;
}

.search-input {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 2px solid var(--color-border);
  border-radius: 12px;
  font-size: 0.95rem;
  background: var(--color-background-soft);
  color: var(--color-text);
  transition: all 0.3s ease;
}

.search-input:focus {
  outline: none;
  border-color: var(--color-border-hover);
  box-shadow: 0 0 0 4px rgba(188, 128, 52, 0.1);
}

.groups-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 1.5rem;
}

.loading-state,
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

@media (max-width: 768px) {
  .header-actions {
    flex-direction: column;
    align-items: stretch;
  }

  .groups-grid {
    grid-template-columns: 1fr;
  }
}

@media (prefers-color-scheme: dark) {
  .tab-btn.active {
    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  }
}
</style>