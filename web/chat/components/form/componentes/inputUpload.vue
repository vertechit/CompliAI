<template>
    <label :class="['block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300']" for="file_input">Selecione seu
        arquivo
    </label>
    <div
        class="flex justify-between w-full items-center  ring-0 file:text-gray-900 focus:outlie-none  border rounded-lg cursor-pointer file:cursor-pointer
        border-gray-300 py-[0.8px]">
        <input
            type="file"
            class="file:py-2 file:px-3 file:border-none file focus:outline-0 w-full" 
            name="file" 
            id="fileUpload"
            @change="captureFile($event)"
            >
        <button type="button"
            @click="clearFiles()"
            :class="[`focus:outline-0 mx-3 px-2 hover:bg-slate-200 h-6 rounded-md ${!fileBuffer.length ? 'hidden' : 'block'}`]"
            >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24"
                stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
            </svg>
        </button>
    </div>
</template>

<script setup lang="ts">

const emit = defineEmits(['update:modelValue'])
const fileBuffer = ref([])
defineProps({
    modelValue: [String,Object,Array]
})

const captureFile = (event: any) => {
    fileBuffer.value = event.target.files
    emit('update:modelValue', event.target.files)
}
const clearFiles = () => {
    let document = window.document.querySelector('#fileUpload') as HTMLInputElement
    document.value = '' 
}

</script>

<style scoped></style>