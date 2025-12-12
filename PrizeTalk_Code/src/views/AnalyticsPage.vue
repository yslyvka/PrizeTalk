<template>
  <div class="analytics-page">
    <!-- Header -->
    <div class="analytics-header">
      <h1>Analytics Dashboard</h1>
      <p class="subtitle">Explore insights from award data</p>
    </div>
    <div class="card">
      <AwardAnalytics/>
    </div>
  </div>
</template>

<script setup>
import AwardAnalytics from './AwardAnalytics.vue'
</script>

<style scoped>
.analytics-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

.analytics-header {
  margin-bottom: 2rem;
}

.analytics-header h1 {
  color: var(--color-heading);
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

.subtitle {
  color: var(--color-text-muted);
  margin-bottom: 1.5rem;
}

.card {
  background: var(--color-background-soft);
  border: 2px solid var(--color-border);
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}
</style>