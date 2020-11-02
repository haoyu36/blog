<template>
  <div>
    <section class="hero is-info is-medium is-bold">
      <div class="hero-body pic">
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
                  @btnClick="Gettagposts"
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
import { gettagposts } from "@/api";
import vPosts from "@/components/Posts";
import AppHeader from "@/components/Header";

export default {
  inject: ["reload"],
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
    Gettagposts: function(n) {
      n = typeof n !== "undefined" ? n : 1;
      const path = "/api/tags/" + this.$route.params.id + "/" + n;
      gettagposts(path).then(res => {
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
  watch: {
    $route(to, from) {
      // 路由变化时重载页面
      this.reload();
    }
  },
  created() {
    this.Gettagposts();
  }
};
</script>


<style scoped>
.pic {
  background-image: url(https://blog-1257629587.cos.ap-shanghai.myqcloud.com/carousel5.jpg);
}

.hero-body {
  background-position: center;
  background-size: cover;
  background-repeat: no-repeat;
  height: 500px;
}
</style>