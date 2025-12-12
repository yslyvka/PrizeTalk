<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-content">
      <div class="modal-header">
        <h2>Create New Group</h2>
        <button class="close-btn" @click="$emit('close')">✕</button>
      </div>

      <form @submit.prevent="handleSubmit" class="group-form">
        <div class="form-group">
          <label>Group Name *</label>
          <input 
            v-model="formData.name" 
            type="text" 
            required 
            maxlength="100" 
            placeholder="e.g., Oscar Film Buffs"
          >
        </div>

        <div class="form-group">
          <label>Description</label>
          <textarea 
            v-model="formData.description" 
            rows="5" 
            placeholder="Tell people what this group is about..."
          ></textarea>
        </div>

        <div class="form-info">
          <p>💡 <strong>Tip:</strong> You'll become the group admin and can invite others to join!</p>
        </div>

        <div class="form-actions">
          <button type="button" class="btn-secondary" @click="$emit('close')">Cancel</button>
          <button type="submit" class="btn-primary" :disabled="submitting">
            {{ submitting ? 'Creating...' : 'Create Group' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const props = defineProps({
  userId: Number
})

const emit = defineEmits(['close', 'created'])

const API_BASE_URL = (
  import.meta.env.VITE_API_BASE_URL ||
  import.meta.env.VITE_API_PROXY_TARGET ||
  ''
).replace(/\/+$/, '')

const formData = ref({
  name: '',
  description: ''
})

const submitting = ref(false)

const handleSubmit = async () => {
  if (!props.userId) {
    alert('You must be logged in to create a group.')
    return
  }

  submitting.value = true
  try {
    const payload = {
      name: formData.value.name,
      description: formData.value.description,
      created_by: props.userId
    }

    const response = await axios.post(`${API_BASE_URL}/api/groups/`, payload)
    emit('created', response.data)
  } catch (error) {
    console.error('Failed to create group:', error)
    alert(error.response?.data?.error || 'Failed to create group')
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

.group-form {
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
.form-group textarea:focus {
  outline: none;
  border-color: var(--color-accent);
}

.form-info {
  padding: 1rem;
  background: var(--color-background-mute);
  border-radius: 8px;
  margin-bottom: 1.5rem;
}

.form-info p {
  margin: 0;
  font-size: 0.9rem;
  color: var(--color-text);
}

.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
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