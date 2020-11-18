<template>
  <div class="columns">
    <div class="column is-6 is-offset-3">
      <article class="post">
        <header class="has-text-centered">
          <div class="title">{{ post.title }}</div>
          <div class="post-meta">
            <span>{{ post.created_at | moment("YYYY-MM-DD") }}</span>
            <span class="post-seq">/</span>
            <span v-for="tag in post.tags" v-bind:key="tag.id">
              <router-link :to="`/tags/${tag.id}`" class="tag-list">{{ tag.name }}
              </router-link>
            </span>
          </div>
        </header>
        <div class="post-content" v-html="post.html_body" v-highlight>
        </div>
      </article>
    </div>
  </div>
</template>


<script>
  export default {
    data() {
      return {
        post: {},
      }
    },
    methods: {
      getpost: function() {
        const path = '/post/' + this.$route.params.id;
        this.$axios.get(path)
          .then((res) => {
            this.post = res.data;
          })
          .catch((error) => {
            this.$router.push('/notfound')
          });
      },
    },
    created() {
      this.getpost();
    },
  };

</script>


<style scoped>
  .post {
    margin: 30px 25px;
  }

  .title {
    font-size: 24px;
    font-weight: bold;
    color: rgb(48, 72, 96);
  }

  .post-meta {
    font-size: 14px;
    padding-top: 4px;
    color: rgb(144, 158, 159)
  }

  .tag-list {
    margin-right: 5px;
    color: #e96900 !important;
    padding: 2px 5px;
    background-color: #f8f8f8;
    border-radius: 2px;
    display: inline;
  }



  .post-content {
    margin-top: 20px;
    line-height: 2rem;
    font-size: 17px;
  }

  .post-seq {
    margin-left: 5px;
    margin-right: 3px;
  }

  a {
    color: #42b983;
  }
</style>
