<template>
  <section class="hero is-fullheight has-text-centered has-background-white">
    <div class="hero-body">
      <div class="container">
        <h1 class="title">Recent Blogs</h1>
        <br>
        <div class="columns is-centered">
          <div class="column is-10">
            <div class="columns is-multiline">
              <div class="column is-one-third">
                <div class="card rb-card">
                  <div class="card-image">
                    <figure class="image is-4by3">
                      <img
                        src="https://blog-1257629587.cos.ap-shanghai.myqcloud.com/posts1.jpeg"
                        alt="this is picture"
                      >
                    </figure>
                  </div>
                  <div class="card-content">
                    <router-link :to="`/post/${p1.id}`" class="posts-title">{{ p1.title }}</router-link>
                    <p class="posts-subtitle">{{ p1.intro }}</p>
                  </div>
                </div>
              </div>
              <div class="column is-one-third">
                <div class="card rb-card">
                  <div class="card-image">
                    <figure class="image is-4by3">
                      <img
                        src="https://blog-1257629587.cos.ap-shanghai.myqcloud.com/posts2.jpeg"
                        alt="this is picture"
                      >
                    </figure>
                  </div>
                  <div class="card-content">
                    <router-link :to="`/post/${p2.id}`" class="posts-title">{{ p2.title }}</router-link>
                    <p class="posts-subtitle">{{ p2.intro }}</p>
                  </div>
                </div>
              </div>
              <div class="column is-one-third">
                <div class="card rb-card">
                  <div class="card-image">
                    <figure class="image is-4by3">
                      <img
                        src="https://blog-1257629587.cos.ap-shanghai.myqcloud.com/posts3.jpeg"
                        alt="this is picture"
                      >
                    </figure>
                  </div>
                  <div class="card-content">
                    <router-link :to="`/post/${p3.id}`" class="posts-title">{{ p3.title }}</router-link>
                    <p class="posts-subtitle">{{ p3.intro }}</p>
                  </div>
                </div>
              </div>

              <div class="container">
                <div class="has-text-centered">
                  <p class="m-t-50">
                    <router-link
                      to="/posts"
                      class="button is-medium is-shadowy is-primary"
                    >Learn more</router-link>
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>


<script>
import { gethomepost } from "@/api";

export default {
  name: "homepost",
  data() {
    return {
      p1: {},
      p2: {},
      p3: {}
    };
  },
  methods: {
    Gethomepost: function() {
      gethomepost().then(res => {
        this.p1 = res.data.posts[0];
        this.p2 = res.data.posts[1];
        this.p3 = res.data.posts[2];
      });
    }
  },
  created() {
    this.Gethomepost();
  }
};
</script>



<style scoped>
.posts-title {
  font-size: 1.15em;
}

.posts-subtitle {
  font-size: 1em;
  line-height: 1.8;
  margin-top: 1rem;
}

.rb-card {
  border: none;
  border-radius: 4px;
  box-shadow: 5px 5px 16px 0 rgba(0, 0, 0, 0.13);
  cursor: pointer;
  transition: all 0.2s ease-in-out;
  /* position: relative; */
  overflow: hidden;
}

.rb-card:hover {
  transform: scale(1.05);
}

.m-t-50 {
  margin-top: 50px !important;
}

a {
  color: rgb(0, 138, 115);
}
</style>
