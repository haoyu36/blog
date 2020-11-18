<template>
  <section class="hero is-primary">
    <div class="hero-foot">
      <span class="has-text-centered">
        <span class="title-item">
          <router-link to="/"><strong>首页</strong></router-link>
        </span>
        <span class="title-item">
          <router-link to="/books"><strong>文件</strong></router-link>
        </span>
        <span class="title-item">
          <router-link to="/tags"><strong>分类</strong></router-link>
        </span>
        <span class="title-item">
          <router-link to="/archives"><strong>归档</strong></router-link>
        </span>
        <span class="title-item">
          <router-link to="/search"><strong>搜索</strong></router-link>
        </span>
        <span class="title-item">
          <router-link to="/about"><strong>关于</strong></router-link>
        </span>
      </span>
    </div>
  </section>
</template>


<style scoped>
  .title-item {
    padding-left: 10px;
    font-size: 18px;
    font-weight: bold;
  }

</style>
