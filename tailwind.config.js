/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      // COLORS - Raven Custom Glass Brand Palette
      colors: {
        raven: {
          // Primary Colors
          black: '#000000',
          white: '#FFFFFF',
          
          // Gray Scale (9-step) - matching ravencustomglass.com
          'gray-50': '#f9f9f9',
          'gray-100': '#f5f5f5',
          'gray-200': '#e0e0e0',
          'gray-300': '#d0d0d0',
          'gray-400': '#b0b0b0',
          'gray-500': '#808080',
          'gray-600': '#666666',
          'gray-700': '#4d4d4d',
          'gray-800': '#1a1a1a',
          'gray-900': '#0a0a0a',
          
          // Accent Colors - Premium
          'accent-gold': '#d4af37',
          'accent-blue': '#0066cc',
          'accent-blue-hover': '#005bb3',
          
          // Functional Colors
          'success': '#4CAF50',
          'warning': '#FF9800',
          'error': '#F44336',
          'info': '#2196F3',
        },
      },

      // TYPOGRAPHY - Font Families
      fontFamily: {
        // Use system font stack that matches modern sans-serif style
        heading: [
          '-apple-system',
          'BlinkMacSystemFont',
          '"Segoe UI"',
          '"Roboto"',
          '"Oxygen"',
          '"Ubuntu"',
          '"Cantarell"',
          '"Fira Sans"',
          '"Droid Sans"',
          '"Helvetica Neue"',
          'sans-serif',
        ],
        body: [
          '-apple-system',
          'BlinkMacSystemFont',
          '"Segoe UI"',
          '"Roboto"',
          '"Oxygen"',
          '"Ubuntu"',
          '"Cantarell"',
          '"Fira Sans"',
          '"Droid Sans"',
          '"Helvetica Neue"',
          'sans-serif',
        ],
        mono: [
          '"JetBrains Mono"',
          '"Monaco"',
          '"Courier New"',
          'monospace',
        ],
      },

      // TYPOGRAPHY - Font Sizes with Line Heights
      fontSize: {
        'xs': ['12px', { lineHeight: '16px', letterSpacing: '0px' }],
        'sm': ['14px', { lineHeight: '20px', letterSpacing: '0px' }],
        'base': ['16px', { lineHeight: '24px', letterSpacing: '0px' }],
        'lg': ['18px', { lineHeight: '28px', letterSpacing: '0px' }],
        'xl': ['20px', { lineHeight: '28px', letterSpacing: '-0.5px' }],
        '2xl': ['24px', { lineHeight: '32px', letterSpacing: '-0.5px' }],
        '3xl': ['30px', { lineHeight: '36px', letterSpacing: '-1px' }],
        '4xl': ['36px', { lineHeight: '44px', letterSpacing: '-1px' }],
        '5xl': ['48px', { lineHeight: '56px', letterSpacing: '-1.5px' }],
      },

      // FONT WEIGHTS
      fontWeight: {
        thin: '100',
        extralight: '200',
        light: '300',
        normal: '400',
        medium: '500',
        semibold: '600',
        bold: '700',
        extrabold: '800',
        black: '900',
      },

      // SPACING - 4px base unit
      spacing: {
        0: '0px',
        1: '4px',
        2: '8px',
        3: '12px',
        4: '16px',
        5: '20px',
        6: '24px',
        7: '28px',
        8: '32px',
        9: '36px',
        10: '40px',
        11: '44px',
        12: '48px',
        14: '56px',
        16: '64px',
        20: '80px',
        24: '96px',
        28: '112px',
        32: '128px',
        36: '144px',
        40: '160px',
        44: '176px',
        48: '192px',
        52: '208px',
        56: '224px',
        60: '240px',
        64: '256px',
        72: '288px',
        80: '320px',
        96: '384px',
      },

      // BORDER RADIUS - Raven style
      borderRadius: {
        'none': '0px',
        'sm': '4px',
        'base': '6px',
        'md': '8px',
        'lg': '12px',
        'xl': '16px',
        '2xl': '20px',
        '3xl': '24px',
        'full': '9999px',
      },

      // BOX SHADOWS - Raven subtle design
      boxShadow: {
        'none': 'none',
        'sm': '0 1px 2px 0 rgb(0 0 0 / 0.05)',
        'base': '0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)',
        'md': '0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)',
        'lg': '0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)',
        'xl': '0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1)',
        '2xl': '0 25px 50px -12px rgb(0 0 0 / 0.25)',
        'inner': 'inset 0 2px 4px 0 rgb(0 0 0 / 0.05)',
        'focus': '0 0 0 3px rgba(0, 0, 0, 0.1)',
        'hover': '0 10px 15px -3px rgb(0 0 0 / 0.15)',
      },

      // TRANSITIONS - Professional pacing
      transitionDuration: {
        '75': '75ms',
        '100': '100ms',
        '150': '150ms',
        '200': '200ms',
        '300': '300ms',
        '500': '500ms',
        '700': '700ms',
        '1000': '1000ms',
      },

      transitionTimingFunction: {
        'linear': 'linear',
        'in': 'cubic-bezier(0.4, 0, 1, 1)',
        'out': 'cubic-bezier(0, 0, 0.2, 1)',
        'in-out': 'cubic-bezier(0.4, 0, 0.2, 1)',
        'ease-out': 'cubic-bezier(0.4, 0, 0.2, 1)',
      },

      // ANIMATIONS
      animation: {
        'fadeIn': 'fadeIn 300ms ease-out forwards',
        'slideUp': 'slideUp 300ms ease-out forwards',
        'slideDown': 'slideDown 300ms ease-out forwards',
        'pulse': 'pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      },

      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        slideDown: {
          '0%': { transform: 'translateY(-10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
}
