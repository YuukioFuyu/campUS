/** @type {import('tailwindcss').Config} */
const defaultTheme = require('tailwindcss/defaultTheme')

module.exports = {
  content: [
    "./templates/**/*.html",
    "./static/src/**/*.js"
  ],
  theme: {
    extend: {
      keyframes: {
        'fade-inleft': {
          'from': {
            opacity: '0',
            position: 'relative',
            left: '-80px'
          },
          'to': {
            opacity: '1',
            position: 'relative',
            left: '0px'
          },
        },
        'fade-intop': {
          'from': {
            opacity: '0',
            position: 'relative',
            top: '-50px'
          },
          'to': {
            opacity: '1',
            position: 'relative',
            top: '0px'
          }
        },

      },
      animation: {
        'fade-inleft': 'fade-inleft 2s ease-out forwards',
        'delay-fade-inleft': 'fade-inleft 2s ease-out .3s forwards',
        'fade-intop': 'fade-intop 2s ease-out forwards',
        'delay-fade-intop': 'fade-intop 2s ease-out .3s forwards',

      },
      fontFamily: {
        'lato': ['Lato', ...defaultTheme.fontFamily.sans],
        'dogica-regular': ['dogica-regular', ...defaultTheme.fontFamily.sans],
        'dogica-regular-bold': ['dogica-bold', ...defaultTheme.fontFamily.sans],
        'dogica-pixel': ['dogica-pixel', ...defaultTheme.fontFamily.sans],
        'dogica-pixel-bold': ['dogica-pixelbold', ...defaultTheme.fontFamily.sans]
      },
    },
  },
  plugins: [
    require("daisyui"),
    require("tailwind-scrollbar")({ nocompatible: true })
  ],
  daisyui: {
    themes: false, // true: all themes | false: only light + dark | array: specific themes like this ["light", "dark", "cupcake"]
    darkTheme: "dark", // name of one of the included themes for dark mode
    base: true, // applies background color and foreground color for root element by default
    styled: true, // include daisyUI colors and design decisions for all components
    utils: true, // adds responsive and modifier utility classes
    rtl: false, // rotate style direction from left-to-right to right-to-left. You also need to add dir="rtl" to your html tag and install `tailwindcss-flip` plugin for Tailwind CSS.
    prefix: "@", // prefix for daisyUI classnames (components, modifiers and responsive class names. Not colors)
    logs: true, // Shows info about daisyUI version and used config in the console when building your CSS
  },
}

