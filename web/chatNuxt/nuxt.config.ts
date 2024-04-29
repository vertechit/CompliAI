// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devtools: { enabled: true },
  modules:[
    '@nuxtjs/tailwindcss',
    'nuxt-headlessui',
    '@pinia/nuxt'
  ],
  headlessui: {
    prefix: 'Headless'
},
tailwindcss:{
  viewer: false,
  configPath: 'tailwind.config.js',
},
runtimeConfig:{
  public:{
    baseURL:process.env.baseURL || ''
  }
}
})
