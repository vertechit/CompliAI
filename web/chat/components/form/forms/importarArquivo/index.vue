<template>
    <div class="grid grid-cols-1">
        <div class="col-span-1">
            <FormComponentesInputUpload />
        </div>
    </div>
    <div class="grid grid-cols-1 w-full mt-2">
        <label :class="['block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300']" for="file_input">
            Descrição
        </label>
        <div class="col-span-1">
            <textarea rows="4" name="comment" id="comment"
                class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-blue-600 sm:text-sm sm:leading-6"
                placeholder="Descrição do arquivo" />
        </div>
    </div>
</template>

<script setup lang="ts">
const props = defineProps({
    clearForm: Boolean,
    submitForm: Boolean
})

watch(() => props.clearForm, () => {
    alert('clearForm')
})
watch(() => props.submitForm, () => {
    alert('submitForm')
})

</script>

<style scoped></style>