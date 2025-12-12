<template>
  <article class="award-card" @click="showDetails = !showDetails">
    <div class="card-header">
      <div class="award-badge">
        <span class="badge-icon">{{ getBadgeIcon() }}</span>
      </div>
      <div class="award-meta">
        <span v-if="getYear()" class="year-badge">
          {{ getYear() }}
        </span>
        <span v-if="getCategory()" class="category-badge">
          {{ getCategory()}}
        </span>
      </div>
    </div>

    <div class="card-body">
      <h3 class="winner-name">
        {{ getWinnerName() }}
      </h3>

      <p v-if="getWorkTitle()" class="work-title">
        {{getWorkTitle()}}
      </p>

      <div v-if="hasAdditionalInfo()" class="additional-info">
        <div v-if="getNationality()" class="info-item">
          <span class="info-label">Country:</span>
          <span class="info-value">{{ getNationality() }}</span>
        </div>
        <div v-if="getGenre()" class="info-item">
          <span class="info-label">Genre:</span>
          <span class="info-value">{{ getGenre() }}</span>
        </div>
        <div v-if="getCeremony()" class="info-item">
          <span class="info-label">Ceremony:</span>
          <span class="info-value">{{ getCeremony() }}</span>
        </div>
        <div v-if="isWinner()" class="info-item">
          <span class="winner-badge">𐃯 Winner</span>
        </div>
      </div>
    </div>

    <div v-if="showDetails" class="card-details">
      <div class="details-grid">
        <div 
          v-for="(value, key) in filteredAwardData" 
          :key="key"
          class="detail-item"
        >
          <span class="detail-label">{{ formatKey(key) }}:</span>
          <span class="detail-value">{{ formatValue(value) }}</span>
        </div>
      </div>
    </div>

    <div class="card-footer">
      <button class="expand-btn" @click.stop="showDetails = !showDetails">
        {{ showDetails ? 'Show Less' : 'Show More' }}
        <span class="expand-icon">{{ showDetails ? '▲' : '▼' }}</span>
      </button>
    </div>
  </article>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  award: {
    type: Object,
    required: true
  },
  columns: {
    type: Array,
    default: () => []
  }
})

const showDetails = ref(false)

const getBadgeIcon = () => {
  const cat = getCategory()?.toLowerCase() || ''
  
  if (cat.includes('film') || cat.includes('picture') || cat.includes('director')) return '⏯'
  if (cat.includes('music') || cat.includes('song') || cat.includes('album')) return '♫'
  if (cat.includes('literature') || cat.includes('novel') || cat.includes('book')) return '✎'
  if (cat.includes('peace')) return '☮︎'
  if (cat.includes('physics')) return '⚛'
  if (cat.includes('chemistry')) return '⌬'
  if (cat.includes('medicine') || cat.includes('physiology')) return '✙'
  if (cat.includes('economics') || cat.includes('economic')) return '$'
  if (cat.includes('actor') || cat.includes('actress')) return '✮'
  
  return '𐃯'
}

const getYear = () => {
  let year =  props.award.YEAR || 
         props.award.Year || 
         props.award.year ||
         props.award.awardYear ||
         props.award.award_year ||
         null
  if (typeof year === 'string' && year.includes('/')) {
    year = year.split('/')[0]  // take only first year
  }
  return year
}

const getCategory = () => {
  return props.award.Category || 
         props.award.category ||
         props.award.category_en ||
         props.award.categoryFullName_en ||
         props.award.Award_Name ||
         props.award.award ||
         props.award.GENRE ||
         null
}

const getWinnerName = () => {
  if (props.award.full_name) return props.award.full_name
  if (props.award.title) return props.award.title
  if (props.award.known_name) return props.award.known_name
  if (props.award.WINNER) return props.award.WINNER
  if (props.award.orgName_en) return props.award.orgName_en
  if (props.award.Nominee) return props.award.Nominee
  if (props.award.Name) return props.award.Name
  if (props.award.winner) return props.award.winner
  if (props.award.artist) return props.award.artist
  if (props.award.author) return props.award.author
  if (props.award.name) return props.award.name

  return 'Unknown'
}



const getWorkTitle = () => {
  return props.award.motivation ||              // Nobel-style motivation
         props.award.categoryTopMotivation ||  // sometimes used
         props.award.title ||                  // generic title
         props.award.Title ||                  // capitalized variant
         props.award.NOVEL ||                  // literature field
         props.award.Film ||                   // film field
         props.award.Work ||                   // generic field
         props.award.topMotivation_en ||      // English variant
         ''
}

const getNationality = () => {
  return props.award.NATIONALITY_AT_TIME_OF_VICTORY ||
         props.award.COUNTRY_OF_BIRTH ||
         props.award.birth_place_country_en ||
         props.award.country ||
         props.award.Country ||
         null
}

