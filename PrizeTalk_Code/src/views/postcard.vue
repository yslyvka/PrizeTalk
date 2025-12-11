<template>
  <article class="post-card">
    <div class="post-header">
      <div class="author-info">
        <div>
          <div class="post-meta">
            <span class="author-name">{{ post.username }}</span>
            <span class="post-type">{{ post.post_type }}</span>
            <span class="separator">•</span>
            <span class="post-time">{{ formatTime(post.created_at) }}</span>
          </div>
        </div>
      </div>

      <button
        :class="['bookmark-btn', { following: post.is_bookmarked }]"
        @click="toggleBookmark"
      >
        {{ post.is_bookmarked ? 'Bookmarked' : 'Bookmark' }}
      </button>
    </div>

    <div class="post-body">
      <h2 class="post-title">{{ post.title }}</h2>
      <p class="post-content">{{ truncateContent(post.content) }}</p>

      <div v-if="post.tags.length > 0" class="post-tags">
        <span v-for="tag in post.tags" :key="tag" class="tag">
          #{{ tag }}
        </span>
      </div>

      <div v-if="hasRelatedContent" class="related-content">
        <span class="related-label">Related to:</span>
        <span v-if="post.related_award_id" class="related-item">
          𐃯 Award #{{ post.related_award_id }}
        </span>
        <span v-if="post.related_winner_id" class="related-item">
          🜲 Winner #{{ post.related_winner_id }}
        </span>
      </div>
    </div>

    <div class="post-actions">
      <button 
        :class="['action-btn', { liked: post.user_reaction === 'like' }]"
        @click="() => toggleReaction('like')"
      >
        <span class="icon" style="font-size: 1.5em;">
          {{ post.user_reaction === 'like' ? '♥︎' : '♡' }}
        </span>
        <span>{{ post.likes_count }}</span>
      </button>

      <button 
        :class="['action-btn', { liked: post.user_reaction === 'dislike' }]"
        @click="() => toggleReaction('dislike')"
      >
        <span class="icon" style="font-size: 1.5em;">
          {{ post.user_reaction === 'dislike' ? '🅧' : 'Ⓧ' }}
        </span>
        <span>{{ post.dislikes_count }}</span>
      </button>


      <button class="action-btn" @click="toggleComments">
        <span class="icon" style="font-size: 2.0em;">✍︎</span>
        <span>{{ post.comments_count }}</span>
      </button>

      <button class="action-btn">
        <span class="icon" style="font-size: 2.0em;">⌯⌲</span>
        <span>Share</span>
      </button>

      <button
      v-if="props.currentUserRole === 'staff_admin'"
      class="action-btn delete-btn"
      @click="deletePost(post.id)">
        Delete
      </button>
    </div>
        <!-- Comments Section -->
    <div v-if="showComments" class="comments-section">
      <div class="comments-header">
        <h3>Comments ({{ comments.length }})</h3>
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

          <button 
            v-if="canDeleteComment(comment)"
            @click="deleteComment(comment.id)"
            class="delete-comment-btn"
          >
            Delete
          </button>
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
import { computed, ref } from 'vue'
import axios from 'axios'

const props = defineProps({
  post: Object,
  currentUserId: Number,
  currentUserRole: String,
})

const emit = defineEmits(['like', 'comment', 'bookmark', 'deleted'])

const API_BASE_URL = (
  import.meta.env.VITE_API_BASE_URL ||
  import.meta.env.VITE_API_PROXY_TARGET ||
  ''
).replace(/\/+$/, '')

const deletePost = async (postId) => {
  if (!confirm("Are you sure you want to delete this post?")) return

  try {
    await axios.delete(`${API_BASE_URL}/api/community/${postId}/`, {
      data: { current_user_id: props.currentUserId }
    })
    alert("Post deleted!")

    emit('deleted', postId)
  } catch (err) {
    console.error(err)
    alert("Failed to delete post")
  }
}

const hasRelatedContent = computed(() => {
  return props.post.related_award_id || props.post.related_winner_id
})

const truncateContent = (content, maxLength = 300) => {
  if (content.length <= maxLength) return content
  return content.substring(0, maxLength) + '...'
}

const formatTime = (timestamp) => {
  const postDate = new Date(timestamp + "-0500");
  const now = new Date();

  const diffMs = now.getTime() - postDate.getTime();

  const diffSeconds = Math.floor(diffMs / 1000);
  const diffMins = Math.floor(diffSeconds / 60);
  const diffHours = Math.floor(diffMins / 60);
  const diffDays = Math.floor(diffHours / 24);
  const diffMonths = Math.floor(diffDays / 30);
  const diffYears = Math.floor(diffDays / 365);

  if (diffYears > 0) return `${diffYears}y ago`;
  if (diffMonths > 0) return `${diffMonths}mo ago`;
  if (diffDays > 0) return `${diffDays}d ago`;
  if (diffHours > 0) return `${diffHours}h ago`;
  if (diffMins > 0) return `${diffMins}m ago`;
  if (diffSeconds > 0) return `${diffSeconds}s ago`;
  return 'just now';
};

const showComments = ref(false)
const comments = ref([])
const newComment = ref('')
const loadingComments = ref(false)
const submitting = ref(false)

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
      `${API_BASE_URL}/api/community/${props.post.id}/comments/`
    )
    comments.value = data
  } finally {
    loadingComments.value = false
  }
}

