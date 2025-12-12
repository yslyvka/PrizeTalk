<template>
  <div class="award-analytics">
    <div class="controls">
      <select v-model="selectedAward" @change="fetchData" class="award-select">
        <option value="oscars">⏯ Oscars</option>
        <option value="grammy">♫ Grammy Awards</option>
        <option value="golden_globes">𖧋 Golden Globes</option>
        <option value="nobel_prizes">𐃯 Nobel Prizes</option>
        <option value="booker_prize">✎ᝰ. Booker Prize</option>
      </select>
    
    </div>

    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>Loading analytics...</p>
    </div>

    <div v-else-if="error" class="error-state">
      <p>{{ error }}</p>
      <button @click="fetchData" class="retry-btn">Try Again</button>
    </div>

    <div v-else class="analytics-grid">
      <!-- Top Winners Leaderboard -->
      <div class="card">
        <h2>𐃯 Top Winners</h2>
        <div v-if="winners.length === 0" class="empty">No data available</div>
        <div v-else class="leaderboard">
          <div 
            v-for="(winner, index) in winners" 
            :key="index"
            class="leaderboard-item"
          >
            <div class="rank" :class="'rank-' + (index + 1)">{{ index + 1 }}</div>
            <div class="winner-info">
              <div class="winner-name">{{ winner.winner_name || winner.Name || winner.Nominee || winner.title || winner.WINNER || 'Unknown' }}</div>
              <div class="winner-details">
                {{ winner.win_count }} {{ winner.win_count === 1 ? 'win' : 'wins' }}
                <span v-if="winner.first_win && winner.latest_win">
                  • {{ winner.first_win }}<span v-if="winner.first_win !== winner.latest_win">-{{ winner.latest_win }}</span>
                </span>
              </div>
            </div>
            <div class="win-badge">
              <span class="win-count">{{ winner.win_count }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Trends Chart -->
      <div class="card">
        <h2>↗ Award Trends Over Time</h2>
        <div v-if="trends.length === 0" class="empty">No trend data available</div>
        <div v-else class="chart-wrapper">
          <div class="chart-container">
            <svg :width="chartWidth" :height="300" class="line-chart">
              <!-- Grid lines -->
              <line 
                v-for="i in 5" 
                :key="'grid-' + i"
                x1="60" 
                :y1="50 + (i * 40)" 
                :x2="chartWidth - 20" 
                :y2="50 + (i * 40)"
                stroke="#e0e0e0" 
                stroke-width="1"
                stroke-dasharray="4"
              />
              
              <!-- Y-axis -->
              <line x1="60" y1="30" x2="60" y2="270" stroke="#666" stroke-width="2"/>
              <!-- X-axis -->
              <line x1="60" y1="270" :x2="chartWidth - 20" y2="270" stroke="#666" stroke-width="2"/>
              
              <!-- Y-axis labels -->
              <text 
                v-for="(label, i) in yAxisLabels" 
                :key="'y-' + i"
                x="50" 
                :y="270 - (i * 60) + 5"
                text-anchor="end"
                font-size="12"
                fill="#666"
              >
                {{ label }}
              </text>
              
              <!-- Data line -->
              <polyline
                v-if="trendPoints"
                :points="trendPoints"
                fill="none"
                stroke="#8884d8"
                stroke-width="3"
              />
              
              <!-- Data points with hover -->
              <g v-for="(point, i) in trendPointsArray" :key="'point-' + i">
                <circle
                  :cx="point.x"
                  :cy="point.y"
                  r="6"
                  fill="#8884d8"
                  class="chart-point"
                >
                  <title>{{ trends[i].year }}: {{ trends[i].awards_count }} awards</title>
                </circle>
              </g>
              
              <!-- X-axis labels (years) -->
              <text 
                v-for="(trend, i) in trendsToDisplay" 
                :key="'label-' + i"
                :x="80 + (i * xStep)"
                y="290"
                text-anchor="middle"
                font-size="11"
                fill="#666"
              >
                {{ trend.year }}
              </text>
            </svg>
          </div>
        </div>
      </div>

      <!-- Category Distribution -->
      <div class="card full-width">
        <h2> 𖣯Category Distribution</h2>
        <div v-if="categories.length === 0" class="empty">No category data available</div>
        <div v-else class="category-grid">
          <div 
            v-for="(cat, index) in categories.slice(0, 10)" 
            :key="index"
            class="category-bar"
          >
            <div class="category-name" :title="cat.category">
              {{ truncateText(cat.category, 30) }}
            </div>
            <div class="bar-container">
              <div 
                class="bar-fill" 
                :style="{ 
                  width: (cat.count / maxCategoryCount * 100) + '%',
                  background: getBarColor(index)
                }"
              >
                <span v-if="cat.count / maxCategoryCount > 0.2" class="bar-label">
                  {{ cat.count }}
                </span>
              </div>
            </div>
            <div class="category-count">{{ cat.count }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

const API_BASE_URL = (
  import.meta.env.VITE_API_BASE_URL ||
  import.meta.env.VITE_API_PROXY_TARGET ||
  ''
).replace(/\/+$/, '')

const selectedAward = ref('oscars')
const winners = ref([])
const trends = ref([])
const categories = ref([])
const loading = ref(true)
const error = ref(null)
const chartWidth = ref(700)

const maxCategoryCount = computed(() => {
  return Math.max(...categories.value.map(c => c.count), 1)
})

const trendsToDisplay = computed(() => {
  // Show max 15 data points for readability
  const maxPoints = 15
  if (trends.value.length <= maxPoints) return trends.value
  
  const step = Math.ceil(trends.value.length / maxPoints)
  return trends.value.filter((_, i) => i % step === 0).slice(0, maxPoints)
})

const xStep = computed(() => {
  const count = trendsToDisplay.value.length
  return count > 1 ? (chartWidth.value - 100) / (count - 1) : 0
})

const yAxisLabels = computed(() => {
  if (trendsToDisplay.value.length === 0) return []
  const maxCount = Math.max(...trendsToDisplay.value.map(t => t.awards_count))
  const step = Math.ceil(maxCount / 4)
  return [0, step, step * 2, step * 3, step * 4]
})

const trendPointsArray = computed(() => {
  if (trendsToDisplay.value.length === 0) return []
  
  const maxCount = Math.max(...trendsToDisplay.value.map(t => t.awards_count))
  const points = []
  
  trendsToDisplay.value.forEach((trend, i) => {
    const x = 80 + (i * xStep.value)
    const y = 270 - ((trend.awards_count / maxCount) * 240)
    points.push({ x, y })
  })
  
  return points
})

const trendPoints = computed(() => {
  return trendPointsArray.value.map(p => `${p.x},${p.y}`).join(' ')
})

const getBarColor = (index) => {
  const colors = [
    'linear-gradient(90deg, #667eea 0%, #764ba2 100%)',
    'linear-gradient(90deg, #f093fb 0%, #f5576c 100%)',
    'linear-gradient(90deg, #4facfe 0%, #00f2fe 100%)',
    'linear-gradient(90deg, #43e97b 0%, #38f9d7 100%)',
    'linear-gradient(90deg, #fa709a 0%, #fee140 100%)',
  ]
  return colors[index % colors.length]
}

const truncateText = (text, maxLength) => {
  if (!text) return ''
  return text.length > maxLength ? text.substring(0, maxLength) + '...' : text
}

const fetchData = async () => {
  loading.value = true
  error.value = null
  
  try {
    console.log('Fetching award analytics for:', selectedAward.value)
    
    const [winnersRes, trendsRes] = await Promise.all([
      axios.get(`${API_BASE_URL}/api/analytics/award-winners/`, {
        params: { award_type: selectedAward.value, limit: 10 }
      }),
      axios.get(`${API_BASE_URL}/api/analytics/award-trends/`, {
        params: { award_type: selectedAward.value }
      })
    ])
    
    winners.value = winnersRes.data || []
    trends.value = trendsRes.data.trends || []
    categories.value = trendsRes.data.categories || []
    
    console.log('Winners:', winners.value.length)
    console.log('Trends:', trends.value.length)
    console.log('Categories:', categories.value.length)
  } catch (err) {
    console.error('Error fetching award analytics:', err)
    error.value = err.response?.data?.error || 'Failed to load data. Please try again.'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchData()
  
  // Set chart width based on container
  const updateChartWidth = () => {
    chartWidth.value = window.innerWidth > 900 ? 700 : Math.max(window.innerWidth - 100, 400)
  }
  updateChartWidth()
  window.addEventListener('resize', updateChartWidth)
})
</script>

<style scoped>
.award-analytics {
  margin-top: 2rem;
}

.controls {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
}

.award-select {
  flex: 1;
  padding: 0.75rem 1rem;
  border: 2px solid var(--color-border);
  border-radius: 8px;
  font-size: 1rem;
  background: var(--color-background-soft);
  color: var(--color-text);
  cursor: pointer;
  transition: all 0.3s ease;
}

.award-select:hover {
  border-color: var(--color-border-hover);
}

.award-select:focus {
  outline: none;
  border-color: var(--color-button-bg);
}

.refresh-btn, .retry-btn {
  padding: 0.75rem 1.5rem;
  background: var(--color-button-bg);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s ease;
}

.refresh-btn:hover, .retry-btn:hover {
  background: var(--color-button-hover-bg);
  transform: translateY(-1px);
}

.analytics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(1000px, 1fr));
  gap: 1.5rem;
}

