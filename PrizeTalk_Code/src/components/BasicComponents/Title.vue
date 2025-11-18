<template>
  <component :is="`h${level}`" :class="`font-bold ${class}`" :style="`font-size: ${size}`">
    <slot></slot>
  </component>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  level?: number
  class?: string
}

const props = withDefaults(defineProps<Props>(), {
  level: 1,
  class: ''
})

const size = computed(() => {
  switch (props.level) {
    case 1: return '2rem'
    case 2: return '1.5rem'
    case 3: return '1.25rem'
    default: return '1rem'
  }
})
</script>