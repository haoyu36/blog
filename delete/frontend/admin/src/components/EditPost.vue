<template>
  <div class="columns">
    <div class="edit-post">
      <div class="column is-10 is-offset-1">
        <div class="form-post">
          <div class="field">
            <label class="label">Title</label>
            <div class="control">
              <input v-model="post.title" class="input" type="text" placeholder="Text input">
            </div>
          </div>

          <div class="field">
            <label class="label">Intro</label>
            <div class="control">
              <textarea v-model="post.intro" class="textarea" placeholder="Textarea"></textarea>
            </div>
          </div>


          <div class="field">
            <label class="label">Body</label>
            <div class="control">
              <mavon-editor v-model="post.body" @change="changeData" />
            </div>
          </div>

          <div class="field is-grouped">
            <div class="control">
              <button @click="putpost" class="button is-link">Submit</button>
            </div>
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
        post: {},
      }
    },

    methods: {
      getpost() {
        const path = '/post/' + this.$route.params.id;
        this.$axios.get(path)
          .then((res) => {
            this.post = res.data;
          })
          .catch((error) => {
            console.error(error);
          });

      },
      putpost() {
        const path = '/post/' + this.$route.params.id;
        this.$axios.put(path, this.post)
          .then(() => this.$router.push('/'))
      },
      changeData(value, render) {
        this.post.body = value;
        this.post.html_body = render;
      },
    },
    created() {
      this.getpost();
    },
  };

</script>

<style>
  .edit-post {
    margin: 50px 30px;
  }

</style>
