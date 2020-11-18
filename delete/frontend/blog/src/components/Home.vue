<template>
  <div class="columns">
    <div class="column is-8 is-offset-2">
      <v-posts v-bind:posts="posts"></v-posts>
      <div class="has-text-centered">
        <vue-paginate-al :totalPage="pages" @btnClick="getposts"></vue-paginate-al>
      </div>
    </div>
  </div>
</template>


<script>
  import vPosts from '@/components/Posts'

  export default {
    data() {
      return {
        posts: [],
        pages: 0,
      }
    },
    components: {
      vPosts,
    },
    methods: {
      getposts: function(n) {
        n = typeof n !== 'undefined' ? n : 1;
        const path = '/posts/' + n;
        this.$axios.get(path)
          .then((res) => {
            this.posts = res.data.posts;
            this.pages = res.data.pages;
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