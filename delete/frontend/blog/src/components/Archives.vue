<template>
  <div class="columns">
    <div class="column is-6 is-offset-3">
      <div v-for="mon in posts" :key="mon.month" class="mon-posts">
        <div class="mon-header">
          <span class="month">{{ mon.month }}</span>
        </div>
        <div v-for="post in mon.posts" :key="post.id" class="post-item">
          {{ post.created_at | moment("MM-DD") }}<span class="archive-seq">/</span>
          <router-link :to="`/post/${post.id}`">{{ post.title}}</router-link>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
  export default {
    data() {
      return {
        posts: [],
      }
    },
    methods: {
      getposts() {
        const path = '/archives';
        this.$axios.get(path)
          .then((res) => {
            this.posts = res.data.posts;
          })
          .catch((error) => {
            this.$router.push('/notfound')
          });
      },
    },
    created() {
      this.getposts();
    },
  };

</script>



<style scoped>
  .mon-posts {
    margin: 30px 15px;
  }

  .post-item {
    margin-top: 3px;
    margin-left: 15px;
    font-size: 16px;
    color: #34495e;
  }

  .month {
    margin-left: 10px;
    margin-bottom: 10px;
    font-size: 24px;
    color: #34495e;
    font-weight: bold;
  }

  a {
    color: #42b983;
  }

  .archive-seq {
    margin-left: 5px;
    margin-right: 5px;
  }

</style>
