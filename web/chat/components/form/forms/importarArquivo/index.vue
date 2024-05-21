<template>
    <div class="grid grid-cols-1">
        <div class="col-span-1">
            <FormComponentesInputUpload v-model="form.files"/>
        </div>
    </div>
    <div class="grid grid-cols-1 w-full mt-2">
        <label :class="['block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300']" for="file_input">
            Descrição
        </label>
        <div class="col-span-1">
            <textarea 
                v-model="form.description"
                rows="4" name="comment" id="comment"
                class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-blue-600 sm:text-sm sm:leading-6"
                placeholder="Descrição do arquivo" />
        </div>
    </div>
</template>

<script setup lang="ts">
import FormComponentesInputUpload from '@/components/form/componentes/inputUpload.vue'
import {useNotificationStore} from '@/stores/notification'
import {defaultStore} from '@/stores/default'
const notificationStore = useNotificationStore()
const defaultStorePinia = defaultStore()
const emit = defineEmits(['close'])
const props = defineProps({
    clearForm: Boolean,
    submitForm: Boolean
})

const setLoading = (loading:boolean) => {
    defaultStorePinia.setLoading(loading)
  }

const form = ref({
    files: [] as any[],
    description: ''
})
watch(() => props.clearForm, () => {
    alert('clearForm')
})
watch(() => props.submitForm, async() => {
    try {
        setLoading(true)
        const formData = new FormData()
        formData.append('file', form.value.files[0]);
        formData.append('description', form.value.description);
        await $fetch('/api/documents/create', {
            method: 'POST',
            body: formData
        })
        notificationStore.successNotification(null,'Arquivo enviado com sucesso')
        emit('close')
    } catch (error) {
        notificationStore.errorNotification(null,'Erro ao enviar arquivo')
    }finally{
        setLoading(false)
        form.value.files = []
        form.value.description = ''
    }

})

</script>

<style scoped></style>