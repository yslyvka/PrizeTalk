<template>
  <div class="awards-page">
    <div class="awards-header">
      <h1>Awards</h1>
      <p class="subtitle">Explore winners and nominees across all prestigious awards</p>

      <div class="filters-section">
        <div class="filter-tabs">
          <button 
            :class="['tab-btn', { active: activeAward === 'all' }]"
            @click="activeAward = 'all'"
          >
            ⌕ All Awards
          </button>
          <button 
            v-for="award in awards" 
            :key="award.id"
            :class="['tab-btn', { active: activeAward === award.id }]"
            @click="activeAward = award.id"
          >
            <span class="award-icon">{{ getAwardIcon(award.award_name) }}</span>
            {{ award.award_name }}
          </button>
        </div>

        <div class="view-controls">
          <button 
            :class="['view-btn', { active: viewMode === 'cards' }]"
            @click="viewMode = 'cards'"
            title="Card View"
          >
            <span class="icon">▦</span>
          </button>
          <button 
            :class="[
              'view-btn', 
              { active: viewMode === 'table', disabled: activeAward === 'all' }
            ]"
            @click="activeAward !== 'all' && (viewMode = 'table')"
            :disabled="activeAward === 'all'"
            title="Table View (disabled in All mode)"
          >
            <span class="icon">☰</span>
          </button>
        </div>
      </div>

      <div class="search-bar">
        <input 
          v-model="searchQuery" 
          type="search" 
          placeholder="Search winners, categories, years..." 
          class="search-input"
        />
      </div>
    </div>

    <div class="awards-container">
      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
        <p>Loading award data...</p>
      </div>

      <div v-else-if="filteredRows.length === 0" class="empty-state">
        <div class="empty-icon">𐃯</div>
        <p>No results found</p>
        <p class="empty-hint">Try adjusting your search or select a different award</p>
      </div>

      <!-- Card View -->
      <div v-else-if="viewMode === 'cards'" class="cards-grid">
        <AwardCard 
          v-for="(row, index) in filteredRows" 
          :key="index"
          :award="row"
          :columns="columns"
        />
      </div>

      <!-- Table View -->
      <div v-else class="table-wrapper">
        <div class="table-container">
          <table class="award-table">
            <thead>
              <tr>
                <th v-for="col in displayColumns" :key="col" @click="sortBy(col)">
                  {{ formatColumnName(col) }}
                  <span v-if="sortColumn === col" class="sort-indicator">
                    {{ sortDirection === 'asc' ? '↑' : '↓' }}
                  </span>
                </th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(row, index) in filteredRows" :key="index">
                <td v-for="col in displayColumns" :key="col" :data-label="formatColumnName(col)">
                  {{ formatCellValue(row[col]) }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Pagination -->
      <div v-if="totalPages > 1" class="pagination">
        <button 
          @click="currentPage--" 
          :disabled="currentPage === 1"
          class="page-btn"
        >
          ← Previous
        </button>
        <span class="page-info">Page {{ currentPage }} of {{ totalPages }}</span>
        <button 
          @click="currentPage++" 
          :disabled="currentPage === totalPages"
          class="page-btn"
        >
          Next →
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import axios from 'axios'
import AwardCard from './AwardCard.vue'

const API_BASE_URL = import.meta.env.VITE_API_PROXY_TARGET || ''

const awards = ref([])
const activeAward = ref(null)
const awardRows = ref([])
const columns = ref([])
const loading = ref(true)
const viewMode = ref('cards')
const searchQuery = ref('')
const currentPage = ref(1)
const itemsPerPage = 12
const sortColumn = ref(null)
const sortDirection = ref('asc')

const tableMapping = {
  1: "booker_prize",
  2: "golden_globes",
  3: "grammy",
  4: "nobel_prizes",
  5: "oscars"
}

// Define which columns to show for each award type
const columnMapping = {
  booker_prize: ['YEAR', 'WINNER', 'NOVEL', 'GENRE', 'NATIONALITY_AT_TIME_OF_VICTORY', 'PUBLISHER', 'AGE_WHEN_WON'],
  golden_globes: ['year', 'award', 'title', 'Name', 'Winner'],
  grammy: ['Year', 'Award_Name', 'Work', 'Nominee', 'Nominee'],
  nobel_prizes: ['award_year', 'full_name', 'category', 'birth_country', 'prize_amount'],
  oscars: ['Year', 'Category', 'Film', 'Name', 'Nominees']
}

const displayColumns = computed(() => {
  if (!activeAward.value || columns.value.length === 0) return []
  
  const tableName = tableMapping[activeAward.value]
  const preferredColumns = columnMapping[tableName] || []
  
  // Filter to only show columns that exist in the data
  return preferredColumns.filter(col => columns.value.includes(col))
})

const getAwardIcon = (name) => {
  const icons = {
    'Booker Prize': '✎ᝰ.',
    'Golden Globes': '𖧋',
    'Grammy': '♫',
    'Nobel Prize': '🏅',
    'Oscars': '⏯'
  }
  return icons[name] || '𐃯'
}

const formatColumnName = (col) => {
  return col
    .replace(/_/g, ' ')
    .replace(/\b\w/g, l => l.toUpperCase())
}

const formatCellValue = (value) => {
  if (value === null || value === undefined) return '-'
  if (typeof value === 'string' && value.length > 100) {
    return value.substring(0, 100) + '...'
  }
  return value
}

const filteredRows = computed(() => {
  let filtered = awardRows.value

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(row => {
      return Object.values(row).some(val => 
        val && val.toString().toLowerCase().includes(query)
      )
    })
  }

  // Apply sorting
  if (sortColumn.value) {
    filtered = [...filtered].sort((a, b) => {
      const aVal = a[sortColumn.value]
      const bVal = b[sortColumn.value]
      
      if (aVal === bVal) return 0
      
      const comparison = aVal > bVal ? 1 : -1
      return sortDirection.value === 'asc' ? comparison : -comparison
    })
  }

  // Apply pagination
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return filtered.slice(start, end)
})

