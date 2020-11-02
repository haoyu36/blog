<template>
  <div id="app">
    <router-view v-if="isRouterAlive"/>
    <BackTop></BackTop>
  </div>
</template>


<script>
import BackTop from "@/components/BackTop";

export default {
  name: "App",
  components: {
    BackTop
  },
  provide() {
    return {
      reload: this.reload
    };
  },
  data() {
    return {
      isRouterAlive: true
    };
  },
  methods: {
    reload() {
      this.isRouterAlive = false;
      this.$nextTick(() => (this.isRouterAlive = true));
    }
  }
};
</script>


<style>
#app {
  font-family: sans-serif;
  font-size: 16px;
  background: #f0f2f4;
}

.article {
  margin-top: -200px;
}

.article-head {
  margin: 0 auto;
  width: 19rem;
  padding-top: 2rem;
}

.archive-seq {
  margin: 0 5px;
}
</style>