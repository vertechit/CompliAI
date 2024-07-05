
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
  definePageMeta({
  middleware: 'auth'
})
  import {nextTick} from 'vue'
  import Messages from '@/models/Message'
  import FooterInputMensages from '@/components/footer/inputMensages.vue'
  import cMessages from '@/components/messages.vue'
  import {defaultStore} from '@/stores/default'
  const route = useRoute()
  const auth = authStore()
  const chatContainer: Ref<HTMLElement | null> = ref(null);
  const defaultStorePinia = defaultStore()
  const MessagesModel = ref(new Messages())

  const chatId = route.params.id;
  try{
    let result = [] as any[];
    result = await $fetch(`/api/chathistory/${chatId}`,{
        method:'GET',
        headers: {
          "Authorization" :"bearer "+auth.token
        }
      }) as []

      result.reverse()

if(result){
  for (let i in result){
    if (result[i].tipo === 1){
      MessagesModel.value.addMessage({date: result[i].criado ,id: result[i].chathistory_id,type:'user',userId:1,message: result[i].mensagem})
    }else{
      MessagesModel.value.addMessage({date: result[i].criado ,id: result[i].chathistory_id,type:'response',userId:0,message: result[i].mensagem})
    }
    
  }
}

  }catch(error){
    clearError({ redirect: '/login?message=Token expirado' })
  }
  
  const submit = async (message: string) => {
    setLoading(true)
    try {
      MessagesModel.value.addMessage({date:'',id:'',type:'user',userId:1,message})
      MessagesModel.value.addDotsLoading()
      let result = await $fetch(`/api/chain/${chatId}`,{
        method:'POST',
        timeout: 300000,
        headers: {
          "Authorization" :"bearer "+auth.token
        },
        body:{
          "HumamMessage": message,
        }
      }) as { AiMessage: string}
      await MessagesModel.value.removeDotLoading()
      MessagesModel.value.addMessage({date:'',id:'',type:'response',userId:0,message:result.AiMessage})
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

<style>

.message_response h1 {
  display: block;
    font-size: 2em;
    margin-block-start: 0.67em;
    margin-block-end: 0.67em;
    margin-inline-start: 0px;
    margin-inline-end: 0px;
    font-weight: bold;
    unicode-bidi: isolate;
}

.message_response h2 {
  display: block;
    font-size: 1.5em;
    margin-block-start: 0.83em;
    margin-block-end: 0.83em;
    margin-inline-start: 0px;
    margin-inline-end: 0px;
    font-weight: bold;
    unicode-bidi: isolate;
}

.message_response h3 {
  display: block;
    font-size: 1.17em;
    margin-block-start: 1em;
    margin-block-end: 1em;
    margin-inline-start: 0px;
    margin-inline-end: 0px;
    font-weight: bold;
    unicode-bidi: isolate;
}

.message_response h4 {
  display: block;
    margin-block-start: 1.33em;
    margin-block-end: 1.33em;
    margin-inline-start: 0px;
    margin-inline-end: 0px;
    font-weight: bold;
    unicode-bidi: isolate;
}

.message_response h5 {
  display: block;
    font-size: 0.83em;
    margin-block-start: 1.67em;
    margin-block-end: 1.67em;
    margin-inline-start: 0px;
    margin-inline-end: 0px;
    font-weight: bold;
    unicode-bidi: isolate;
}

.message_response h6 {
  display: block;
    font-size: 0.67em;
    margin-block-start: 2.33em;
    margin-block-end: 2.33em;
    margin-inline-start: 0px;
    margin-inline-end: 0px;
    font-weight: bold;
    unicode-bidi: isolate;
}

.message_response code {
  display: inline-block;
  background-color: rgb(31, 31, 31);
  padding: 5px 5px 5px 10px;
  border-radius: 5px;
}

.message_response blockquote{
  margin: 1rem;
  padding-left: 0.5rem;
  border-left: 4px solid #dadada;
  color: #dadada;
}

.message_response a{
  color: -webkit-link;
  cursor: pointer;
  text-decoration: underline;
}

.message_response hr{
  border-width: 1px;
  margin: 5px 0px;
}

.message_response ol {
  display: block;
  list-style-type: decimal;
  margin-block-start: .1em;
  margin-block-end: .1em;
  margin-inline-start: 0px;
  margin-inline-end: 0px;
  padding-inline-start: 20px;
  unicode-bidi: isolate;
}

.message_response ol ul {
  list-style-type: circle;
    margin-block-start: 0px;
    margin-block-end: 0px;
}

.message_response ul {
  display: block;
    list-style-type: disc;
    margin-inline-start: 0px;
    margin-inline-end: 0px;
    padding-inline-start: 20px;
    unicode-bidi: isolate;
}

.message_response table {
  display: table;
    border-collapse: separate;
    box-sizing: border-box;
    text-indent: initial;
    unicode-bidi: isolate;
    border: 2px solid #ccc;
    border-spacing: 0px 0px;
    margin: 5px;
}

.message_response table th, .message_response table td {
  display: table-cell;
  border: 1px solid #ccc;
  border-spacing: 0px;
  padding: 5px;
}

.message_response p code, .message_response li code {
  padding: 0px 5px 0px 5px;
  border-radius: 5px;
  color: #DBD7CAEE;
}

</style>