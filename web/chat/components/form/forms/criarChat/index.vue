<template>
    <div class="text-red-500">{{ errorMessage }}</div>

    <div class="grid grid-cols-1 w-full mt-2">
        <label :class="['block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300']" for="pergunta">
            Pergunta
        </label>
        <div class="col-span-1">
            <textarea 
                v-model="form.pergunta"
                rows="4" name="pergunta" id="pergunta"
                class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-blue-600 sm:text-sm sm:leading-6"
                placeholder="O que deseja saber hoje?" />
        </div>
    </div>
</template>

<script setup lang="ts">
import {useNotificationStore} from '~/stores/notification'
import {defaultStore} from '@/stores/default'
import {authStore} from '@/stores/auth'
import { type ChatSession } from '@/models/Chatsession/List'
const notificationStore = useNotificationStore()
const defaultStorePinia = defaultStore()
const errorMessage = ref("");
const auth = authStore()
const emit = defineEmits(['close'])
const props = defineProps({
    clearForm: Boolean,
    submitForm: Boolean,
    chatList: Array
})

const setLoading = (loading:boolean) => {
    defaultStorePinia.setLoading(loading)
  }

const form = ref({
    pergunta: ''
})

watch(() => props.clearForm, () => {
    alert('clearForm')
})
watch(() => props.submitForm, async() => {
    try {
        setLoading(true)
        try{
            const retorno = await $fetch('/api/chatsession/create', {
            method: 'POST',
            timeout: 300000,
            headers: {
                "Authorization" :"bearer "+auth.token
            },
            body: {
                "pergunta": form.value.pergunta
                }
            }) as ChatSession
        notificationStore.successNotification(null,'Chat criado com sucesso!')
        emit('close')
        props.chatList.unshift(retorno)
        await navigateTo(`/chats/${retorno.session_id}`)
        }catch(error){
            clearError({ redirect: '/login?message=Token expirado' })
        }
    } catch (error) {
        notificationStore.errorNotification(null,'Erro ao criar novo chat')
    }finally{
        setLoading(false)
        form.value.pergunta = ''
    }

})

</script>