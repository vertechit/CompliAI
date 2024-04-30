module.exports = {
  content: [
    `layouts/**/*.vue`,
    `components/**/*.{vue,js}`,
    `pages/**/*.vue`,
    `composables/**/*.{js,ts}`,
    `plugins/**/*.{js,ts}`
  ],
  darkMode: 'class',
  theme: {
    extend: {
      scale: {
        '101': '1.01',
      },
      fontFamily: {
        'sans': ['Inter', 'sans-serif'],
        'display': ['Montserrat', 'sans-serif']
      },
      fontSize: {
        '0': '0px',
        'xs': '.825rem',
        'md': '.925rem'
      },
      colors: {
        'dark': '#0b0b0b',
        'dark-900': '#1d1c1c', //'#121416'
        'dark-800': '#262626', //'#1C1C1F'
        'dark-700': '#29292d',
        'dark-600': '#303035',
        'dark-500': '#343439',
        'dark-100': '#babbbf'
      },
      borderRadius: {
        '4xl': '2rem',
        '5xl': '2.5rem'
      }
    }
  },
  plugins: [
    require('@tailwindcss/forms'),
    require("tailwind-scrollbar"),
  ],
}
