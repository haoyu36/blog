<template>
  <div class="createPost-container">
    <el-form ref="postForm" :model="postForm" class="form-container">
      <sticky class-name="sub-navbar draft">
        <el-button
          v-loading="loading"
          style="margin-left: 10px;"
          type="success"
          @click="submitForm"
        >提交</el-button>
      </sticky>

      <div class="createPost-main-container">
        <el-row>
          <el-col :span="24">
            <el-form-item style="margin-bottom: 20px;" prop="title">
              <MDinput v-model="postForm.title" :maxlength="100" name="title" required>Title</MDinput>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row>
          <el-col :span="24">
            <el-form-item style="margin-bottom: 20px;" prop="title">
              <MDinput v-model="postForm.intro" :maxlength="100" name="intro" required>Intro</MDinput>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row>
          <el-col :span="12">
            <el-form-item label-width="45px" label="标签:" class="postInfo-container-item">
              <el-select
                v-model="postForm.tag_lst"
                multiple
                filterable
                allow-create
                placeholder="搜索标签"
              >
                <el-option
                  v-for="(item,index) in tagListOptions"
                  :key="item+index"
                  :label="item"
                  :value="item"
                />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row>
          <markdown-editor
            ref="markdownEditor"
            v-model="postForm.body"
            :options="{hideModeSwitch:true,previewStyle:'tab'}"
            height="500px"
          />
        </el-row>
      </div>
    </el-form>
  </div>
</template>

<script>
import MarkdownEditor from "@/components/MarkdownEditor";
import MDinput from "@/components/MDinput";
import Sticky from "@/components/Sticky";
import { fetchPost, updatePost, fetchTags } from "@/api";

export default {
  name: "PostDetail",
  components: { MarkdownEditor, MDinput, Sticky },
  props: {
    isEdit: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      postForm: {
        title: "",
        intro: "",
        body: "",
        tag_lst: []
      },
      loading: false,
      tagListOptions: [],
      tempRoute: {}
    };
  },
  created() {
    if (this.isEdit) {
      const id = this.$route.params && this.$route.params.id;
      this.fetchData(id);
    }
    this.tempRoute = Object.assign({}, this.$route);

    fetchTags()
      .then(response => {
        this.tagListOptions = response.data.tags;
      })
      .catch(err => {
        console.log(err);
      });
  },
  methods: {
    fetchData(id) {
      fetchPost(id)
        .then(res => {
          this.postForm.title = res.data.title;
          this.postForm.intro = res.data.intro;
          this.postForm.body = res.data.body;
          this.postForm.tag_lst = res.data.tag_lst;
          this.setTagsViewTitle();
        })
        .catch(err => {
          console.log(err);
        });
    },
    setTagsViewTitle() {
      const title = "编辑文章";
      const route = Object.assign({}, this.tempRoute, {
        title: `${title}-${this.postForm.id}`
      });
      this.$store.dispatch("updateVisitedView", route);
    },
    submitForm() {
      this.$refs.postForm.validate(valid => {
        if (valid) {
          this.loading = true;
          if (this.isEdit) {
            this.postForm.id = this.$route.params.id;
          }
          let self = this;
          updatePost(this.postForm)
            .then(response => {
              this.$message({
                type: "success",
                message: response.data.message
              });
              this.loading = false;
              this.$router.push("/post/list?refresh=1");
            })
            .catch(err => {
              console.log(err);
            });
        } else {
          console.log("error submit!!");
          return false;
        }
      });
    }
  }
};
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
@import "~@/styles/mixin.scss";
.createPost-container {
  position: relative;
  .createPost-main-container {
    padding: 40px 45px 20px 50px;
  }
}
</style>
