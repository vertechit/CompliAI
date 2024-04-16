// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devtools: { enabled: true },
  modules:[
    '@nuxtjs/tailwindcss',
    'nuxt-headlessui',
  ],
  headlessui: {
    prefix: 'Headless'
},
tailwindcss:{
  viewer: false,
  configPath: 'tailwind.config.js',
}
})