const totalPages = computed(() => {
  const total = searchQuery.value 
    ? awardRows.value.filter(row => 
        Object.values(row).some(val => 
          val && val.toString().toLowerCase().includes(searchQuery.value.toLowerCase())
        )
      ).length
    : awardRows.value.length
  
  return Math.ceil(total / itemsPerPage)
})

const fetchAllAwardsData = async () => {
  loading.value = true
  currentPage.value = 1
  awardRows.value = []
  columns.value = []

  try {
    // Fetch all awards at once
    const promises = Object.values(tableMapping).map(table =>
      axios.get(`${API_BASE_URL}/api/awards/${table}/?limit=20000`)
    )

    const results = await Promise.all(promises)

    // Combine rows from all awards
    const merged = results.flatMap(r => r.data.rows)

    awardRows.value = merged

    // Compute a union of all columns
    const colSet = new Set()
    merged.forEach(row => Object.keys(row).forEach(c => colSet.add(c)))
    columns.value = [...colSet]

  } catch (e) {
    console.error("Failed to load all awards:", e)
  }

  loading.value = false
}

const sortBy = (column) => {
  if (sortColumn.value === column) {
    sortDirection.value = sortDirection.value === 'asc' ? 'desc' : 'asc'
  } else {
    sortColumn.value = column
    sortDirection.value = 'asc'
  }
}

const fetchAwards = async () => {
  try {
    const { data } = await axios.get(`${API_BASE_URL}/api/awards/`)
    awards.value = data
    if (data.length > 0) activeAward.value = "all"
  } catch (error) {
    console.error('Failed to fetch awards:', error)
  }
}

const fetchAwardData = async (awardId) => {
  if (!awardId) return
  loading.value = true
  currentPage.value = 1
  
  try {
    const tableName = tableMapping[awardId]
    if (!tableName) return
    
    const { data } = await axios.get(`${API_BASE_URL}/api/awards/${tableName}/?limit=20000`)
    awardRows.value = data.rows
    columns.value = data.rows.length > 0 ? Object.keys(data.rows[0]) : []
  } catch (error) {
    console.error('Failed to fetch award data:', error)
  } finally {
    loading.value = false
  }
}

watch(activeAward, async (newAwardId) => {
  if (newAwardId === 'all') {
    await fetchAllAwardsData()
  } else {
    await fetchAwardData(newAwardId)
  }
})


watch(searchQuery, () => {
  currentPage.value = 1
})

onMounted(async () => {
  await fetchAwards()
})
</script>

<style scoped>
.awards-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

.awards-header {
  margin-bottom: 2rem;
}

