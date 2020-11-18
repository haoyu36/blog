<template>
  <div class="columns">
    <div class="column is-6 is-offset-3">
      <div class="allfiles">
        <div v-for="file in files" v-bind:key="file.name" class="sin-file">
          <div class="fil-title">{{ file.name }}</div>

          <div class="fil-meta">
            {{ file.size}}
            <span class="book-seq">/</span>
            <a @click="download(file.name)">下载</a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>



<script>
export default {
  data() {
    return {
      files: []
    };
  },
  components: {},

  methods: {
    getfiles: function() {
      const path = "/files";
      this.$axios
        .get(path)
        .then(res => {
          this.files = res.data.files;
        })
        .catch(error => {
          this.$router.push("/notfound");
        });
    },
    download: function(name) {
      const path = "/download/" + name;
      this.$axios.get(path).then(res => {
        window.location.href = res.data.url;
      });
    }
  },
  created() {
    this.getfiles();
  }
};
</script>


<style scoped>
.allfiles {
  margin: 30px 35px;
}

.fil-title {
  font-size: 16px;
  font-weight: bold;
  color: rgb(48, 72, 96);
}

.fil-meta {
  font-size: 14px;
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
