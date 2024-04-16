
<template>
    <main class="flex flex-col h-screen">
        <div class="overflow-auto">
            <chat :mensages="mensages"></chat>
        </div>
        <div class="mt-auto">
            <div class="sticky bottom-0 bg-white py-2 w-full  border-t-2 pt-2">
                <div class="justify-between w-full mx-auto px-4">
                    <FooterInputMensages  @submit="submit($event)"></FooterInputMensages>
                </div>
            </div>
        </div>
    </main>
  </template>
  <script setup lang="ts">
  import FooterInputMensages from '@/components/footer/inputMensages.vue'
  import chat from '@/components/chat.vue'
  
  const mensages = ref([])
  const submit = (message: string) => {
    mensages.value.push({
      message,
      date: new Date().toLocaleDateString('pt-br', {
        day: 'numeric',
        month: 'short',
        year: 'numeric',
      }),
    })
  }
</script>