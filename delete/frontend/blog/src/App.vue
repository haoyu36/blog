<template>
  <div id="app">
    <app-header></app-header>
    <router-view v-if="isRouterAlive" />
    <app-footer></app-footer>
  </div>
</template>


<script>
  import AppHeader from '@/components/Header'
  import AppFooter from '@/components/footer'

  export default {
    name: 'App',
    components: {
      AppHeader,
      AppFooter,
    },
    provide() {
      return {
        reload: this.reload
      }
    },
    data() {
      return {
        isRouterAlive: true
      }
    },
    methods: {
      reload() {
        this.isRouterAlive = false
        this.$nextTick(() => (this.isRouterAlive = true))
      }
    }
  }

</script>


<style>
  pre {
    line-height: 1.2rem;
  }

  h1,h2 {
    margin: 20px 0 !important;
  }

  h3,h4,h5,h6 {
    margin: 10px 0 !important;
  }

  p {
    padding: 10px 0 !important;
  }

</style>
