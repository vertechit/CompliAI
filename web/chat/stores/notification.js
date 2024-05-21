import { defineStore } from 'pinia'
import crypto from 'crypto';
export const useNotificationStore = defineStore('notification', {
     
    state: () => ({
        notifications: []
    }),

  actions: {
    addNotification(payload) {
      this.notifications.push({
        ...payload,
        id: ("0."+crypto.randomInt(0, parseInt(100000000000000)).toString(36) + Date.now().toString(36)).substr(2),
      });
    },
    removeNotification(payload) {
      this.notifications = this.notifications.filter(
        (notification) => notification.id != payload.id,
      );
    },
    successNotification(title = null, message) {
      this.addNotification({
        type: "success",
        title: title || "Tudo Certo!",
        message: message,
      });
    },
    errorNotification(title,message) {
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
