<template>
  <div id="app">
    <app-header></app-header>
    <router-view/>
  </div>
</template>

<script>
import AppHeader from "@/components/Header";

export default {
  name: "App",
  components: {
    AppHeader
  }
};
</script>

<style>
a {
  color: #42b983;
  cursor: pointer;
}
</style>
