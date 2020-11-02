
<template>
  <section class="hero  has-text-centered is-fullheight is-light">
    <div class="hero-body">
      <div class="container">
        <h1 class="title">Recent Books</h1>
        <br>
        <div class="columns is-centered">
          <div class="column is-10">
            <div class="columns is-multiline">
              <div class="column is-one-third" v-for="file in files" :key="file.id">
                <div class="card rb-card">
                  <div class="card-image">
                    <figure class="image is-3by4">
                      <img :src="file.pic_url" alt="this is picture">
                    </figure>
                  </div>
                </div>
              </div>

              <div class="container">
                <div class="has-text-centered">
                  <p class="m-t-50">
                    <router-link
                      to="/files"
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
import { gethomefile } from "@/api";

export default {
  name: "homefile",
  data() {
    return {
      files: []
    };
  },
  methods: {
    GethomeFile: function() {
      gethomefile().then(res => {
        this.files = res.data.files;
      });
    }
  },
  created() {
    this.GethomeFile();
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
  position: relative;
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




