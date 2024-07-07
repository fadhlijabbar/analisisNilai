/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/templates/**/*.{html,js}"],
  theme: {
    extend: {
      colors: {
        'primary-600': '#0082bf',
        'primary': '#0090d4',
        'primary-100': '#e6f4fb',
        'netral-500': '#101828',
        'netral-400': '#596275',
        'grey': '#EBEBEB',
        'disable': '#D4D4D4',
        'success': '#1C8C3B',
        'danger': '#D82D22',
        'danger-100': '#FBEAE9',
        'danger-300': '#EFABA7',
        'alert': '#F29901',
        'alert-100': '#FEF5E6',
        'alert-300': '#FBE0B3',
        'alert-600': '#DA8A01',
      },
      width: {
        '350px': '350px',
        'container': '1280px',
        'sideleft': '470px',
        'sideright': '750px',
      },
      height: {
        '60px': '60px',
      },
      fontFamily: {
        'plusjakarta': ['"Plus Jakarta Sans"'],
      },
      padding: {
        '60px': '60px',
      },
    },
  },
  plugins: [],
}

