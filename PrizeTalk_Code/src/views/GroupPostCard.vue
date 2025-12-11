<template>
  <article class="group-post-card">
    <div class="post-header">
      <div class="author-info">
        <div class="post-meta">
          <span class="author-name">{{ post.username }}</span>
          <span class="separator">•</span>
          <span class="post-time">{{ formatTime(post.created_at) }}</span>
        </div>
      </div>
    </div>

    <div class="post-body">
      <h2 class="post-title">{{ post.title }}</h2>
      <p class="post-content">{{ post.content }}</p>
    </div>

    <div class="post-actions">
      <button 
        :class="['action-btn', { active: post.user_reaction === 'like' }]"
        @click="handleReact('like')"
      >
        <span class="icon">♥</span>
        <span>{{ post.likes_count || 0 }}</span>
      </button>

      <button 
        :class="['action-btn', { active: post.user_reaction === 'dislike' }]"
        @click="handleReact('dislike')"
      >
        <span class="icon">🅧</span>
        <span>{{ post.dislikes_count || 0 }}</span>
      </button>

      <button class="action-btn" @click="toggleComments">
        <span class="icon">✍︎</span>
        <span>{{ post.comments_count || 0 }}</span>
      </button>

      <button
        v-if="canDelete"
        class="delete-btn"
        @click="handleDelete">
        Delete
      </button>
    </div>

    <!-- Comments Section -->
    <div v-if="showComments" class="comments-section">
      <div class="comments-header">
        <h3>Comments ({{ post.comments_count }})</h3>
      </div>

      <div class="comment-form">
        <textarea 
          v-model="newComment"
          placeholder="Write a comment..."
          rows="3"
          class="comment-input"
        ></textarea>
        <button 
          @click="submitComment"
          :disabled="!newComment.trim() || submitting"
          class="submit-comment-btn"
        >
          {{ submitting ? 'Posting...' : 'Post Comment' }}
        </button>
      </div>

      <div class="comments-list">
        <div 
          v-for="comment in comments" 
          :key="comment.id"
          class="comment-item"
        >
          <div class="comment-header">
            <span class="comment-author">{{ comment.username }}</span>
            <span class="comment-time">{{ formatTime(comment.created_at) }}</span>
          </div>
          <p class="comment-text">{{ comment.comment_text }}</p>
          
          <div class="comment-actions">
            <button 
              :class="['comment-action-btn', { active: comment.user_reaction === 'like' }]"
              @click="handleCommentReact(comment.id, 'like')"
            >
              <span class="icon">♥</span>
              <span>{{ comment.likes_count || 0 }}</span>
            </button>

            <button 
              :class="['comment-action-btn', { active: comment.user_reaction === 'dislike' }]"
              @click="handleCommentReact(comment.id, 'dislike')"
            >
              <span class="icon">🅧</span>
              <span>{{ comment.dislikes_count || 0 }}</span>
            </button>

            <button 
              v-if="canDeleteComment(comment)"
              @click="deleteComment(comment.id)"
              class="delete-comment-btn"
            >
              Delete
            </button>
          </div>
        </div>
      </div>

      <div v-if="loadingComments" class="loading-comments">
        <div class="spinner-small"></div>
        <span>Loading comments...</span>
      </div>
    </div>
  </article>
</template>

<script setup>
import { ref, computed } from 'vue'
import axios from 'axios'

const props = defineProps({
  post: {
    type: Object,
    required: true
  },
  groupId: {
    type: Number,
    required: true
  },
  currentUserId: Number,
  currentUserRole: String,
  userGroupRole: String
})

const emit = defineEmits(['deleted', 'updated'])

const API_BASE_URL = (
  import.meta.env.VITE_API_BASE_URL ||
  import.meta.env.VITE_API_PROXY_TARGET ||
  ''
).replace(/\/+$/, '')

const showComments = ref(false)
const comments = ref([])
const newComment = ref('')
const loadingComments = ref(false)
const submitting = ref(false)

const canDelete = computed(() => {
  if (props.currentUserRole === 'staff_admin') return true
  if (props.userGroupRole === 'admin') return true
  return props.post.user_id === props.currentUserId
})

const canDeleteComment = (comment) => {
  if (props.currentUserRole === 'staff_admin') return true
  if (props.userGroupRole === 'admin') return true
  return comment.user_id === props.currentUserId
}

