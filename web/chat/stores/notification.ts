import { defineStore } from 'pinia'

export const useNotificationStore = defineStore('notification', {
     
    state: () => ({
        notifications: []
    }),

  actions: {
    addNotification(payload:any) {
      this.notifications.push({
        ...payload,
        id: (Math.random().toString(36) + Date.now().toString(36)).substr(2),
      });
    },
    removeNotification(payload:any) {
      this.notifications = this.notifications.filter(
        (notification) => notification.id != payload.id,
      );
    },
    successNotification(title = null, message:string) {
      this.addNotification({
        type: "success",
        title: title || "Tudo Certo!",
        message: message,
      });
    },
    errorNotification(title:string | null = null, message:string) {
      this.addNotification({
        type: "error",
        title: title || "Ops! Algo deu errado!",
        message: message  || "Por favor, tente novamente.",
      });
    },
  },
  getters: {
    active: (state) => (state.notifications.length ? true : false),
  },
});
