<template>
  <div class="container">
    <div class="columns login-from">
      <div class="column is-4 is-offset-4">
        <div class="field">
          <label class="label">Name</label>
          <div class="control">
            <input v-model="data.username" class="input" type="text" placeholder="Name input">
          </div>
        </div>

        <div class="field">
          <label class="label">Password</label>
          <div class="control">
            <input v-model="data.password" class="input" type="password" placeholder="Password input">
          </div>
        </div>

        <div class="field is-grouped">
          <div class="control">
            <button @click="submitForm" class="button is-primary">Submit</button>
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
        data: {
          username: '',
          password: ''
        },
      }
    },
    methods: {
      submitForm() {
        const path = '/tokens'
        this.$axios.post(path, {}, {
            auth: this.data
          })
          .then((response) => {
            window.localStorage.setItem('madblog-token', response.data.token)

            if (typeof this.$route.query.redirect == 'undefined') {
              this.$router.push('/')
            } else {
              this.$router.push(this.$route.query.redirect)
            }
          })
          .catch((error) => {
            console.log('failed', error.response);
          })
      },
    },
  };

</script>



<style scoped>
  .login-from {
    margin: 50px 35px;
  }
</style>
