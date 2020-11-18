<template>
  <div>
    <div class="columns">
      <div class="column is-6 is-offset-3">
        <ul class="tag-sty">
          <li v-for="tag in tags" v-bind:key="tag.id" class="tag-list-item">
            <router-link :to="`/tags/${tag.id}`">{{ tag.name }}<span class="tag-count">{{ tag.count}}</span>
            </router-link>
          </li>
        </ul>
      </div>

    </div>
  </div>
</template>



<script>
  export default {
    data() {
      return {
        tags: [],
      }
    },
    methods: {
      gettags() {
        const path = '/tags';
        this.$axios.get(path)
          .then((res) => {
            this.tags = res.data.tags;
          })
          .catch((error) => {
            this.$router.push('/notfound')
          });
      },
    },
    created() {
      this.gettags();
    },
  };
</script>


<style scoped>
  .tag-sty {
    margin: 40px 35px;
  }

  .tag-list-item {
    line-height: 16px;
    display: inline-block;
    height: 20px;
    margin: 3px;
    padding: 0 10px;
    border-radius: 3px;
    background: #f6f6f6;
    min-width: 30px;
    font-size: 16px;
    text-align: center;
    line-height: 30px;
    height: 30px;
    color: #2196F3;
  }

  .tag-count {
    color: #e96900;
    margin-left: 5px;
  }
    
  a {
    color: #42b983;
  }

</style>