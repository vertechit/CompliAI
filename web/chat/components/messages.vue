<template>
  <div class="flex items-center gap-x-4 py-2 pr-2" v-for="(message, index) in messages" :key="index" :type="message.type">
    <div class="flex-1">
      <div class="flex items-center justify-between">
        <div v-if="message.type === 'user'" class="text-lg font-semibold leading-6 text-white"></div>
        <time class="text-xs font-semibold leading-6 text-gray-400">{{ message.date }}</time>
      </div>
      <p v-if="message.type === 'request'" class="text-sm leading-6 text-gray-600"><dots /></p>
      <p v-else-if="message.type === 'response'" class="rounded-lg p-2 bg-blue-800 text-sm leading-6 text-white inline-block">
        {{ displayedTexts[index] }}
      </p>

      <div v-else class="text-sm leading-6 bg-gray-600 rounded-lg text-white text-end p-2 float-end inline-block">{{ message.message }}</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';
import { type IMessage } from '@/models/Message';
import dots from './utils/dots.vue';
const route = useRoute()
let chatId = 0
if (route.params.id){
  chatId = parseInt(route.params.id[0])
}

const props = defineProps({
  messages: {
    type: Array<IMessage>,
    default: [],
  },
});

const displayedTexts = ref(props.messages.map(m => m.message));

async function typeMessage(index: number, message: string, delay = 8) {
  displayedTexts.value[index] = '';

  for (let i = 0; i < message.length; i++) {
    displayedTexts.value[index] += message.charAt(i);
    await new Promise(r => setTimeout(r, delay));
  }
}

watch(() => props.messages.length, (newLength, oldLength) => {
  if (newLength > oldLength) {
    const newMessageIndex = newLength - 1;
    const newMessage = props.messages[newMessageIndex];

    if (newMessage.type === 'response') {
      typeMessage(newMessageIndex, newMessage.message);
    }
  }
});
</script>
