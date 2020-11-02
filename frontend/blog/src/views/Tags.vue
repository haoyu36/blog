<template>
  <div>
    <section class="hero is-info is-medium is-bold">
      <div class="hero-body"></div>
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
              <div class="columns is-centered">
                <div class="column is-8">
                  <ul v-for="tag in tags" v-bind:key="tag.id" class="tag-list-item">
                    <li>
                      <button class="button has-badge-rounded" :data-badge="tag.count">
                        <router-link :to="`/tags/${tag.id}`">{{ tag.name }}</router-link>
                      </button>
                    </li>
                  </ul>
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
import { gettags } from "@/api";
import AppHeader from "@/components/Header";

export default {
  components: {
    AppHeader
  },
  data() {
    return {
      tags: []
    };
  },
  methods: {
    Gettags() {
      gettags().then(res => {
        this.tags = res.data.tags;
      });
    }
  },
  created() {
    this.Gettags();
  }
};
</script>


<style scoped>
.hero-body {
  background-position: center;
  background-size: cover;
  background-repeat: no-repeat;
  height: 500px;
  background-image: url(https://blog-1257629587.cos.ap-shanghai.myqcloud.com/carousel6.jpg);
}

.tag-list-item {
  display: inline-block;
  height: 3.5rem;
  margin: 3px;
  padding: 0 10px;
  text-align: center;
  line-height: 30px;
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
</style>