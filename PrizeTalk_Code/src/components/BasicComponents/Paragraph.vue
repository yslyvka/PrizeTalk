<script setup lang="ts">
import { computed } from 'vue'

type Tone = 'normal' | 'muted' | 'lead'
type Align = 'left' | 'center' | 'right'

const props = withDefaults(defineProps<{
  tone?: Tone
  align?: Align
}>(), {
  tone: 'normal',
  align: 'left',
})

const toneClasses: Record<Tone, string> = {
  normal: 'paragraph paragraph--normal',
  muted: 'paragraph paragraph--muted',
  lead: 'paragraph paragraph--lead text-lg',
}

const cls = computed(() => [
  'font-sans leading-relaxed',
  toneClasses[props.tone],
  props.align === 'center' ? 'text-center' : props.align === 'right' ? 'text-right' : 'text-left',
].join(' '))
</script>

<template>
  <p :class="cls">
    <slot />
  </p>
  
</template>