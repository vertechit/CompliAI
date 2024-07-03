<template>
    <div class="text-red-500">{{ errorMessage }}</div>
    <div v-if="!urlForm" class="grid grid-cols-1">
        <div class="col-span-1">
            <FormComponentesInputUpload v-model="form.files"/>
        </div>
    </div>

    <div v-if="urlForm" class="grid grid-cols-1 w-full mt-2">
        <label :class="['block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300']" for="file_titulol">
            Título
        </label>
        <div class="col-span-1">
            <input
                v-model="form.titulo"
                rows="4" name="titulo" id="titulo"
                class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-blue-600 sm:text-sm sm:leading-6"
                placeholder="Título do documento" />
        </div>
    </div>

    <div v-if="urlForm" class="grid grid-cols-1 w-full mt-2">
        <label :class="['block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300']" for="file_url">
            URL
        </label>
        <div class="col-span-1">
            <input
                v-model="form.url"
                type="url"
                rows="4" name="url" id="url"
                class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-blue-600 sm:text-sm sm:leading-6"
                placeholder="URL do site" />
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
import {useNotificationStore} from '~/stores/notification'
import {defaultStore} from '@/stores/default'
import {authStore} from '@/stores/auth'
const notificationStore = useNotificationStore()
const defaultStorePinia = defaultStore()
const errorMessage = ref("");
const auth = authStore()
const emit = defineEmits(['close'])
const props = defineProps({
    clearForm: Boolean,
    submitForm: Boolean,
    urlForm: Boolean
})

const setLoading = (loading:boolean) => {
    defaultStorePinia.setLoading(loading)
  }

const form = ref({
    files: [] as any[],
    description: '',
    url: '',
    titulo: ''
})

function isUrlValid(userInput:string) {
    var res = userInput.match(/(http(s)?:\/\/.)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)/g);
    if(res == null)
        return false;
    else
        return true;
}

watch(() => props.clearForm, () => {
    alert('clearForm')
})
watch(() => props.submitForm, async() => {
    try {
        setLoading(true)
        if(props.urlForm){
            if(!form.value.titulo){
                errorMessage.value = 'Título não pode ser nulo!'
                return true
            }else if(!isUrlValid(form.value.url)){
                errorMessage.value = 'Não é uma URL Válida!'
                return true
            }else{
                await $fetch('/api/documents/createUrl', {
                    method: 'POST',
                    headers: {
                        "Authorization" :"bearer "+auth.token
                    },
                    body: {
                        "titulo": form.value.titulo,
                        "description": form.value.description,
                        "url": form.value.url
                        }
                })
            }
        }else{
            const formData = new FormData()
            formData.append('file', form.value.files[0]);
            formData.append('description', form.value.description);
            await $fetch('/api/documents/create', {
                method: 'POST',
                headers: {
                    "Authorization" :"bearer "+auth.token
                },
                body: formData
            })
        }
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