import { useRuntimeConfig } from '#imports';
import { authStore } from '@/stores/auth';

type FetchOptions = {
  key?: string;
  method?: "GET" | "POST" | "PUT" | "PATCH" | "DELETE";
  headers?: any;
  body?: any;
  baseURL?: string;
  server?: boolean;
  lazy?: boolean;
  immediate?: boolean;
  mode?: "cors" | "no-cors" | "same-origin";
  credentials?: "omit" | "same-origin" | "include";
  cache?: "default" | "no-store" | "reload" | "no-cache" | "force-cache" | "only-if-cached";
  redirect?: "follow" | "error" | "manual";
  referrer?: string;
  integrity?: any;
  initialCache?: boolean;
  timeout?: number;
}

export const useMyFetch = (url: string, options: FetchOptions = {}) => {
  const config = useRuntimeConfig();

  return $fetch(url, {
    ...options,
    retry: 3,
    retryDelay: 1000,
    async onRequest({ request, options }) {
      options.baseURL = window.location.origin;
      options.headers = options.headers || {};

      if (authStore()?.token) {
        options.headers.authorization = 'Bearer ' + authStore().token;
      }
    },
    // onRequestError será chamado quando a solicitação de busca falhar.
    async onRequestError({ request, options, error }) {
      console.error('Request Error:', error);
      return Promise.reject(request);
    },
    // onResponse será chamado após fetcha chamada e análise do corpo.
    async onResponse({ request, response, options }) {
      // Processar a resposta, se necessário
    },
    async onResponseError({ request, response, options }) {
      if (response.status === 401) {
        await authStore().logout();
      }
      return Promise.reject(response);
    },
  });
}
