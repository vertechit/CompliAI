<template>
    <button type="button" 
    @click="emit('action')"
    class="rounded-md
       px-3.5 py-2.5 text-sm font-semibold text-white shadow-sm
       focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2"
        :class="[`${custom}`]"
     >
   
        {{ label }}
    </button>
</template>

<script setup lang="ts">
const emit = defineEmits(['action'])
defineProps({
    label: {
        type: String,
    },
    custom: {
        type: String
    },
})
</script>

<style scoped>

</style>