<template>
  <div class="columns">
    <div class="column is-6 is-offset-3">

      <div class="file upload">
        <label class="file-label">
          <input class="file-input" type="file" name="resume" @change="uploadConfig">

          <span class="file-cta">
            <span class="file-label">
              Choose a file…
            </span>
          </span>
        </label>
      </div>
    </div>
  </div>
</template>


<script>

  export default {
    data() {
      return {};
    },
    methods: {
      uploadConfig(e) {
        let formData = new FormData();
        formData.append('file', e.target.files[0]);
        let url = '/upload';
        let config = {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        };
        this.$axios.post(url, formData, config).then(function(response) {
          alert(response.data)
        })
      }
    },
  };

</script>



<style>
  .upload {
    margin: 100px 100px;
  }
</style>
