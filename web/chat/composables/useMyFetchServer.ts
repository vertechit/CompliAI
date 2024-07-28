import { useRuntimeConfig } from '#imports';
import { getCookie } from 'h3';

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

export const useMyFetchServer = (url: string, options: FetchOptions = {}, event) => {
  const config = useRuntimeConfig();
  return $fetch(url, {
    ...options,
    retry: 3,
    retryDelay: 1000,
    async onRequest({ request, options }) {
      options.baseURL = config.public.baseURL as string;
      options.headers = options.headers || {};

      // Capturar o token dos cookies no lado do servidor
      if (process.server && event) {
        const token = getCookie(event, 'token');
        if (token) {
          options.headers.authorization = 'Bearer ' + token;
        }
      } 
    },
    // onRequestError será chamado quando a solicitação de busca falhar.
    async onRequestError({ request, options, error }) {
      console.error('Request Error:', error);
    },
    async onResponse({ request, response, options }) {
    },
    async onResponseError({ request, response, options }) {
    },
  });
}
