<template>
  <post-detail :is-edit="true"/>
</template>

<script>
import PostDetail from './PostDetail'

export default {
  name: 'EditPostForm',
  components: { PostDetail }
}
</script>