const handleReact = async (reactionType) => {
  if (!props.currentUserId) {
    alert('You must be logged in to react')
    return
  }

  try {
    const { data } = await axios.post(
      `${API_BASE_URL}/api/groups/${props.groupId}/posts/${props.post.id}/react/`,
      { 
        user_id: props.currentUserId,
        reaction_type: reactionType
      }
    )

    // Update local state
    const oldReaction = props.post.user_reaction
    props.post.user_reaction = data.reaction

    // Update counts
    if (oldReaction === 'like') props.post.likes_count = Math.max(0, (props.post.likes_count || 0) - 1)
    if (oldReaction === 'dislike') props.post.dislikes_count = Math.max(0, (props.post.dislikes_count || 0) - 1)
    
    if (data.reaction === 'like') props.post.likes_count = (props.post.likes_count || 0) + 1
    if (data.reaction === 'dislike') props.post.dislikes_count = (props.post.dislikes_count || 0) + 1

    emit('updated')
  } catch (err) {
    console.error('Failed to react:', err)
    alert('Failed to update reaction')
  }
}

const toggleComments = async () => {
  showComments.value = !showComments.value
  
  if (showComments.value && comments.value.length === 0) {
    await fetchComments()
  }
}

const fetchComments = async () => {
  loadingComments.value = true
  try {
    const { data } = await axios.get(
      `${API_BASE_URL}/api/groups/${props.groupId}/posts/${props.post.id}/comments/`,
      { params: { user_id: props.currentUserId } }
    )
    comments.value = data
  } catch (err) {
    console.error('Failed to fetch comments:', err)
  } finally {
    loadingComments.value = false
  }
}

const submitComment = async () => {
  if (!props.currentUserId) {
    alert('You must be logged in to comment')
    return
  }

  if (!newComment.value.trim()) return

  submitting.value = true
  try {
    const { data } = await axios.post(
      `${API_BASE_URL}/api/groups/${props.groupId}/posts/${props.post.id}/comments/`,
      {
        user_id: props.currentUserId,
        comment_text: newComment.value
      }
    )

    comments.value.push(data)
    props.post.comments_count = (props.post.comments_count || 0) + 1
    newComment.value = ''
    emit('updated')
  } catch (err) {
    console.error('Failed to post comment:', err)
    alert('Failed to post comment')
  } finally {
    submitting.value = false
  }
}

const handleCommentReact = async (commentId, reactionType) => {
  if (!props.currentUserId) {
    alert('You must be logged in to react')
    return
  }

  try {
    const { data } = await axios.post(
      `${API_BASE_URL}/api/groups/${props.groupId}/posts/${props.post.id}/comments/${commentId}/react/`,
      { 
        user_id: props.currentUserId,
        reaction_type: reactionType
      }
    )

    // Update local comment state
    const comment = comments.value.find(c => c.id === commentId)
    if (comment) {
      const oldReaction = comment.user_reaction
      comment.user_reaction = data.reaction

      if (oldReaction === 'like') comment.likes_count = Math.max(0, (comment.likes_count || 0) - 1)
      if (oldReaction === 'dislike') comment.dislikes_count = Math.max(0, (comment.dislikes_count || 0) - 1)
      
      if (data.reaction === 'like') comment.likes_count = (comment.likes_count || 0) + 1
      if (data.reaction === 'dislike') comment.dislikes_count = (comment.dislikes_count || 0) + 1
    }
  } catch (err) {
    console.error('Failed to react to comment:', err)
    alert('Failed to update reaction')
  }
}

const deleteComment = async (commentId) => {
  if (!confirm('Delete this comment?')) return

  try {
    await axios.delete(
      `${API_BASE_URL}/api/groups/${props.groupId}/posts/${props.post.id}/comments/${commentId}/`,
      { data: { user_id: props.currentUserId } }
    )

    comments.value = comments.value.filter(c => c.id !== commentId)
    props.post.comments_count = Math.max(0, (props.post.comments_count || 0) - 1)
    emit('updated')
  } catch (err) {
    console.error('Failed to delete comment:', err)
    alert('Failed to delete comment')
  }
}

const handleDelete = async () => {
  if (!confirm('Delete this post?')) return

  try {
    await axios.delete(
      `${API_BASE_URL}/api/groups/${props.groupId}/posts/${props.post.id}/`,
      { data: { user_id: props.currentUserId } }
    )
    emit('deleted', props.post.id)
  } catch (err) {
    console.error('Failed to delete post:', err)
    alert('Failed to delete post')
  }
}

const formatTime = (timestamp) => {
  if (!timestamp) return ''
  const date = new Date(timestamp)
  const now = new Date()
  const diffMs = now - date
  const diffMins = Math.floor(diffMs / 60000)
  const diffHours = Math.floor(diffMs / 3600000)
  const diffDays = Math.floor(diffMs / 86400000)

  if (diffMins < 60) return `${diffMins}m ago`
  if (diffHours < 24) return `${diffHours}h ago`
  if (diffDays < 7) return `${diffDays}d ago`
  return date.toLocaleDateString()
}
</script>

