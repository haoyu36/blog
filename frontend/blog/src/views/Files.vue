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
              <div class="columns">
                <div class="column is-8 is-offset-2">
                  <div v-for="file in files" v-bind:key="file.id" class="sin-file">
                    <div class="fil-title">{{ file.filename }}</div>

                    <div class="fil-meta">
                      {{ file.size }}
                      <span class="book-seq">/</span>
                      <a :href="file.file_url">下载</a>
                    </div>
                  </div>
                </div>
              </div>
              <div class="has-text-centered">
                <vue-paginate-al
                  :totalPage="pages"
                  customActiveBGColor="#42b983"
                  @btnClick="Getfiles"
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
import { getfiles } from "@/api";
import AppHeader from "@/components/Header";

export default {
  data() {
    return {
      files: [],
      pages: 0
    };
  },
  components: {
    AppHeader
  },
  methods: {
    Getfiles: function(n) {
      n = typeof n !== "undefined" ? n : 1;
      getfiles(n).then(res => {
        this.files = res.data.files;
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
    this.Getfiles();
  }
};
</script>


<style scoped>
.hero-body {
  background-position: center;
  background-size: cover;
  background-repeat: no-repeat;
  height: 500px;
  background-image: url(https://blog-1257629587.cos.ap-shanghai.myqcloud.com/carousel3.jpg);
}

.fil-title {
  font-weight: bold;
  color: rgb(48, 72, 96);
}

.fil-meta {
  font-size: 0.9rem;
  padding-top: 4px;
  color: rgb(144, 158, 159);
}

.sin-file {
  padding-top: 20px;
}

a {
  color: #42b983;
}

.book-seq {
  margin-left: 5px;
  margin-right: 5px;
}
</style>