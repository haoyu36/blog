<template>
  <div id="archives">
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
              <div class="columns">
                <div class="column is-8 is-offset-2">
                  <div class="timeline">
                    <div v-for="year in posts" :key="year[0]">
                      <header class="timeline-header">
                        <span class="tag is-medium is-primary">{{ year[0] }}</span>
                      </header>
                      <div v-for="post in year[1]" :key="post.id">
                        <div class="timeline-item is-primary">
                          <div class="timeline-marker is-primary"></div>
                          <div class="timeline-content">
                            <p class="data">
                              {{ post.created_at | moment("MM-DD") }} /
                              <router-link :to="`/post/${post.id}`">{{ post.title}}</router-link>
                            </p>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                  <header class="timeline-header">
                    <span class="tag is-medium is-primary">End</span>
                  </header>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
import { getarchives } from "@/api";
import AppHeader from "@/components/Header";

export default {
  components: {
    AppHeader
  },
  data() {
    return {
      posts: []
    };
  },
  methods: {
    Getarchives: function() {
      getarchives().then(res => {
        this.posts = res.data.archives;
      });
    }
  },
  created() {
    this.Getarchives();
  }
};
</script>

<style scoped>
.hero-body {
  background-position: center;
  background-size: cover;
  background-repeat: no-repeat;
  height: 500px;
  background-image: url(https://blog-1257629587.cos.ap-shanghai.myqcloud.com/carousel2.jpg);
}

a:link {
  color: rgb(48, 72, 96);
}

a:visited {
  color: rgb(48, 72, 96);
}

a:hover {
  color: rgb(0, 138, 115);
}

.data {
  color: rgb(48, 72, 96);
}
</style>