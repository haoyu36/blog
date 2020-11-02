<template>
  <div>
    <section class="hero is-info is-medium is-bold">
      <div class="hero-body">
      </div>
    </section>
    <div class="container">
      <div class="columns">
        <div class="column is-8 is-offset-2">
          <div class="card article">
            <section class="hero article-head">
              <div class="hero-head">
                <app-header></app-header>
              </div>
            </section>
            <div class="card-content">
              <v-posts v-bind:posts="posts"></v-posts>
              <div class="has-text-centered">
                <vue-paginate-al
                  :totalPage="pages"
                  customActiveBGColor="#42b983"
                  @btnClick="Getposts"
                ></vue-paginate-al>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>



<script>
import { getposts } from "@/api";
import vPosts from "@/components/Posts";
import AppHeader from "@/components/Header";

export default {
  data() {
    return {
      posts: [],
      pages: 0
    };
  },
  components: {
    vPosts,
    AppHeader
  },
  methods: {
    Getposts: function(n) {
      n = typeof n !== "undefined" ? n : 1;
      getposts(n).then(res => {
        this.posts = res.data.posts;
        this.pages = res.data.total_pages;
        this.backTop();
      });
    },
    backTop() {
      document.body.scrollTop = 0;
      document.documentElement.scrollTop = 0;
    }
  },
  created() {
    this.Getposts();
  }
};
</script>


<style scoped>
.hero-body {
  background-position: center;
  background-size: cover;
  background-repeat: no-repeat;
  height: 500px;
  background-image: url(https://blog-1257629587.cos.ap-shanghai.myqcloud.com/carousel1.jpg);
}

.hero-body {
  background-position: center;
  background-size: cover;
  background-repeat: no-repeat;
  height: 500px;
}
</style>