<style scoped>
.group-post-card {
  background: var(--color-background-soft);
  border: 1px solid var(--color-border);
  border-radius: 12px;
  padding: 1.5rem;
  transition: all 0.3s ease;
  overflow: hidden;
}

.group-post-card:hover {
  box-shadow: var(--shadow-hover);
  transform: translateY(-2px);
}

.post-header {
  margin-bottom: 1rem;
}

.author-info {
  display: flex;
  gap: 0.75rem;
  align-items: center;
}

.post-meta {
  font-size: 0.85rem;
  color: var(--color-text-muted);
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.author-name {
  font-weight: 600;
  color: var(--color-text);
}

.post-body {
  margin-bottom: 1rem;
}

.post-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--color-heading);
  margin-bottom: 0.75rem;
  line-height: 1.3;
}

.post-content {
  color: var(--color-text);
  line-height: 1.6;
  white-space: pre-wrap;
}

.post-actions {
  display: flex;
  gap: 1rem;
  padding-top: 1rem;
  border-top: 1px solid var(--color-border);
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 0.75rem;
  border: none;
  background: transparent;
  color: var(--color-text-muted);
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s ease;
}

.action-btn:hover {
  background: var(--color-background-mute);
  color: var(--color-text);
}

.action-btn.active {
  color: var(--color-button-bg);
  background: var(--color-background-mute);
}

.icon {
  font-size: 1.1rem;
}

.delete-btn {
  background: transparent;
  color: #dc2626;
  border: none;
  padding: 0.5rem 0.75rem;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s ease;
  margin-left: auto;
}

.delete-btn:hover {
  background: rgba(220, 38, 38, 0.1);
}

/* Comments Section */
.comments-section {
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid var(--color-border);
  animation: slideDown 0.3s ease;
}

@keyframes slideDown {
  from {
    opacity: 0;
    max-height: 0;
  }
  to {
    opacity: 1;
    max-height: 2000px;
  }
}

.comments-header h3 {
  font-size: 1.1rem;
  color: var(--color-heading);
  font-weight: 600;
  margin-bottom: 1rem;
}

.comment-form {
  margin-bottom: 1.5rem;
}

.comment-input {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid var(--color-border);
  box-sizing: border-box;
  border-radius: 8px;
  font-family: inherit;
  font-size: 0.95rem;
  resize: vertical;
  margin-bottom: 0.75rem;
  background: var(--color-background-soft);
  color: var(--color-text);
}

.comment-input:focus {
  outline: none;
  border-color: var(--color-border-hover);
}

.submit-comment-btn {
  padding: 0.5rem 1rem;
  background: var(--color-button-bg);
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.submit-comment-btn:hover:not(:disabled) {
  background: var(--color-button-hover-bg);
}

.submit-comment-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.comments-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.comment-item {
  padding: 1rem;
  background: var(--color-background-mute);
  border-radius: 8px;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.comment-author {
  font-weight: 600;
  color: var(--color-heading);
  font-size: 0.9rem;
}

.comment-time {
  font-size: 0.75rem;
  color: var(--color-text-muted);
}

.comment-text {
  color: var(--color-text);
  line-height: 1.5;
  font-size: 0.95rem;
  margin-bottom: 0.75rem;
  white-space: pre-wrap;
}

.comment-actions {
  display: flex;
  gap: 0.75rem;
  align-items: center;
}

.comment-action-btn {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.25rem 0.5rem;
  border: none;
  background: transparent;
  color: var(--color-text-muted);
  border-radius: 4px;
  cursor: pointer;
  font-weight: 600;
  font-size: 0.875rem;
  transition: all 0.3s ease;
}

.comment-action-btn:hover {
  background: rgba(0, 0, 0, 0.05);
}

.comment-action-btn.active {
  color: var(--color-button-bg);
}

.delete-comment-btn {
  background: transparent;
  color: #dc2626;
  border: none;
  padding: 0.25rem 0.5rem;
  font-size: 0.85rem;
  cursor: pointer;
  font-weight: 600;
  transition: color 0.3s ease;
}

.delete-comment-btn:hover {
  color: #b91c1c;
}

.loading-comments {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 1rem;
  color: var(--color-text-muted);
  font-size: 0.9rem;
}

.spinner-small {
  width: 20px;
  height: 20px;
  border: 2px solid var(--color-border);
  border-top-color: var(--color-button-bg);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}


@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>