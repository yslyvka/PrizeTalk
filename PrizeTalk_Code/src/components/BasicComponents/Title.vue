<script setup lang="ts">
import { computed } from 'vue'

type Level = 'h1' | 'h2' | 'h3'
type Align = 'left' | 'center' | 'right'

const props = withDefaults(defineProps<{
  level?: Level
  align?: Align
}>(), {
  level: 'h1',
  align: 'left',
})

const sizes: Record<Level, string> = {
  h1: 'text-4xl sm:text-5xl font-extrabold',
  h2: 'text-3xl sm:text-4xl font-bold',
  h3: 'text-2xl sm:text-3xl font-semibold',
}

const cls = computed(() => [
  'title font-sans tracking-tight',
  sizes[props.level],
  props.align === 'center' ? 'text-center' : props.align === 'right' ? 'text-right' : 'text-left',
].join(' '))
</script>

<template>
  <component :is="props.level" :class="cls">
    <slot />
  </component>
</template>