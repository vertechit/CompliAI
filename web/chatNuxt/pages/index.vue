
<template>
    <main class="flex flex-col h-screen">
        <div class="overflow-y-auto m-0 flex-grow" ref="chatContainer">
            <chat :mensages="MessagesModel.listMensage"></chat>
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
  import chat from '@/components/chat.vue'
  import {defaultStore} from '@/stores/default'
  const chatContainer: Ref<HTMLElement | null> = ref(null);

  const defaultStorePinia = defaultStore()
  const MessagesModel = ref(new Messages())
  const submit = async (message: string) => {
    setLoading(true)
    try {
      MessagesModel.value.addMessage({date:'',id:'',type:'user',userId:1,message})
      MessagesModel.value.addDotsLoading()
       await  wait(1000)
       MessagesModel.value.removeDotLoading()
    } catch (error) {
      console.log(error)
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
  console.log(chatContainer.value)
  if (chatContainer.value) {
    chatContainer.value.scrollTop = chatContainer.value.scrollHeight ;
  }
};
onMounted(scrollToBottom);

</script>