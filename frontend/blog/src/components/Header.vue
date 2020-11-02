<template>
  <nav class="navbar is-spaced" role="navigation" aria-label="main navigation">
    <div class="container">
      <div class="navbar-brand">
        <router-link to="/" class="navbar-item button has-text-weight-semibold">首页</router-link>
        <router-link to="/posts" class="navbar-item button has-text-weight-semibold">博客</router-link>
        <router-link to="/files" class="navbar-item button has-text-weight-semibold">书籍</router-link>
        <router-link to="/tags" class="navbar-item button has-text-weight-semibold">标签</router-link>
        <router-link to="/archives" class="navbar-item button has-text-weight-semibold">归档</router-link>
      </div>
    </div>
  </nav>
</template>


<style scoped>
a:hover {
  color: rgb(0, 138, 115);
}

a:link {
  color: rgb(48, 72, 96);
}

</style>
