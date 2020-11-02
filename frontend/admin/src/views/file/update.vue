<template>
  <div class="updateFile-container">
    <el-form ref="fileForm" :model="fileForm" class="form-container">
      <sticky class-name="sub-navbar draft">
        <el-button
          v-loading="loading"
          style="margin-left: 10px;"
          type="success"
          @click="submitForm"
        >提交</el-button>
      </sticky>

      <div class="updateFile-main-container">
        <el-row>
          <el-col :span="24">
            <el-form-item style="margin-bottom: 20px;" prop="title">
              <MDinput v-model="fileForm.author" :maxlength="100" name="author" required>Author</MDinput>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row>
          <el-col :span="24">
            <el-form-item style="margin-bottom: 20px;" prop="title">
              <MDinput v-model="fileForm.intro" :maxlength="500" name="intro" required>Intro</MDinput>
            </el-form-item>
          </el-col>
        </el-row>
      </div>
    </el-form>
  </div>
</template>

<script>
import MDinput from "@/components/MDinput";
import Sticky from "@/components/Sticky";
import { fetchFile, updateFile } from "@/api";

export default {
  name: "FileUpdate",
  components: { MDinput, Sticky },
  data() {
    return {
      fileForm: {
        id: "",
        author: "",
        intro: ""
      },
      loading: false
    };
  },
  created() {
    this.fetchData(this.$route.params.id);
  },
  methods: {
    fetchData(id) {
      fetchFile(id)
        .then(res => {
          this.fileForm.id = res.data.id;
          this.fileForm.author = res.data.author;
          this.fileForm.intro = res.data.intro;
        })
        .catch(err => {
          console.log(err);
        });
    },
    submitForm() {
      updateFile(this.fileForm)
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
.updateFile-container {
  position: relative;
  .updateFile-main-container {
    padding: 40px 45px 20px 50px;
  }
}
</style>
