<template>
  <div class="post-list">
    <div class="columns">
      <div class="column is-4 is-offset-4">
        <table class="table">
          <thead>
            <tr>
              <th>id</th>
              <th>title</th>
              <th>Tag</th>
              <th>Delete</th>
            </tr>
          </thead>
          <tbody v-for="post in posts" v-bind:key="post.id">
            <tr>
              <td>{{ post.id }}</td>
              <td>
                <router-link :to="`/post/${post.id}`">{{ post.title}}</router-link>
              </td>
              <td>
                <router-link :to="`/tag/${post.id}`">Tag</router-link>
              </td>
              <td>
                <a @click="deletepost(post.id)">delete</a>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <div class="container has-text-centered">
      <vue-paginate-al :totalPage="pages" @btnClick="getposts"></vue-paginate-al>
    </div>
  </div>
</template>



<script>
export default {
  data() {
    return {
      posts: [],
      pages: 0
    };
  },
  methods: {
    getposts: function(n) {
      n = typeof n !== "undefined" ? n : 1;
      const path = "/api/posts/" + n;
      this.$axios
        .get(path)
        .then(res => {
          this.posts = res.data.posts;
          this.pages = res.data.total_pages;
        })
        .catch(error => {
          this.$router.push("/notfound");
        });
    },
    deletepost(id) {
      const path = "/post/" + id;
      this.$axios.delete(path).then(() => this.$router.go(0));
    }
  },
  created() {
    this.getposts();
  }
};
</script>



<style>
.post-list {
  margin: 50px 35px;
}
</style>
