<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-content">
      <div class="modal-header">
        <h2>Create New Post</h2>
        <button class="close-btn" @click="$emit('close')">✕</button>
      </div>

      <form @submit.prevent="handleSubmit" class="post-form">
        <div class="form-group">
          <label>Post Type</label>
          <select v-model="formData.post_type" required>
            <option value="discussion">Discussion</option>
            <option value="analysis">Analysis</option>
            <option value="opinion">Opinion</option>
            <option value="news">News</option>
            <option value="question">Question</option>
          </select>
        </div>

        <div class="form-group">
          <label>Title</label>
          <input v-model="formData.title" type="text" required maxlength="300" placeholder="What's your post about?">
        </div>

        <div class="form-group">
          <label>Content</label>
          <textarea v-model="formData.content" required rows="8" placeholder="Share your thoughts..."></textarea>
        </div>

        <div class="form-group">
          <label>Tags (comma-separated)</label>
          <input v-model="tagsInput" type="text" placeholder="nobel, physics, 2023">
        </div>

        <div class="form-actions">
          <button type="button" class="btn-secondary" @click="$emit('close')">Cancel</button>
          <button type="submit" class="btn-primary" :disabled="submitting">
            {{ submitting ? 'Posting...' : 'Post' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const emit = defineEmits(['close', 'created'])

const API_BASE_URL = (
  import.meta.env.VITE_API_BASE_URL ||
  import.meta.env.VITE_API_PROXY_TARGET ||
  ''
).replace(/\/+$/, '')

const CATEGORY_MAP = {
  discussion: 1,
  analysis: 2,
  opinion: 3,
  news: 4,
  question: 5
}

const formData = ref({
  title: '',
  content: '',
  post_type: 'discussion',
})

const tagsInput = ref('')
const submitting = ref(false)
const loggedInUserId = ref(null)
const loggedInUserRole = ref('user');

onMounted(() => {
  const storedUser = JSON.parse(localStorage.getItem('loggedInUser'))
  if (storedUser?.userId) {
    loggedInUserId.value = storedUser.userId
  } else {
    console.warn('No logged-in user found')
  }

  loggedInUserRole.value = storedUser.role || 'user';
})

const handleSubmit = async () => {
  if (!loggedInUserId.value) {
    alert('You must be logged in to post.')
    return
  }

  submitting.value = true
  try {
    const tags = tagsInput.value
      .split(',')
      .map(tag => tag.trim())
      .filter(tag => tag.length > 0)

    const payload = {
      user_id: loggedInUserId.value,
      category_id: CATEGORY_MAP[formData.value.post_type] || 1,
      title: formData.value.title,
      content: formData.value.content,
      tags: tags
    }

    const response = await axios.post(`${API_BASE_URL}/api/community/`, payload)

    emit('created', response.data)
    emit('close')
  } catch (error) {
    console.error('Failed to create post:', error)
    alert('Failed to create post. Check console for details.')
  } finally {
    submitting.value = false
  }
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
}

.modal-content {
  background: var(--color-background);
  border-radius: 16px;
  max-width: 600px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid var(--color-border);
}

.modal-header h2 {
  margin: 0;
  color: var(--color-heading);
}

.close-btn {
  width: 32px;
  height: 32px;
  border: none;
  background: transparent;
  color: var(--color-text-muted);
  font-size: 1.5rem;
  cursor: pointer;
  border-radius: 50%;
  transition: all 0.3s ease;
}

.close-btn:hover {
  background: var(--color-background-mute);
  color: var(--color-text);
}

.post-form {
  padding: 1.5rem;
}

.form-group {
  margin-bottom: 1.25rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: var(--color-text);
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid var(--color-border);
  border-radius: 8px;
  font-size: 0.95rem;
  font-family: inherit;
  background: var(--color-background-soft);
  color: var(--color-text);
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: var(--color-accent);
}

.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 1.5rem;
}

.btn-primary,
.btn-secondary {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-primary {
  background: var(--color-button-bg);
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: var(--color-button-hover-bg);
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-secondary {
  background: transparent;
  color: var(--color-text);
  border: 2px solid var(--color-border);
}

.btn-secondary:hover {
  background: var(--color-background-mute);
}
</style>