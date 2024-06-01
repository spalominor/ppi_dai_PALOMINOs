/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './consumo_gasolina/templates/**/*.html',  // Archivos de plantilla Django en la app consumo_gasolina
    './consumo_gasolina/static/src/**/*.js',   // Archivos JavaScript en la app consumo_gasolina
    // Incluye otras rutas si es necesario
  ],
  darkMode: 'class', // or 'media' or 'class'
  theme: {
    extend: {
      colors: {
        'primary': '#7d2fd0',
        'secondary': {
          100: '#efbbff', 
          200: '#660066'},
      }
    },
  },
  plugins: [],
}

