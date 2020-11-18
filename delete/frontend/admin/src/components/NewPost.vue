<template>
  <div class="container ">
    <div class="new-post">
      <div class="column is-10 is-offset-1">
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

        <div class="field">
          <div class="control">
            <button @click="ppost" class="button is-link">Submit</button>
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
        post: {
          'title': '',
          'intro': '',
          'body': '',
          'html_body': '',
        },
      }
    },
    methods: {
      ppost() {
        const path = '/post/write';
        var data = this.post;
        console.log(data)
        this.$axios.post(path, data)
          .then(() => this.$router.push('/'))
      },
      changeData(value, render) {
        this.post.body = value;
        this.post.html_body = render;
      },
    },
  };

</script>

<style>
  .new-post {
    margin: 50px 30px;
  }

</style>
