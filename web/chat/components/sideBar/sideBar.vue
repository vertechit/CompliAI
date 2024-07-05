<template>
    <div>
      <HeadlessTransitionRoot as="template" :show="sidebarOpen">
        <HeadlessDialog as="div" class="relative z-50 lg:hidden" @close="sidebarOpen = false">
          <HeadlessTransitionChild as="template" enter="transition-opacity ease-linear duration-300" enter-from="opacity-0" enter-to="opacity-100" leave="transition-opacity ease-linear duration-300" leave-from="opacity-100" leave-to="opacity-0">
            <div class="fixed inset-0 bg-gray-900/80" />
          </HeadlessTransitionChild>
  
          <div class="fixed inset-0 flex">
            <HeadlessTransitionChild as="template" enter="transition ease-in-out duration-300 transform" enter-from="-translate-x-full" enter-to="translate-x-0" leave="transition ease-in-out duration-300 transform" leave-from="translate-x-0" leave-to="-translate-x-full">
              <HeadlessDialogPanel class="relative mr-16 flex w-full max-w-xs flex-1">
                <HeadlessTransitionChild as="template" enter="ease-in-out duration-300" enter-from="opacity-0" enter-to="opacity-100" leave="ease-in-out duration-300" leave-from="opacity-100" leave-to="opacity-0">
                  <div class="absolute left-full top-0 flex w-16 justify-center pt-5">
                    <button type="button" class="-m-2.5 p-2.5" @click="sidebarOpen = false">
                      <span class="sr-only">Close sidebar</span>
                      <XMarkIcon class="h-6 w-6 text-white" aria-hidden="true" />
                    </button>
                  </div>
                </HeadlessTransitionChild>
                <div class="flex grow flex-col gap-y-5 overflow-y-auto bg-blue-900 px-6 pb-2 ring-1 ring-white/10">
                  <div class="flex h-32 shrink-0 items-center">
                    <img class="h-8 w-auto" src="~/assets/img/logoCompliIc.png" alt="Compliance Soluções" />
                  </div>
                  <nav class="flex flex-1 flex-col">
                    <ul  class="flex flex-1 flex-col gap-y-7">
                      <li>
                        <ul  class="-mx-2 space-y-1">
                          <li v-for="item in navigation" :key="item.name">
                            <a :href="item.href" :class="[item.href === route.path ? 'bg-blue-800 text-white' : 'text-white hover:text-white hover:bg-blue-800', 'group flex gap-x-3 rounded-md p-2 text-sm leading-6 font-semibold']">
                              <component :is="item.icon" class="h-6 w-6 shrink-0" aria-hidden="true" />
                              {{ item.name }}
                            </a>
                          </li>
                        </ul>
                      </li>
                      <li>
                        <div class="group flex gap-x-3 text-xl font-semibold leading-6 text-white">
                          <component :is="ChatBubbleOvalLeftEllipsisIcon" class="h-6 w-6 shrink-0" aria-hidden="true" />
                          Chats
                          <div style="margin-left: auto;">
                            <a href="#" class="justify-end">
                              <component :is="PlusCircleIcon" class="h-6 w-6 shrink-0" aria-hidden="true" @click="changeModalCriarChat(true)"/>
                            </a>
                          </div>
                        </div>
                        <ul  class="-mx-2 mt-2 max-h-[500px] overflow-y-auto overflow-x-hidden">
                          <li v-for="chat in chats" :key="chat.titulo" class="ml-5 hover:bg-blue-800 group relative">
                            <a :href="'/chats/'+chat.session_id" :class="[chatId == chat.session_id ? 'bg-blue-800 text-white' : 'text-white hover:text-white', 'flex gap-x-3 rounded-md pl-2 p-1 text-xs font-thin']">
                              <span class="truncate" :title="chat.titulo">{{ chat.titulo }}</span>
                            </a>
                            <div class="absolute inset-y-0 right-1 hidden group-hover:block bg-blue-800">
                                <component :is="TrashIcon" class="text-neutral-500 h-6 w-6 " aria-hidden="true" @click="openDeleteDialog(chat.session_id, chat.titulo)"/>
                              </div>
                          </li>
                        </ul>
                      </li>
                    </ul>
                  </nav>
                </div>
              </HeadlessDialogPanel>
            </HeadlessTransitionChild>
          </div>
        </HeadlessDialog>
      </HeadlessTransitionRoot>
  
      <div class="hidden lg:fixed lg:inset-y-0 lg:z-50 lg:flex lg:w-64 lg:flex-col ">
        <div class="flex grow flex-col gap-y-5 overflow-y-auto p-1 bg-blue-900 px-6 rounded-r-xl" >
          <div class="flex h-14 shrink-0 items-center">
            <img class="w-auto h-full" src="~/assets/img/logoCompliIc.png" alt="Compliance Soluções" />
          </div>
          <nav class="flex flex-1 flex-col">
            <ul  class="flex flex-1 flex-col gap-y-7">
              <li>
                <ul  class="-mx-2 space-y-1">
                  <li v-for="item in navigation" :key="item.name">
                    <a :href="item.href" :class="[item.href === route.path ? 'bg-blue-800 text-white' : 'text-white hover:text-white hover:bg-blue-800', 'group flex gap-x-3 rounded-md p-2 text-sm leading-6 font-semibold']">
                      <component :is="item.icon" class="h-6 w-6 shrink-0" aria-hidden="true" />
                      {{ item.name }}
                    </a>
                  </li>
                </ul>
              </li>
              <li>
                <div class="group flex gap-x-3 text-xl font-semibold leading-6 text-white">
                  <component :is="ChatBubbleOvalLeftEllipsisIcon" class="h-6 w-6 shrink-0" aria-hidden="true" />
                  Chats
                  <div style="margin-left: auto;">
                    <a href="#" class="justify-end">
                      <component :is="PlusCircleIcon" class="h-6 w-6 shrink-0" aria-hidden="true" @click="changeModalCriarChat(true)"/>
                    </a>
                  </div>
                </div>
                <ul  class="-mx-2 mt-2 max-h-[500px] overflow-y-auto overflow-x-hidden">
                  <li v-for="chat in chats" :key="chat.titulo" class="ml-5 hover:bg-blue-800 group relative">
                    <a :href="'/chats/'+chat.session_id" :class="[chatId == chat.session_id ? 'bg-blue-800 text-white' : 'text-white hover:text-white', 'flex gap-x-3 rounded-md pl-2 p-1 text-xs font-thin']">
                      <span class="truncate" :title="chat.titulo">{{ chat.titulo }}</span>
                    </a>
                    <div class="absolute inset-y-0 right-1 hidden group-hover:block bg-blue-800">
                        <component :is="TrashIcon" class="text-neutral-500 h-6 w-6 " aria-hidden="true" @click="openDeleteDialog(chat.session_id, chat.titulo)"/>
                      </div>
                  </li>
                </ul>
              </li>
              <li class="-mx-6 mt-auto">
                <a href="#" class="flex items-center gap-x-4 px-6 py-3 text-sm font-semibold leading-6 text-white hover:bg-blue-800">
                  <component :is="UserCircleIcon" class="h-8 w-8"></component>
                  <span class="sr-only">Your profile</span>
                  <span class="truncate" aria-hidden="true">{{auth.login}}</span>
                </a>
              </li>
            </ul>
          </nav>
        </div>
      </div>
  
      <div class="sticky top-0 z-40 flex items-center gap-x-6 bg-blue-900 px-4 py-4 shadow-sm sm:px-6 lg:hidden">
        <button type="button" class="-m-2.5 p-2.5 text-gray-400 lg:hidden" @click="sidebarOpen = true">
          <span class="sr-only">Open sidebar</span>
          <Bars3Icon class="h-6 w-6" aria-hidden="true" />
        </button>
        <div class="flex-1 text-sm font-semibold leading-6 text-white">Menu</div>
        <a href="#" class="text-white">
          <div class="flex">
            <span class="sr-only">Your profile</span>
            <component :is="UserCircleIcon" class="h-8 w-8"></component>
            <span class="sr-only">Your profile</span>
            <span class="truncate" aria-hidden="true">{{auth.login}}</span>
          </div>
        </a>
      </div>
  
      <main class="lg:pl-72">
        <ModalConfirmDelete
          title="Atenção"
          :text="'Deseja realmente excluir a sessão '+currentTitle+'?'"
          :isOpen="isOpenModalDelete"
          @confirm="deleteSesssion(currentElement)"
          @close="close()"
          >
        </ModalConfirmDelete>

        <SlideOversWithFooter  v-if="modalCriarChat" title="Iniciar novo chat" @close="changeModalCriarChat(false)" >
            <template #content>
                <FormFormsCriarChat :chat-list="chatList" :clear-form="clearForm" :submit-form="submitForm" @close="forceGetList = !forceGetList ,changeModalCriarChat(false)"  />
            </template>
            <template #footer>
                <div class="space-x-2">
                    <buttonsDefault @action="clearForm = !clearForm" label="Limpar" custom="white !text-black border hover:bg-gray-100" />
                    <buttonsDefault @action="submitForm = !submitForm" label="Enviar" custom="bg-green-500 hover:bg-green-600" />
                </div>
            </template>
        </SlideOversWithFooter>
        <div class="pl-4 ">
        
          <slot />
        </div>
      </main>
    </div>
  </template>
  
  <script setup lang="ts">
