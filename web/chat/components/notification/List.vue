<template>
  <div>
    <div class="fixed top-0 right-0 mr-3.5 w-96 z-50">
      <TransitionRoot
        as="div"
        :show="isShowing"
        enter="transition-all duration-300 ease-linear"
        enter-from="translate-x-96"
        enter-to="translate-0"
        leave="transition-all duration-300 ease-linear"
        leave-from="translate-0"
        leave-to="translate-x-96"
      >
        <notification-message
          v-for="notification in notifications"
          :key="notification.id"
          :notification="notification"
        />
      </TransitionRoot>
      
    </div>
  </div>
</template>

<script setup>

  import { storeToRefs } from 'pinia'
  import { TransitionRoot } from '@headlessui/vue'
  import { useNotificationStore } from '@/stores/notification.js'
  import { computed } from 'vue'

  import NotificationMessage from '@/components/notification/Message.vue'

  const store             = useNotificationStore();
  const { notifications } = storeToRefs(store)
  const isShowing         = computed(() => store.active)


</script>