.card {
  background: var(--color-background-soft);
  border: 2px solid var(--color-border);
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

.card.full-width {
  grid-column: 1 / -1;
}

.card h2 {
  margin-bottom: 1.5rem;
  color: var(--color-heading);
  font-size: 1.25rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.leaderboard {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.leaderboard-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: var(--color-background);
  border-radius: 10px;
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.leaderboard-item:hover {
  transform: translateX(4px);
  border-color: var(--color-button-bg);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.rank {
  width: 45px;
  height: 45px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-button-bg);
  color: white;
  border-radius: 50%;
  font-weight: bold;
  font-size: 1.2rem;
  flex-shrink: 0;
}

.rank-1 {
  background: linear-gradient(135deg, #FFD700, #FFA500);
  box-shadow: 0 4px 12px rgba(255, 215, 0, 0.4);
}

.rank-2 {
  background: linear-gradient(135deg, #C0C0C0, #808080);
}

.rank-3 {
  background: linear-gradient(135deg, #CD7F32, #8B4513);
}

.winner-info {
  flex: 1;
  min-width: 0;
}

.winner-name {
  font-weight: 600;
  color: var(--color-heading);
  margin-bottom: 0.25rem;
  font-size: 1.05rem;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.winner-details {
  font-size: 0.9rem;
  color: var(--color-text-muted);
}

.win-badge {
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 50px;
}

.win-count {
  font-size: 1.8rem;
  font-weight: bold;
  color: var(--color-button-bg);
}

.chart-wrapper {
  overflow-x: auto;
  overflow-y: hidden;
}

.chart-container {
  min-width: 400px;
}

.line-chart {
  display: block;
  margin: 0 auto;
}

.chart-point {
  cursor: pointer;
  transition: r 0.2s;
}

.chart-point:hover {
  r: 8;
}

.category-grid {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.category-bar {
  display: grid;
  grid-template-columns: minmax(150px, 250px) 1fr 70px;
  align-items: center;
  gap: 1rem;
  padding: 0.5rem 0;
}

.category-name {
  font-weight: 600;
  color: var(--color-heading);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-size: 0.95rem;
}

.bar-container {
  height: 36px;
  background: var(--color-background);
  border-radius: 8px;
  overflow: hidden;
  position: relative;
  border: 1px solid var(--color-border);
}

.bar-fill {
  height: 100%;
  transition: width 0.8s ease;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  padding-right: 8px;
  position: relative;
}

.bar-label {
  color: white;
  font-weight: bold;
  font-size: 0.85rem;
  text-shadow: 0 1px 2px rgba(0,0,0,0.3);
}

.category-count {
  text-align: right;
  font-weight: bold;
  color: var(--color-button-bg);
  font-size: 1.1rem;
}

.loading-state, .empty, .error-state {
  text-align: center;
  padding: 3rem 2rem;
  color: var(--color-text-muted);
}

.error-state {
  color: #e53e3e;
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
  .analytics-grid {
    grid-template-columns: 1fr;
  }
  
  .category-bar {
    grid-template-columns: minmax(100px, 150px) 1fr 50px;
    gap: 0.5rem;
  }
  
  .category-name {
    font-size: 0.85rem;
  }
}
</style>