const submitComment = async () => {
  submitting.value = true
  try {
    const { data } = await axios.post(
      `${API_BASE_URL}/api/community/${props.post.id}/comments/`,
      {
        user_id: props.currentUserId,
        comment_text: newComment.value
      }
    )
    comments.value.push(data)
    props.post.comments_count++
    emit('comment', { postId: props.post.id, newCount: props.post.comments_count })
    newComment.value = ''
  } finally {
    submitting.value = false
  }
}


const canDeleteComment = (comment) => {
  return props.currentUserRole === "staff_admin" ||
         comment.user_id === props.currentUserId
}

const deleteComment = async (commentId) => {
  await axios.delete(
    `${API_BASE_URL}/api/community/${props.post.id}/comments/${commentId}/`,
    { data: { current_user_id: props.currentUserId } }
  )
  comments.value = comments.value.filter(c => c.id !== commentId)
  props.post.comments_count--
}

const toggleReaction = async (type) => {
  if (!props.currentUserId) return // user not logged in

  try {
    const { data } = await axios.post(
      `${API_BASE_URL}/api/community/${props.post.id}/react/`,
      {
        user_id: props.currentUserId,
        reaction_type: type, // 'like' or 'dislike'
      }
    )

    // Handle backend response
    switch (data.status) {
      case 'added':
        if (type === 'like') props.post.likes_count++
        else props.post.dislikes_count++
        props.post.user_reaction = type
        break

      case 'removed':
        if (type === 'like') props.post.likes_count = Math.max(0, props.post.likes_count - 1)
        else props.post.dislikes_count = Math.max(0, props.post.dislikes_count - 1)
        props.post.user_reaction = null
        break

      case 'updated':
        if (type === 'like') {
          props.post.likes_count++
          props.post.dislikes_count = Math.max(0, props.post.dislikes_count - 1)
        } else {
          props.post.dislikes_count++
          props.post.likes_count = Math.max(0, props.post.likes_count - 1)
        }
        props.post.user_reaction = type
        break
    }
  } catch (err) {
    console.error("Failed to react:", err)
    alert("Failed to react to post")
  }
}

const toggleBookmark = async () => {
  if (!props.currentUserId) return

  try {
    const { data } = await axios.post(
      `${API_BASE_URL}/api/community/${props.post.id}/bookmark/`,
      { user_id: props.currentUserId }
    )

    props.post.is_bookmarked = (data.status === "added")
  } catch (err) {
    console.error("Failed to toggle bookmark:", err)
    alert("Failed to bookmark post")
  }
}

</script>

<style scoped>
.post-card {
  background: var(--color-background-soft);
  border: 1px solid var(--color-border);
  border-radius: 12px;
  padding: 1.5rem;
  transition: all 0.3s ease;
}

.post-card:hover {
  box-shadow: var(--shadow-hover);
  transform: translateY(-2px);
}

.post-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
}

.author-info {
  display: flex;
  gap: 0.75rem;
  align-items: center;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
}

.author-name {
  font-weight: 600;
  color: var(--color-text);
  text-decoration: none;
}

.author-name:hover {
  color: var(--color-accent);
}

.post-meta {
  font-size: 0.85rem;
  color: var(--color-text-muted);
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.post-type {
  background: var(--color-background-mute);
  padding: 0.125rem 0.5rem;
  border-radius: 4px;
  text-transform: capitalize;
}

.bookmark-btn {
  padding: 0.375rem 0.875rem;
  border: 2px solid var(--color-button-bg);
  background: transparent;
  color: var(--color-button-bg);
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.bookmark-btn:hover {
  background: var(--color-button-bg);
  color: white;
}

.bookmark-btn.following {
  background: var(--color-button-bg);
  color: white;
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
  margin-bottom: 1rem;
}

.post-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.tag {
  background: var(--color-background-mute);
  color: var(--color-accent);
  padding: 0.25rem 0.75rem;
  border-radius: 6px;
  font-size: 0.875rem;
  font-weight: 600;
}

.related-content {
  display: flex;
  gap: 0.5rem;
  align-items: center;
  font-size: 0.875rem;
  color: var(--color-text-muted);
  padding: 0.75rem;
  background: var(--color-background-mute);
  border-radius: 8px;
}

.related-label {
  font-weight: 600;
}

.related-item {
  background: white;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
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

.action-btn.liked {
  color: var(--color-button-bg);
}

.icon {
  font-size: 1.1rem;
}

.delete-btn {
  margin-left: auto;
  background: #e54848;
  color: white;
  padding: 0.5rem 0.75rem;
  border-radius: 6px;
  border: none;
}

.delete-btn:hover {
  background: #c43d3d;
  transform: translateY(-1px);
}

.comments-section {
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid var(--color-border);
}

.comment-form {
  margin-bottom: 1.5rem;
}

.comment-input {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid var(--color-border);
  border-radius: 8px;
  background: var(--color-background-soft);
  color: var(--color-text);
  margin-bottom: 0.75rem;
}

.submit-comment-btn {
  padding: 0.5rem 1rem;
  background: var(--color-button-bg);
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
}

.comment-item {
  padding: 1rem;
  background: var(--color-background-mute);
  border-radius: 8px;
  margin-bottom: 1rem;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  font-size: 0.85rem;
  margin-bottom: 0.5rem;
}

.delete-comment-btn {
  background: #e54848;
  border: none;
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 6px;
  font-size: 0.8rem;
  margin-top: 0.5rem;
  cursor: pointer;
}

.comment-input {
  width: 100%;
  box-sizing: border-box;
  padding: 0.75rem;
  border: 2px solid var(--color-border);
  border-radius: 8px;
  background: var(--color-background-soft);
  color: var(--color-text);
  margin-bottom: 0.75rem;
}

</style>
