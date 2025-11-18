<template>
  <p :class="`text-base ${class}`" :style="align === 'center' ? 'text-align: center' : align === 'right' ? 'text-align: right' : 'text-align: left'">
    <slot></slot>
  </p>
</template>

<script setup lang="ts">
interface Props {
  align?: 'left' | 'center' | 'right'
  class?: string
}

withDefaults(defineProps<Props>(), {
  align: 'left',
  class: ''
})
</script>