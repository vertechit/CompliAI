
<template>
    <main class="flex flex-col h-screen">
        <div class="overflow-y-auto flex-grow" ref="chatContainer">
            <cMessages :messages="MessagesModel.listMensage"></cMessages>
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
  import {nextTick} from 'vue'
  import Messages from '@/models/Message'
  import FooterInputMensages from '@/components/footer/inputMensages.vue'
  import cMessages from '@/components/messages.vue'
  import {defaultStore} from '@/stores/default'
  const chatContainer: Ref<HTMLElement | null> = ref(null);

  const defaultStorePinia = defaultStore()
  const MessagesModel = ref(new Messages())
  const submit = async (message: string) => {
    setLoading(true)
    try {
      MessagesModel.value.addMessage({date:'',id:'',type:'user',userId:1,message})
      MessagesModel.value.addDotsLoading()
      let result = await $fetch('/api/chain',{
        method:'POST',
        body:{
          "SystemMessage": "Responde de forma educada",
          "HumamMessage": message
        }
      }) as { AiMessage: string}
      await MessagesModel.value.removeDotLoading()
      MessagesModel.value.addMessage({date:'',id:'',type:'response',userId:5,message:result.AiMessage})
    } catch (error) {
      console.log(error)
      await MessagesModel.value.removeDotLoading()
    }finally{
      setLoading(false)
    }
  }

  const setLoading = (loading:boolean) => {
    defaultStorePinia.setLoading(loading)
  }

  async function wait(ms:number) {
    return new Promise((resolve)=>{
      setTimeout(resolve,ms)
    })
  }
  watch(MessagesModel.value.listMensage,async()=> {
    await nextTick();
    scrollToBottom();
  })
const scrollToBottom = () => {
  if (chatContainer.value) {
    chatContainer.value.scrollTop = chatContainer.value.scrollHeight ;
  }
};
onMounted(scrollToBottom);

</script>