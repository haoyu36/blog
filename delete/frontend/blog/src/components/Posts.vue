<template>
  <div class="blog-posts">
    <div v-for="post in posts"  v-bind:key="post.id">
      <article class="posts-item">
        <div class="post-title">
          <router-link :to="`/post/${post.id}`">{{ post.title}}</router-link>
        </div>

        <div class="post-meta">
          {{ post.created_at | moment("YYYY-MM-DD") }}
          <span class="posts-seq">/</span>
          <span v-for="tag in post.tags" :key="tag.id">
            <router-link :to="`/tags/${tag.id}`" class="tag-list">{{ tag.name }}
            </router-link>
          </span>
        </div>

        <div class="post-excerpt">{{ post.intro }}</div>
        <div class="more">
          <router-link :to="`/post/${post.id}`">Read more</router-link>
        </div>
      </article>
      <hr>
    </div>
  </div>
</template>


<script>
  export default {
    props: ['posts']
  };
</script>



<style scoped>
  .blog-posts {
    margin: 30px 35px;
  }

  .posts-item {
    padding: 5px 0;
  }

  .post-title {
    font-size: 18px;
    font-weight: bold;
  }

  .post-title a {
    color: rgb(48, 72, 96);
  }

  .post-title a:hover {
    color: #42b983;
  }

  .post-excerpt {
    margin-top: 2px;
    font-size: 16px;
    line-height: 1.8rem;
    color: #34495e;
  }

  .post-meta {
    font-size: 14px;
    min-height: 30px;
    padding-top: 4px;
    color: rgb(144, 158, 159);
  }

  .tag-list {
    margin-right: 5px;
    color: #e96900 !important;
    padding: 0 5px;
    background-color: #f8f8f8;
    border-radius: 2px;
    display: inline;
  }

  .more {
    margin-top: 3px;
    font-size: 16px;
    font-weight: bold;
  }

  a {
    color: #42b983;
  }

  .posts-seq {
    margin-left: 5px;
    margin-right: 5px;
  }
</style>
