<template>
  <div>
    <section class="hero is-info is-medium is-bold">
      <div class="hero-body pic">
        <div class="container has-text-centered">
          <h1 class="title">When threads sleep, do they dream?</h1>
        </div>
      </div>
    </section>
    <div class="container">
      <div class="columns">
        <div class="column is-8 is-offset-2">
          <div class="card article">
            <!-- <div v-html="post.toc" class="toc"></div> -->
            <div class="card-content">
              <div class="article-head has-text-centered">
                <p class="title article-title">{{ post.title }}</p>
                <div class="article-meta">
                  <span>{{ post.created_at | moment("YYYY-MM-DD") }}</span>
                  <span class="archive-seq">/</span>
                  <span v-for="tag in post.tags" v-bind:key="tag.id">
                    <router-link :to="`/tags/${tag.id}`" class="tag-list">{{ tag.name }}</router-link>
                  </span>
                </div>
              </div>
              <div class="content article-body">
                <div v-html="post.html" v-highlight></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
import { getpost } from "@/api";

export default {
  components: {},
  data() {
    return {
      post: {}
    };
  },
  methods: {
    Getpost: function() {
      getpost(this.$route.params.id).then(res => {
        this.post = res.data;
      });
    }
  },
  created() {
    this.Getpost();
  }
};
</script>

<style scoped>
.pic {
  background-image: url(https://blog-1257629587.cos.ap-shanghai.myqcloud.com/carousel4.jpg);
}

.hero-body {
  background-position: center;
  background-size: cover;
  background-repeat: no-repeat;
  height: 500px;
}

.toc {
  line-height: 1.9;
  margin: 0 auto;
  width: 20rem;
  padding-top: 2rem;
}

.article-title {
  font-size: 1.5rem;
  line-height: 2;
}

.article-body {
  line-height: 1.8;
  margin: 0 0.8rem;
}

.article-meta {
  color: rgb(144, 158, 159);
  margin: 2rem 0;
}

.tag-list {
  margin-right: 5px;
  color: #e96900 !important;
  padding: 2px 5px;
  background-color: #f8f8f8;
  border-radius: 2px;
  display: inline;
}
</style>

