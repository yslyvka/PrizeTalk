<script setup lang="ts">
import { computed } from 'vue'

type Variant = 'primary' | 'outline' | 'ghost'
type Size = 'sm' | 'md' | 'lg'
type ButtonType = 'button' | 'submit' | 'reset'

const props = withDefaults(defineProps<{
  variant?: Variant
  size?: Size
  block?: boolean
  disabled?: boolean
  type?: ButtonType
}>(), {
  variant: 'primary',
  size: 'md',
  block: false,
  disabled: false,
  type: 'button',
})

const baseClasses =
  'inline-flex items-center justify-center font-medium rounded-xl transition-all duration-200 select-none ' +
  'focus:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 active:translate-y-[1px] disabled:opacity-50 disabled:cursor-not-allowed'

const sizeClasses: Record<Size, string> = {
  sm: 'px-3 py-1.5 text-sm',
  md: 'px-4 py-2 text-base',
  lg: 'px-5 py-3 text-lg',
}

const variantClasses: Record<Variant, string> = {
  primary: 'bg-[var(--color-button-bg)] text-[var(--color-button-text)] border border-[var(--color-border)] hover:bg-[var(--color-button-hover-bg)]',
  outline: 'bg-transparent text-[var(--color-text)] border border-[var(--color-border)] hover:bg-[var(--color-background-soft)]',
  ghost: 'bg-transparent text-[var(--color-text)] border-transparent hover:bg-[var(--color-background-soft)]',
}

const rootClasses = computed(() =>
  [
    baseClasses,
    sizeClasses[props.size],
    variantClasses[props.variant],
    props.block ? 'w-full' : '',
  ].join(' ')
)
</script>

<template>
  <button
    :type="type"
    :disabled="disabled"
    :class="rootClasses"
  >
    <span class="inline-flex items-center gap-2">
      <slot>Click Me</slot>
    </span>
  </button>
</template>