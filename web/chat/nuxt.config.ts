import { nodePolyfills } from 'vite-plugin-node-polyfills'
// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devtools: { enabled: true },
  vite: {
    plugins: [
      nodePolyfills({
        exclude: [
          'assert',
          'buffer',
          'child_process',
          'cluster',
          'dgram',
          'dns',
          'domain',
          'events',
          'fs',
          'http',
          'https',
          'net',
          'os',
          'path',
          'punycode',
          'querystring',
          'readline',
          'stream',
          'string_decoder',
          'timers',
          'tls',
          'tty',
          'url',
          'util',
          'vm',
          'zlib',
        ],
        globals: {
          Buffer: true,
          global: true,
          process: true,
        },
        protocolImports: true,
      }),
    ],
  },
  modules:[
    '@nuxtjs/tailwindcss',
    'nuxt-headlessui',
    '@pinia/nuxt',
    'nuxt-icon',
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
    baseURL:process.env.WEB_BASE_URL || ''
  }
}
})
