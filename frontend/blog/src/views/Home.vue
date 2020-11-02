<template>
  <div id="home-page">
    <section class="hero is-fullheight is-light">
      <div class="hero-head">
        <nav class="navbar is-spaced" role="navigation" aria-label="main navigation">
          <div class="container">
            <div class="navbar-brand">
              <router-link to="/" class="navbar-item has-text-weight-semibold">首页</router-link>
              <router-link to="/posts" class="navbar-item has-text-weight-semibold">博客</router-link>
              <router-link to="/files" class="navbar-item has-text-weight-semibold">书籍</router-link>
              <router-link to="/tags" class="navbar-item has-text-weight-semibold">标签</router-link>
              <router-link to="/archives" class="navbar-item has-text-weight-semibold">归档</router-link>
            </div>
          </div>
        </nav>
      </div>

      <div class="hero-body">
        <div class="container">
          <h2 class="subtitle">
            <span
              class="has-text-centered is-block"
            >If the search has a result, it will automatically display</span>
          </h2>
          <div class="columns is-centered">
            <div class="column is-7">
              <div class="search-form">
                <form>
                  <div class="field has-addons has-shadow-field">
                    <div class="control has-icons-left is-expanded">
                      <VueFuse
                        placeholder="Search Blog"
                        event-name="results"
                        class="input is-large is-primary"
                        :list="posts"
                        :keys="[{name:'title', weigth:0.7}, {name:'body', weigth:0.3}]"
                        :findAllMatches="true"
                        :defaultAll="false"
                      />
                      <span class="icon is-small is-left">
                        <svg-icon icon-class="search"/>
                      </span>
                    </div>
                  </div>
                </form>
              </div>
              <div class="has-text-centered" v-show="results == false">
                <img class="m-t-50" src="../assets/home.png" alt="Find rentals">
              </div>
              <div>
                <div class="total-search has-text-centered m-t-50" v-show="results.length !== 0">
                  共找到
                  <span class="search-count">{{ results.length }}</span> 篇相关文章
                </div>
                <v-posts v-bind:posts="results"></v-posts>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <home-post/>
    <home-file/>
    <about/>
  </div>
</template>


<script>
import vPosts from "@/components/Posts";
import { getsearch } from "@/api";
import HomePost from "./components/homepost";
import HomeFile from "./components/homefile";
import About from "./components/about";

export default {
  name: "home",
  components: {
    HomePost,
    HomeFile,
    vPosts,
    About
  },
  data() {
    return {
      results: [],
      posts: []
    };
  },
  methods: {
    Getsearch: function() {
      getsearch().then(res => {
        this.posts = res.data.posts;
      });
    }
  },
  created() {
    this.Getsearch();
    this.$on("results", results => {
      this.results = results;
    });
  }
};
</script>


<style scoped>
.m-t-50 {
  margin-top: 50px;
}

.hero.is-light .subtitle {
  color: #99a6b3;
}

.search {
  margin: 30px 35px;
}

.search-count {
  color: #42b983;
}

.total-search {
  color: #34495e;
  font-size: 1.4rem;
  font-weight: bold;
  padding-bottom: 1rem;
}
</style>