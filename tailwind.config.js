/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './app/templates/**/*.html',
    './app/blueprints/**/*.py',
    './app/forms.py',
  ],
  theme: {
    extend: {
      colors: {
        white: '#F7FAFC',
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
  ],
}