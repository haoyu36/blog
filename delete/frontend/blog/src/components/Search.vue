<template>
  <div class="columns">
    <div class="column is-6 is-offset-3">

      <div class="search has-text-centered">
        <VueFuse placeholder="Search Blog" event-name="results" class="input is-medium is-primary" :list="posts" :keys="['title', 'body']" :findAllMatches=true :defaultAll=false />
      </div>

      <div class="total-search has-text-centered"> 共找到 <span class="search-count">{{ results.length }}</span> 篇相关文章</div>

      <v-posts v-bind:posts="results"></v-posts>
    </div>
  </div>
</template>


<script>
  import vPosts from '@/components/Posts'

  export default {
    data() {
      return {
        results: [],
        posts: []
      }
    },
    components: {
      vPosts
    },
    methods: {
      getposts: function() {
        const path = '/search';
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
      this.$on('results', results => {
        this.results = results
      })
    }
  }

</script>


<style scoped>
  .search {
    margin: 30px 35px;
  }

  .search-count {
    color: #42b983;
  }

  .total-search {
    color: #34495e;
    font-size: 19px;
    font-weight: bold;
  }
</style>
