<template>
  <section class="hero is-primary">
    <div class="hero-foot">
      <nav class="tabs">
        <ul>
          <li>
            <router-link to="/"><strong>Home</strong></router-link>
          </li>
          <li>
            <router-link to="/newpost"><strong>NewPost</strong></router-link>
          </li>
          <li>
            <router-link to="/files"><strong>Files</strong></router-link>
          </li>
          <li>
            <router-link to="/upload"><strong>Upload</strong></router-link>
          </li>
          <li>
            <router-link to="/login"><strong>Login</strong></router-link>
          </li>
          <li>
            <a @click="handlerLogout"><strong>Logout</strong></a>
          </li>
        </ul>
      </nav>
    </div>
  </section>
</template>


<script>

  export default {
    methods: {
      handlerLogout(e) {
        window.localStorage.removeItem('madblog-token')
        this.$router.push('/login')
      }
    }
  };

</script>
