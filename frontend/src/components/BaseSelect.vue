<template>
  <label class="field">
    <span>{{ label }}</span>
    <select :value="modelValue" :aria-invalid="!!error" @change="onChange">
      <option disabled value="">{{ placeholder }}</option>
      <option v-for="option in options" :key="option.value" :value="option.value">
        {{ option.label }}
      </option>
    </select>
    <small v-if="error" class="field__error">{{ error }}</small>
  </label>
</template>

<script setup>
const props = defineProps({
  label: { type: String, required: true },
  modelValue: { type: [String, Number], default: '' },
  options: { type: Array, required: true },
  placeholder: { type: String, default: 'Seleccione una opción' },
  error: { type: String, default: '' },
})
const emit = defineEmits(['update:modelValue'])

function onChange(event) {
  // Conserva el tipo original del valor (número o texto).
  const found = props.options.find((o) => String(o.value) === event.target.value)
  emit('update:modelValue', found ? found.value : event.target.value)
}
</script>
