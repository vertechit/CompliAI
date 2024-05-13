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
                    <ul role="list" class="flex flex-1 flex-col gap-y-7">
                      <li>
                        <ul role="list" class="-mx-2 space-y-1">
                          <li v-for="item in navigation" :key="item.name">
                            <a :href="item.href" :class="[item.current ? 'bg-blue-800 text-white' : 'text-white hover:text-white hover:bg-blue-800', 'group flex gap-x-3 rounded-md p-2 text-sm leading-6 font-semibold']">
                              <component :is="item.icon" class="h-6 w-6 shrink-0" aria-hidden="true" />
                              {{ item.name }}
                            </a>
                          </li>
                        </ul>
                      </li>
                      <li>
                        <div class="text-xs font-semibold leading-6 text-white">Your teams</div>
                        <ul role="list" class="-mx-2 mt-2 space-y-1">
                          <li v-for="team in teams" :key="team.name">
                            <a :href="team.href" :class="[team.current ? 'bg-blue-800 text-white' : 'text-white hover:text-white hover:bg-blue-800', 'group flex gap-x-3 rounded-md p-2 text-sm leading-6 font-semibold']">
                              <span class="flex h-6 w-6 shrink-0 items-center justify-center rounded-lg border border-blue-700 bg-blue-800 text-[0.625rem] font-medium text-white group-hover:text-white">{{ team.initial }}</span>
                              <span class="truncate">{{ team.name }}</span>
                            </a>
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
            <ul role="list" class="flex flex-1 flex-col gap-y-7">
              <li>
                <ul role="list" class="-mx-2 space-y-1">
                  <li v-for="item in navigation" :key="item.name">
                    <a :href="item.href" :class="[item.current ? 'bg-blue-800 text-white' : 'text-white hover:text-white hover:bg-blue-800', 'group flex gap-x-3 rounded-md p-2 text-sm leading-6 font-semibold']">
                      <component :is="item.icon" class="h-6 w-6 shrink-0" aria-hidden="true" />
                      {{ item.name }}
                    </a>
                  </li>
                </ul>
              </li>
              <li>
                <div class="text-xs font-semibold leading-6 text-white">Your teams</div>
                <ul role="list" class="-mx-2 mt-2 space-y-1">
                  <li v-for="team in teams" :key="team.name">
                    <a :href="team.href" :class="[team.current ? 'bg-blue-800 text-white' : 'text-white hover:text-white hover:bg-blue-800', 'group flex gap-x-3 rounded-md p-2 text-sm leading-6 font-semibold']">
                      <span class="flex h-6 w-6 shrink-0 items-center justify-center rounded-lg border border-blue-700 bg-blue-800 text-[0.625rem] font-medium text-white group-hover:text-white">{{ team.initial }}</span>
                      <span class="truncate">{{ team.name }}</span>
                    </a>
                  </li>
                </ul>
              </li>
              <li class="-mx-6 mt-auto">
                <a href="#" class="flex items-center gap-x-4 px-6 py-3 text-sm font-semibold leading-6 text-white hover:bg-blue-800">
                  <img class="h-8 w-8 rounded-full bg-blue-800" src="https://images.unsplash.com/photo-1550525811-e5869dd03032?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80" alt="" />
                  <span class="sr-only">Your profile</span>
                  <span aria-hidden="true">Bete</span>
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
        <div class="flex-1 text-sm font-semibold leading-6 text-white">Chat</div>
        <a href="#">
          <span class="sr-only">Your profile</span>
          <img class="h-8 w-8 rounded-full bg-blue-800" src="https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80" alt="" />
        </a>
      </div>
  
      <main class="lg:pl-72">
        <div class="pl-4 ">
        
          <slot />
        </div>
      </main>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import {
    Bars3Icon,
    CalendarIcon,
    ChartPieIcon,
    DocumentDuplicateIcon,
    FolderIcon,
    DocumentTextIcon,
    XMarkIcon,
    ChatBubbleOvalLeftEllipsisIcon
  } from '@heroicons/vue/24/outline'
  
  const navigation = [
    { name: 'Chat', href: '/', icon: ChatBubbleOvalLeftEllipsisIcon, current: true },
    { name: 'Documentos', href: '/documentos', icon: DocumentTextIcon, current: false },
    { name: 'Projects', href: '#', icon: FolderIcon, current: false },
    { name: 'Calendar', href: '#', icon: CalendarIcon, current: false },
    { name: 'Documents', href: '#', icon: DocumentDuplicateIcon, current: false },
    { name: 'Reports', href: '#', icon: ChartPieIcon, current: false },
  ]
  const teams = [
    { id: 1, name: 'Heroicons', href: '#', initial: 'H', current: false },
    { id: 2, name: 'Tailwind Labs', href: '#', initial: 'T', current: false },
    { id: 3, name: 'Workcation', href: '#', initial: 'W', current: false },
  ]
  
  const sidebarOpen = ref(false)
  </script>