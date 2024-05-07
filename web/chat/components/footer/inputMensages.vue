
<template>
    <div class="flex items-start space-x-4">
      <div class="flex-shrink-0">
        <img class="inline-block h-10 w-10 rounded-full" src="https://images.unsplash.com/photo-1550525811-e5869dd03032?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80" alt="" />
      </div>
      <div class="min-w-0 flex-1">
        <form action="#" @submit.prevent>
          <div class="border-b border-gray-200 focus-within:border-blue-600">
            <label for="comment" class="sr-only">Escreva sua dúvida</label>
            <textarea :disabled="loading" v-model="message" @keypress.enter="onSubmit" rows="3" name="comment" id="comment" 
             class="block w-full resize-none border-0 border-b border-transparent p-0 pb-2 text-gray-900 placeholder:text-gray-400 focus:border-blue-600 focus:ring-0 sm:text-sm sm:leading-6" placeholder="Envie sua Dúvida"
            :class="{'cursor-not-allowed bg-gray-100':loading}" 
            
            />
          </div>
          <div class="flex justify-between pt-2">
            <div class="flex items-center space-x-5">
              
              <div class="flow-root">
              </div>
            </div>
            <div class="flex-shrink-0">
              <button :disable="loading" type="submit" @keypress.enter="onSubmit"  class="inline-flex items-center rounded-md bg-blue-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-blue-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-600"
              :class="{'cursor-not-allowed bg-blue-800':loading}" 
              >Enviar</button>
            </div>
          </div>
        </form>
      </div>
    </div>
  </template>
  
  <script setup lang="ts">
  import {defaultStore} from '@/stores/default'
  const defaultStorePinia = defaultStore()
  let message = ref('')
  const emit = defineEmits(['submit'])
  const loading = computed(()=>defaultStorePinia.loading)
  function onSubmit() {
    emit('submit', message.value)
    message.value = ''
  }
  
  </script>