.awards-header h1 {
  color: var(--color-heading);
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

.subtitle {
  color: var(--color-text-muted);
  margin-bottom: 1.5rem;
}

.filters-section {
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
  flex-wrap: wrap;
  flex: 1;
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

.award-icon {
  font-size: 1.2rem;
}

.view-controls {
  display: flex;
  gap: 0.5rem;
}

.view-btn {
  width: 40px;
  height: 40px;
  border: 2px solid var(--color-border);
  background: transparent;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.view-btn:hover {
  border-color: var(--color-border-hover);
}

.view-btn.active {
  background: var(--color-button-bg);
  color: white;
  border-color: var(--color-button-bg);
}

.view-btn .icon {
  font-size: 1.2rem;
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

.cards-grid {
  display: grid;
  gap: 1.5rem;
  grid-template-columns: repeat(3, 1fr) !important;
  max-width: 100%;
}

.table-wrapper {
  width: 100%;
  position: relative;
}

.table-container {
  overflow-x: auto;
  overflow-y: visible;
  background: var(--color-background-soft);
  border-radius: 12px;
  border: 1px solid var(--color-border);
  max-width: 100%;
  
  /* Custom scrollbar */
  scrollbar-width: thin;
  scrollbar-color: var(--color-border-hover) var(--color-background-mute);
}

.table-container::-webkit-scrollbar {
  height: 8px;
}

.table-container::-webkit-scrollbar-track {
  background: var(--color-background-mute);
  border-radius: 4px;
}

.table-container::-webkit-scrollbar-thumb {
  background: var(--color-border-hover);
  border-radius: 4px;
}

.table-container::-webkit-scrollbar-thumb:hover {
  background: var(--color-accent);
}

.award-table {
  width: 100%;
  border-collapse: collapse;
  min-width: 800px;
}

.award-table th {
  background: var(--color-background-mute);
  padding: 1rem;
  text-align: left;
  font-weight: 600;
  color: var(--color-heading);
  border-bottom: 2px solid var(--color-border);
  cursor: pointer;
  user-select: none;
  position: sticky;
  top: 0;
  z-index: 10;
  white-space: nowrap;
  min-width: 120px;
}

.award-table th:first-child {
  position: sticky;
  left: 0;
  z-index: 20;
  box-shadow: 2px 0 4px rgba(0, 0, 0, 0.05);
}

.award-table th:hover {
  background: rgba(217, 202, 179, 0.3);
}

.sort-indicator {
  margin-left: 0.5rem;
  color: var(--color-accent);
}

.award-table td {
  padding: 1rem;
  border-bottom: 1px solid var(--color-border);
  color: var(--color-text);
  max-width: 300px;
  overflow: hidden;
  text-overflow: ellipsis;
}

.award-table td:first-child {
  position: sticky;
  left: 0;
  background: var(--color-background-soft);
  z-index: 5;
  box-shadow: 2px 0 4px rgba(0, 0, 0, 0.05);
  font-weight: 600;
}

.award-table tr:hover td {
  background: var(--color-background-mute);
}

.award-table tr:hover td:first-child {
  background: var(--color-background-mute);
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

.empty-hint {
  font-size: 0.9rem;
  margin-top: 0.5rem;
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

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  margin-top: 2rem;
  padding: 1rem;
}

.page-btn {
  padding: 0.5rem 1rem;
  border: 2px solid var(--color-border);
  background: var(--color-background-soft);
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  color: var(--color-text);
  transition: all 0.3s ease;
}

.page-btn:hover:not(:disabled) {
  border-color: var(--color-border-hover);
  background: var(--color-button-bg);
  color: white;
}

.page-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.page-info {
  color: var(--color-text-muted);
  font-weight: 600;
}

@media (max-width: 768px) {
  .filters-section {
    flex-direction: column;
    align-items: stretch;
  }

  .cards-grid {
    grid-template-columns: 1fr;
  }

  .award-table {
    display: block;
  }

  .award-table thead {
    display: none;
  }

  .award-table tr {
    display: block;
    margin-bottom: 1rem;
    border: 1px solid var(--color-border);
    border-radius: 8px;
    padding: 0.5rem;
  }

  .award-table td {
    display: block;
    text-align: right;
    padding: 0.5rem;
    border: none;
  }

  .award-table td::before {
    content: attr(data-label);
    float: left;
    font-weight: 600;
    color: var(--color-heading);
  }
}

@media (prefers-color-scheme: dark) {
  .award-table th {
    background: rgba(59, 130, 246, 0.1);
  }
}
</style>