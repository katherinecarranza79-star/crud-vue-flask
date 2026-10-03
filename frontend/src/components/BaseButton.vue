<template>
  <button :type="type" :class="['button', `button--${variant}`]" :disabled="disabled">
    <slot />
  </button>
</template>

<script setup>
defineProps({
  type: { type: String, default: 'button' },
  variant: { type: String, default: 'primary' },
  disabled: { type: Boolean, default: false },
})
</script>
