module.exports = [
  {
    ignores: [
      '.nuxt/**',
      '.output/**',
      'dist/**',
      'node_modules/**',
      '**/*.d.ts'
    ]
  },
  {
    languageOptions: {
      ecmaVersion: 2020,
      sourceType: 'module',
      parser: require('vue-eslint-parser'),
      parserOptions: {
        parser: '@typescript-eslint/parser'
      },
      globals: {
        // Browser globals
        window: 'readonly',
        document: 'readonly',
        navigator: 'readonly',
        console: 'readonly',
        localStorage: 'readonly',
        confirm: 'readonly',
        setTimeout: 'readonly',
        clearTimeout: 'readonly',
        global: 'readonly',
        // DOM types
        IntersectionObserverInit: 'readonly',
        HTMLElementEventMap: 'readonly',
        WorkerGlobalScope: 'readonly',
        // Node globals
        process: 'readonly',
        Buffer: 'readonly',
        // Nuxt globals
        $fetch: 'readonly',
        useRoute: 'readonly',
        useRouter: 'readonly',
        useHead: 'readonly',
        useLazyAsyncData: 'readonly',
        useAuthStore: 'readonly',
        useApi: 'readonly',
        navigateTo: 'readonly',
        computed: 'readonly',
        ref: 'readonly',
        reactive: 'readonly',
        watch: 'readonly',
        onMounted: 'readonly',
        nextTick: 'readonly',
        defineNuxtConfig: 'readonly',
        defineNuxtPlugin: 'readonly',
        defineNuxtRouteMiddleware: 'readonly',
        definePageMeta: 'readonly',
        useNuxtApp: 'readonly',
        useRuntimeConfig: 'readonly',
        useDebounceFn: 'readonly'
      }
    },
    plugins: {
      vue: require('eslint-plugin-vue'),
      '@typescript-eslint': require('@typescript-eslint/eslint-plugin')
    },
    rules: {
      // Vue specific rules
      'vue/multi-word-component-names': 'off',
      'vue/no-multiple-template-root': 'off',
      'vue/script-setup-uses-vars': 'error',
      'vue/no-unused-vars': 'error',
      
      // TypeScript rules
      '@typescript-eslint/no-unused-vars': ['error', { 
        argsIgnorePattern: '^_',
        varsIgnorePattern: '^_'
      }],
      '@typescript-eslint/no-explicit-any': 'warn',
      
      // General rules
      'no-console': 'warn',
      'no-debugger': 'error',
      'prefer-const': 'error',
      'no-var': 'error',
      'no-undef': 'error'
    },
    files: ['**/*.vue', '**/*.ts', '**/*.js']
  }
]