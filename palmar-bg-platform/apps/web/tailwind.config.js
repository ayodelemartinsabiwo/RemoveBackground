/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        border: 'hsl(214.3 31.8% 91.4%)', // Default border color
        primary: {
          50: '#fff5f2',
          100: '#ffe8e1',
          200: '#ffd4c7',
          300: '#ffb89f',
          400: '#ff9066',
          500: '#ff6b35', // Main brand color - var(--primary-color)
          600: '#f04c1a',
          700: '#d13910',
          800: '#a82f10',
          900: '#892a13',
          950: '#4b1206',
          dark: '#e85a28', // var(--primary-dark)
          light: '#ff8555', // var(--primary-light)
        },
        secondary: {
          DEFAULT: '#2d3748', // var(--secondary-color)
        },
        text: {
          dark: '#1a202c', // var(--text-dark)
          light: '#4a5568', // var(--text-light)
          muted: '#718096', // var(--text-muted)
        },
        bg: {
          light: '#f7fafc', // var(--bg-light)
          white: '#ffffff', // var(--bg-white)
        },
        gradient: {
          start: '#ff6b35', // var(--gradient-start)
          end: '#ff8555', // var(--gradient-end)
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'Helvetica Neue', 'Arial', 'sans-serif'],
      },
      boxShadow: {
        'sm': '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)',
        'md': '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
        'lg': '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
        'xl': '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
        '2xl': '0 25px 50px -12px rgba(0, 0, 0, 0.25)',
      },
      animation: {
        'float': 'float 6s ease-in-out infinite',
        'float-center': 'floatCenter 5s ease-in-out infinite',
        'float-delayed': 'float 7s ease-in-out infinite 1s',
        'mask-reveal': 'maskReveal 6s ease-in-out infinite',
        'line-sweep': 'lineSweep 6s ease-in-out infinite',
        'sparkle': 'sparkle 0.6s ease-in-out infinite',
        'arrow-bounce-h': 'arrowBounceHorizontal 1.5s ease-in-out infinite',
        'arrow-bounce-v': 'arrowBounceVertical 1.5s ease-in-out infinite',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-20px)' },
        },
        floatCenter: {
          '0%, 100%': { transform: 'translate(-50%, -50%) translateY(0px)' },
          '50%': { transform: 'translate(-50%, -50%) translateY(-15px)' },
        },
        maskReveal: {
          '0%, 15%': { clipPath: 'inset(0 0 0 0)' },
          '50%, 65%': { clipPath: 'inset(0 0 0 100%)' },
          '100%': { clipPath: 'inset(0 0 0 0)' },
        },
        lineSweep: {
          '0%, 15%': { right: '100%', opacity: '0' },
          '20%': { right: '100%', opacity: '1' },
          '50%': { right: '0%', opacity: '1' },
          '55%': { right: '0%', opacity: '0' },
          '100%': { right: '100%', opacity: '0' },
        },
        sparkle: {
          '0%, 100%': { opacity: '0', transform: 'scale(0.5)' },
          '50%': { opacity: '1', transform: 'scale(1.5)' },
        },
        arrowBounceHorizontal: {
          '0%, 100%': { transform: 'translateX(0)', opacity: '1' },
          '50%': { transform: 'translateX(10px)', opacity: '0.7' },
        },
        arrowBounceVertical: {
          '0%, 100%': { transform: 'translateY(0)', opacity: '1' },
          '50%': { transform: 'translateY(10px)', opacity: '0.7' },
        },
      },
    },
  },
  plugins: [],
}
