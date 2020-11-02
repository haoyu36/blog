<template>
  <div class="createFile-container">
    <el-form class="form-container">
      <el-row>
        <el-col :span="12" :offset="6">
          <el-form-item label="Author">
            <el-input type="text" v-model="author"></el-input>
          </el-form-item>
        </el-col>
      </el-row>

      <el-row>
        <el-col :span="12" :offset="6">
          <el-form-item label="Intro">
            <el-input type="text" v-model="intro"></el-input>
          </el-form-item>
        </el-col>
      </el-row>

      <el-row>
        <el-col :span="12" :offset="6">
          <el-form-item label="书籍PDF文件">
            <br>
            <input type="file" @change="getFile($event)">
          </el-form-item>
        </el-col>
      </el-row>

      <el-row>
        <el-col :span="12" :offset="6">
          <el-form-item label="图片预览">
            <br>
            <input type="file" @change="getPic($event)">
          </el-form-item>
        </el-col>
      </el-row>

      <el-row>
        <el-col :span="12" :offset="6">
          <el-form-item>
            <el-button type="primary" v-loading="loading" @click="submitForm()">提交</el-button>
          </el-form-item>
        </el-col>
      </el-row>
    </el-form>
  </div>
</template>

<script>
import { uploadFile } from "@/api";

export default {
  name: "CreateFileForm",
  data() {
    return {
      author: "",
      intro: "",
      loading: false
    };
  },
  methods: {
    getFile(event) {
      this.file = event.target.files[0];
    },
    getPic(event) {
      this.pic = event.target.files[0];
    },
    submitForm() {
      this.loading = true;
      let formData = new FormData();
      formData.append("author", this.author);
      formData.append("intro", this.intro);
      formData.append("file", this.file);
      formData.append("pic", this.pic);

      uploadFile(formData)
        .then(response => {
          this.$message({
            type: "success",
            message: response.data.message
          });
          this.loading = false;
          this.$router.push("/file/list?refresh=1");
        })
        .catch(err => {
          console.log(err);
        });
    }
  }
};
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
@import "~@/styles/mixin.scss";
.createFile-container {
  position: relative;
  .createFile-main-container {
    padding: 40px 45px 20px 50px;
  }
}
</style>
