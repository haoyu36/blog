<template>
  <div class="file-list">
    <div class="columns">
      <div class="column is-4 is-offset-4">
        <table class="table">
          <thead>
            <tr>
              <th>id</th>
              <th>title</th>
              <th>Delete</th>
            </tr>
          </thead>
          <tbody v-for="file in files" v-bind:key="file.id">
            <tr>
              <td>{{ file.id }}</td>
              <td>{{ file.name}}</td>
              <td><a @click="deletepost(file.id)">delete</a></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>



<script>
  export default {
    data() {
      return {
        files: [],
      };
    },
    methods: {
      getfiles: function() {
        const path = '/files';
        this.$axios.get(path)
          .then((res) => {
            this.files = res.data.files;
          })
          .catch((error) => {
            this.$router.push('/notfound')
          });
      },
      deletepost(id) {
        const path = '/delete/' + id;
        this.$axios.get(path)
          .then(() => this.$router.go(0))
      },
    },
    created() {
      this.getfiles();
    },
  };

</script>



<style>
  .file-list {
    margin: 50px 35px;
  }

</style>
