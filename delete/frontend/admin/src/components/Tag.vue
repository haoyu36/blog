<template>
  <div class="container tag-sele">
    <br>

    <div class="field">
      <label class="label">Tag</label>
      <div class="control">
        <multiselect v-model="data.tags" tag-placeholder="Add this as new tag" placeholder="Search or add a tag" :options="options" :multiple="true" :taggable="true" :searchable="true" @tag="addTag">
        </multiselect>
      </div>
    </div>

    <button @click="putpost" class="button is-danger">提交</button>
  </div>
</template>


<script>
  export default {
    data() {
      return {
        data: {},
        options: [],
      }
    },

    methods: {
      getpost() {
        const path = '/posttag/' + this.$route.params.id;
        this.$axios.get(path)
          .then((res) => {
            this.data = res.data;
          })
          .catch((error) => {
            console.error(error);
          });

      },
      gettags() {
        const path = '/tags';
        this.$axios.get(path)
          .then((res) => {
            this.options = res.data.tags;
          })
          .catch((error) => {
            console.error(error);
          });
      },
      putpost() {
        const path = '/posttag/' + this.$route.params.id;

        this.$axios.post(path, this.data)
          .then(() => this.$router.push('/'))
      },
      addTag(tag) {
        this.options.push(tag);
        this.post.tags.push(tag)
      },
    },
    created() {
      this.getpost();
      this.gettags();
    },
  };

</script>

<style src="../assets/vue-multiselect.min.css">
  .tag-sele {
    margin: 30px, 35px;
  }

</style>
