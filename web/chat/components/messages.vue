<template>
  <div class="flex items-center gap-x-4 py-2 pr-2" v-for="(message, index) in messages" :key="index" :type="message.type">
    <div class="flex-1">
      <div class="flex items-center justify-between">
        <div v-if="message.type === 'user'" class="text-lg font-semibold leading-6 text-white"></div>
        <time class="text-xs font-semibold leading-6 text-gray-400">{{ message.date }}</time>
      </div>
      <p v-if="message.type === 'request'" class="text-sm leading-6 text-gray-600"><dots /></p>
      <!-- <p v-else-if="message.type === 'response'" class="rounded-lg p-2 bg-blue-800 text-sm leading-6 text-white inline-block">
        {{ displayedTexts[index] }}
      </p> -->
      <ContentRenderer v-else-if="message.type === 'response'" class="message_response rounded-lg p-2 bg-blue-500 text-sm leading-6 text-white inline-block" :value="displayedTexts[index]"/>

      <div v-else class="text-sm leading-6 bg-gray-500 rounded-lg text-white p-2 float-end inline-block">{{ message.message }}</div>
      <!-- <ContentRenderer v-else class="rounded-lg p-2 bg-blue-800 text-sm leading-6 text-white inline-block" :value="markdon"/> -->

    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';
import { type IMessage } from '@/models/Message';
import dots from './utils/dots.vue';
import markdownParser from '@nuxt/content/transformers/markdown';

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

const displayedTexts = ref([] as Array<IMessage>);

for(let idx in props.messages){
  displayedTexts.value.push(await markdownParser.parse(null, props.messages[idx].message))
}

watch(() => props.messages.length, async (newLength, oldLength) => {
  if (newLength > oldLength) {
    const newMessageIndex = newLength - 1;
    const newMessage = props.messages[newMessageIndex];

    if (newMessage.type === 'response') {
      displayedTexts.value[newMessageIndex] = await markdownParser.parse(null, newMessage.message);
    }
  }
});
</script>
