<template>
  <div class="relative shadow bg-white p-3 rounded-2xl mt-3">
    <div class="flex">
      <div class="px-2">
        <svg v-if="notification.type === 'success'" class="w-6 h-6" :class="textColor" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
          <path fill="currentColor" d="M14.72,8.79l-4.29,4.3L8.78,11.44a1,1,0,1,0-1.41,1.41l2.35,2.36a1,1,0,0,0,.71.29,1,1,0,0,0,.7-.29l5-5a1,1,0,0,0,0-1.42A1,1,0,0,0,14.72,8.79ZM12,2A10,10,0,1,0,22,12,10,10,0,0,0,12,2Zm0,18a8,8,0,1,1,8-8A8,8,0,0,1,12,20Z"/>
        </svg>
        <svg v-else-if="notification.type === 'error'" class="w-6 h-6" :class="textColor" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
          <path fill="currentColor" d="M15.71,8.29a1,1,0,0,0-1.42,0L12,10.59,9.71,8.29A1,1,0,0,0,8.29,9.71L10.59,12l-2.3,2.29a1,1,0,0,0,0,1.42,1,1,0,0,0,1.42,0L12,13.41l2.29,2.3a1,1,0,0,0,1.42,0,1,1,0,0,0,0-1.42L13.41,12l2.3-2.29A1,1,0,0,0,15.71,8.29Zm3.36-3.36A10,10,0,1,0,4.93,19.07,10,10,0,1,0,19.07,4.93ZM17.66,17.66A8,8,0,1,1,20,12,7.95,7.95,0,0,1,17.66,17.66Z"/>
        </svg>
        <svg v-else xmlns="http://www.w3.org/2000/svg" class="w-6 h-6" :class="textColor" viewBox="0 0 24 24">
          <path fill="currentColor" d="M12,14a1.25,1.25,0,1,0,1.25,1.25A1.25,1.25,0,0,0,12,14Zm0-1.5a1,1,0,0,0,1-1v-3a1,1,0,0,0-2,0v3A1,1,0,0,0,12,12.5ZM12,2A10,10,0,1,0,22,12,10.01114,10.01114,0,0,0,12,2Zm0,18a8,8,0,1,1,8-8A8.00917,8.00917,0,0,1,12,20Z"/>
        </svg>
      </div>
      <div class="ml-2 mr-2 w-full">
        <div class="flex justify-between items-center">
          <span class="font-medium text-zinc-700 tracking-tight">{{ notification.title }}</span>
          <button type="button" class="flex justify-center items-center text-zinc-800 transform scale-75 focus:outline-none" @click="removeNotification(notification)">
            <i class="flex justify-center items-center w-[16px] h-[16px] relative transition-all ease-in-out duration-200 hover:after:w-[14px] hover:after:rotate-180 hover:before:w-[14px] hover:before:rotate-180 before:transform before:-rotate-45 before:bg-zinc-800 before:absolute before:w-[14px] before:h-[2px] before:rounded-sm before:transition-all before:ease-in-out before:duration-300 after:absolute after:w-[14px] after:h-[2px] after:transition-all after:rounded-sm after:ease-in-out after:duration-300 after:transform after:rotate-45 after:bg-zinc-800"></i>
          </button>
        </div>
        <span class="block text-zinc-500 font-light">
          {{ notification.message }}
        </span>
      </div>
    </div>
  </div>
</template>

<script>

  import { computed, onBeforeUnmount } from 'vue'
  import { useNotificationStore } from '~/stores/notification'

  export default {
    name: 'NotificationMessage',
    props: ['notification'],
    setup(props){

      let timeout = null;

      const textColor = computed(() => {
        if(props.notification.type === 'success') return 'text-green-500'
        else if(props.notification.type === 'error') return 'text-red-500'
        else return 'text-yellow-500'
      })

      const store = useNotificationStore()

      const removeNotification = (params) => {
        store.removeNotification(params)
      }

      timeout = setTimeout(() => {
        removeNotification(props.notification)
      }, 5000)

      onBeforeUnmount(() => {
        clearTimeout(timeout)
      })

      return { 
        textColor,
        removeNotification 
      }

    }
  }
</script>