const getGenre = () => {
  return props.award.GENRE ||
         props.award.genre ||
         props.award.Genre ||
         props.award.Award_Type ||
         null
}

const getCeremony = () => {
  return props.award.Ceremony ||
         props.award.ceremony ||
         null
}

const isWinner = () => {
  if (props.award.Winner === true || props.award.Winner === 'True' || props.award.Winner === 1) return true
  if (props.award.winner === true || props.award.winner === 'True' || props.award.winner === 1) return true
  return false
}

const hasAdditionalInfo = () => {
  return getNationality() || getGenre() || getCeremony() || isWinner()
}

const filteredAwardData = computed(() => {
  const excluded = ['id', 'ID', 'index', 'SL_NO', 'award_id', 'fileName']
  const filtered = {}
  
  for (const [key, value] of Object.entries(props.award)) {
    if (!excluded.includes(key) && value !== null && value !== undefined && value !== '') {
      filtered[key] = value
    }
  }
  
  return filtered
})

const formatKey = (key) => {
  return key
    .replace(/_/g, ' ')
    .replace(/\b\w/g, l => l.toUpperCase())
}

const formatValue = (value) => {
  if (value === null || value === undefined) return '-'
  if (typeof value === 'boolean') return value ? 'Yes' : 'No'
  if (value === 'True' || value === 'true' || value === 1) return 'Yes'
  if (value === 'False' || value === 'false' || value === 0) return 'No'
  return value.toString()
}



</script>

<style scoped>
.award-card {
  background: var(--color-background-soft);
  border: 1px solid var(--color-border);
  border-radius: 12px;
  padding: 1.5rem;
  transition: all 0.3s ease;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  width: 300px; 
}

.award-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, var(--color-accent), var(--color-button-bg));
  opacity: 0;
  transition: opacity 0.3s ease;
}

.award-card:hover {
  box-shadow: var(--shadow-hover);
  transform: translateY(-4px);
  border-color: var(--color-border-hover);
}

.award-card:hover::before {
  opacity: 1;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
}

.award-badge {
  width: 50px;
  height: 50px;
  background: var(--color-background-mute);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  flex-shrink: 0;
}

.award-meta {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  align-items: flex-end;
  flex: 1;
  margin-left: 1rem;
}

.year-badge {
  background: var(--color-button-bg);
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 6px;
  font-weight: 700;
  font-size: 0.875rem;
}

.category-badge {
  background: var(--color-background-mute);
  color: var(--color-text-muted);
  padding: 0.25rem 0.75rem;
  border-radius: 6px;
  font-size: 0.75rem;
  font-weight: 600;
  text-align: right;
  word-break: break-word;
}

.card-body {
  min-height: 180px; 
  margin-bottom: 1rem;
}

.winner-name {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--color-heading);
  margin-bottom: 0.5rem;
  line-height: 1.3;
  max-height: 3.9em;
  overflow: hidden;
  text-overflow: ellipsis;
}


.work-title {
  color: var(--color-text);
  font-size: 0.95rem;
  line-height: 1.5;
  margin-bottom: 1rem;
  font-style: italic;
  max-height: 4.5em;
  overflow: hidden;
  text-overflow: ellipsis;
}

.additional-info {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid var(--color-border);
}

.info-item {
  display: flex;
  gap: 0.5rem;
  font-size: 0.875rem;
}

.info-label {
  font-weight: 600;
  color: var(--color-text-muted);
  min-width: 120px;
}

.info-value {
  color: var(--color-text);
}

.winner-badge {
  background: linear-gradient(135deg, var(--color-accent), var(--color-button-bg));
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 6px;
  font-weight: 700;
  font-size: 0.875rem;
}

.card-details {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid var(--color-border);
  animation: slideDown 0.3s ease;
  max-height: 400px;
  overflow-y: auto;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.details-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 0.75rem;
}

.detail-item {
  display: flex;
  gap: 0.5rem;
  font-size: 0.875rem;
}

.detail-label {
  font-weight: 600;
  color: var(--color-text-muted);
  min-width: 120px;
  flex-shrink: 0;
}

.detail-value {
  color: var(--color-text);
  word-break: break-word;
}

.card-footer {
  margin-top: 1rem;
  display: flex;
  justify-content: center;
}

.expand-btn {
  padding: 0.5rem 1rem;
  border: 2px solid var(--color-border);
  background: transparent;
  color: var(--color-text-muted);
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  font-size: 0.875rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.3s ease;
}

.expand-btn:hover {
  border-color: var(--color-border-hover);
  background: var(--color-background-mute);
  color: var(--color-text);
}

.expand-icon {
  font-size: 0.75rem;
}

@media (prefers-color-scheme: dark) {
  .award-badge {
    background: rgba(59, 130, 246, 0.1);
  }

  .year-badge {
    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  }
}
</style>