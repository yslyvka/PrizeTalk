<template>
  <article class="group-card">
    <div class="card-header">
      <div class="group-icon">𖠋𖠋</div>
      <div class="group-meta">
        <span class="member-count">
          {{ group.member_count || 0 }} members
        </span>
      </div>
    </div>

    <div class="card-body">
      <h3 class="group-name">{{ group.name }}</h3>
      <p v-if="group.description" class="group-description">
        {{ truncate(group.description, 120) }}
      </p>

      <div class="group-stats">
        <div class="stat-item">
          <span class="stat-icon">✉︎</span>
          <span>{{ group.post_count || 0 }} posts</span>
        </div>
        <div class="stat-item">
          <span class="stat-icon">𖠋</span>
          <span>Created by {{ group.creator_username }}</span>
        </div>
      </div>

      <div v-if="group.user_role" class="role-badge">
        {{ getRoleLabel(group.user_role) }}
      </div>
    </div>

    <div class="card-actions">
      <button 
        v-if="!isMember"
        class="action-btn primary"
        @click.stop="$emit('join', group.id)"
      >
        Join Group
      </button>

      <template v-else>
        <button 
          class="action-btn"
          @click.stop="$emit('view', group.id)"
        >
          View Posts
        </button>

        <button 
          v-if="canLeave"
          class="action-btn secondary"
          @click.stop="$emit('leave', group.id)"
        >
          Leave
        </button>
      </template>

      <button 
        v-if="canDelete"
        class="action-btn danger"
        @click.stop="$emit('delete', group.id)"
      >
        Delete Group
      </button>
    </div>
  </article>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  group: Object,
  currentUserId: Number,
  currentUserRole: String
})

defineEmits(['join', 'leave', 'delete', 'view'])

const isMember = computed(() => {
  return props.group.user_role !== null && props.group.user_role !== undefined
})

const canLeave = computed(() => {
  // Creator cannot leave
  return props.group.created_by !== props.currentUserId
})

const canDelete = computed(() => {
  // Staff admin can delete any group
  if (props.currentUserRole === 'staff_admin') return true
  
  // Group admin or creator can delete
  return props.group.user_role === 'admin' || props.group.created_by === props.currentUserId
})

const getRoleLabel = (role) => {
  const labels = {
    admin: '♛ Admin',
    moderator: '⛊ Moderator',
    member: '✓ Member'
  }
  return labels[role] || role
}

const truncate = (text, length) => {
  if (!text) return ''
  return text.length > length ? text.substring(0, length) + '...' : text
}
</script>

<style scoped>
.group-card {
  background: var(--color-background-soft);
  border: 1px solid var(--color-border);
  border-radius: 12px;
  padding: 1.5rem;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
}

.group-card:hover {
  box-shadow: var(--shadow-hover);
  transform: translateY(-2px);
  border-color: var(--color-border-hover);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
}

.group-icon {
  width: 50px;
  height: 50px;
  background: var(--color-background-mute);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
}

.group-meta {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.member-count {
  background: var(--color-button-bg);
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 6px;
  font-weight: 700;
  font-size: 0.875rem;
}

.card-body {
  flex: 1;
  margin-bottom: 1rem;
}

.group-name {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--color-heading);
  margin-bottom: 0.5rem;
  line-height: 1.3;
}

.group-description {
  color: var(--color-text);
  font-size: 0.95rem;
  line-height: 1.5;
  margin-bottom: 1rem;
}

.group-stats {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  padding: 0.75rem;
  background: var(--color-background-mute);
  border-radius: 8px;
  margin-bottom: 1rem;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: var(--color-text-muted);
}

.stat-icon {
  font-size: 1rem;
}

.role-badge {
  background: linear-gradient(135deg, var(--color-accent), var(--color-button-bg));
  color: white;
  padding: 0.5rem 0.75rem;
  border-radius: 6px;
  font-weight: 700;
  font-size: 0.875rem;
  text-align: center;
}

.card-actions {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.action-btn {
  flex: 1;
  padding: 0.5rem 1rem;
  border: 2px solid var(--color-border);
  background: transparent;
  color: var(--color-text);
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.9rem;
}

.action-btn:hover {
  border-color: var(--color-border-hover);
  background: var(--color-background-mute);
}

.action-btn.primary {
  background: var(--color-button-bg);
  color: white;
  border-color: var(--color-button-bg);
}

.action-btn.primary:hover {
  background: var(--color-button-hover-bg);
  border-color: var(--color-button-hover-bg);
}

.action-btn.secondary {
  border-color: var(--color-text-muted);
  color: var(--color-text-muted);
}

.action-btn.danger {
  background: #dc2626;
  color: white;
  border-color: #dc2626;
}

.action-btn.danger:hover {
  background: #b91c1c;
  border-color: #b91c1c;
}

@media (prefers-color-scheme: dark) {
  .group-icon {
    background: rgba(59, 130, 246, 0.1);
  }

  .member-count {
    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  }
}
</style>