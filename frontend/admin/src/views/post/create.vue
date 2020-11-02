<template>
  <post-detail :is-edit="false"/>
</template>

<script>
import PostDetail from './PostDetail'

export default {
  name: 'CreatePostForm',
  components: { PostDetail }
}
</script>