import { authStore } from '@/stores/auth'
import { ref } from 'vue'
import {
  Bars3Icon,
  DocumentTextIcon,
  XMarkIcon,
  ChatBubbleOvalLeftEllipsisIcon,
  HomeIcon,
  TrashIcon
} from '@heroicons/vue/24/outline'
import { PlusCircleIcon, UserCircleIcon } from '@heroicons/vue/20/solid';
import { type ChatSession } from '@/models/Chatsession/List'

const submitForm = ref(false)
const clearForm = ref(false)
const forceGetList = ref(false)
const chatList = ref([] as ChatSession[])
const chats = ref(chatList)
const isOpenModalDelete = ref(false)
const currentElement = ref(0)
const currentTitle = ref('')

const modalCriarChat = ref(false)
const changeModalCriarChat = (value: boolean) => modalCriarChat.value = value

const close = async () => {
    isOpenModalDelete.value = false;
    currentElement.value = 0
}

const openDeleteDialog = async (value: number, titulo: string) => {
  isOpenModalDelete.value = true
  currentElement.value = value
  currentTitle.value = '"'+titulo+'"'
}

const deleteSesssion = async (value: number) => {
  await $fetch(`/api/chatsession/${value}`,{
    method: "DELETE",
    headers: {
        "Authorization" :"bearer "+auth.token
    }
  })
  await getSessions()
  await navigateTo('/home')
  await close()
}

const navigation = ref([
  { name: 'Home', href: '/home', icon: HomeIcon},
  { name: 'Documentos', href: '/documentos', icon: DocumentTextIcon},
])

const sidebarOpen = ref(false)
const route = useRoute()
const auth = authStore()
let chatId = ref(0)
if (route.params.id){
  chatId.value = parseInt(route.params.id as string)
}


const getSessions = async () => {
  try{
     let retorno
     retorno = await $fetch('/api/chatsession/list',{
      method: "GET",
      headers: {
        "Authorization" :"bearer "+auth.token
      }
    }) as ChatSession[]

    chatList.value = retorno.reverse()
  }catch(error){
    clearError({ redirect: '/login?message=Token expirado' })
  }

}
await getSessions()

watch(() => route.fullPath, () => {
    chatId.value = parseInt(route.params.id as string)
});

  </script>