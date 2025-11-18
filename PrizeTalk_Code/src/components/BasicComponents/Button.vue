<template>
  <button
    :class="buttonClasses"
    :type="type"
    :disabled="disabled"
    @click="$emit('click')"
  >
    <slot></slot>
  </button>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  variant?: 'primary' | 'secondary' | 'outline'
  size?: 'sm' | 'md' | 'lg'
  block?: boolean
  disabled?: boolean
  type?: 'button' | 'submit' | 'reset'
  class?: string
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'primary',
  size: 'md',
  block: false,
  disabled: false,
  type: 'button',
  class: ''
})

const buttonClasses = computed(() => {
  let classes = 'inline-flex items-center justify-center font-medium rounded transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed'

  // Size
  switch (props.size) {
    case 'sm':
      classes += ' px-3 py-1.5 text-sm'
      break
    case 'lg':
      classes += ' px-6 py-3 text-lg'
      break
    default:
      classes += ' px-4 py-2 text-base'
  }

  // Variant
  switch (props.variant) {
    case 'secondary':
      classes += ' bg-gray-200 text-gray-900 hover:bg-gray-300 focus:ring-gray-500'
      break
    case 'outline':
      classes += ' border border-gray-300 bg-white text-gray-700 hover:bg-gray-50 focus:ring-blue-500'
      break
    default: // primary
      classes += ' bg-blue-600 text-white hover:bg-blue-700 focus:ring-blue-500'
  }

  // Block
  if (props.block) {
    classes += ' w-full'
  }

  // Custom class
  if (props.class) {
    classes += ` ${props.class}`
  }

  return classes
})

defineEmits<{
  click: []
}>()
</script>