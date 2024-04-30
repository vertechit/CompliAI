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
}

// import { useUserStore } from '@/stores/user';
// import { authStore } from '@/stores/auth';

export const useMyFetch = (url: string, options: FetchOptions) => {

    const runTimeConfig = useRuntimeConfig();
    // const userStore     = useUserStore();
    // const auth          = authStore();

    return $fetch(url, {
        ...options,
        retry: 3,
        retryDelay: 1000,
        async onRequest({ request, options }) {

            const { baseURL } = runTimeConfig.public
            console.log(baseURL)
            options.baseURL = baseURL
            options.headers = options.headers || {}

            // if (userStore?.userData) options.headers.authorization = 'Bearer ' + userStore?.userData?.token?.accessToken

        },
        // onRequestError será chamado quando a solicitação de busca falhar.
        async onRequestError({ request, options, error }) {
            //console.log("[onRequestError]", error)
        },
        // onResponse será chamado após fetcha chamada e análise do corpo.
        async onResponse({ request, response, options }) {
            //console.log(response)            
        },
        // onResponseError é o mesmo que, onResponse mas será chamado quando a busca acontecer, mas response.ok não for true.
        async onResponseError({ request, response, options }) {
            // if (response.status === 401) return await auth.logout()
            // else if([502,503].includes(response.status)) throw new Error('Falha de comunicação com o servidor, contate o suporte!')
        },    
    });

}