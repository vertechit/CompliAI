<template>

    <button 
    @click="emit('action')"
    type="button" class="inline-flex items-center gap-x-2 rounded-md bg-blue-600 px-3.5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-blue-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-600">
      {{ label}}
      <slot name="icon"></slot>
    </button>
  </template>
  
  <script setup lang="ts">
  const emit = defineEmits(['action'])
  defineProps<{
    label: string
  }>()
  </script>