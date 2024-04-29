<template>
    <div class="flex items-center gap-x-4 py-6 pr-2" v-for="message in mensages" :type="message.type">
      <img class="h-10 w-10 rounded-full bg-gray-800" src="https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80" alt="" />
      <div class="flex-1">
        <div class="flex items-center justify-between">
          <h1 class="text-lg font-semibold leading-6 text-white"></h1>
          <time class="text-xs font-semibold leading-6 text-gray-400">{{message.date }}</time>
        </div>
        <p v-if="message.type === 'request' " class="mt-1 text-sm leading-6 text-gray-600"><dots /></p>
        <p v-else class="mt-1 text-sm leading-6 text-gray-600"> {{message.message}} </p>
        <hr class="mt-1">
      </div>
    </div>    
</template>

<script setup lang="ts">
import {IMessage} from '@/models/Message'
import dots from './utils/dots.vue';


defineProps({
    mensages:{
      type: Array<IMessage>,
      default:[], 
    }
})



</script>