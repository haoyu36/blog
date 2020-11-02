import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

export default new Router({
  // base: process.env.BASE_URL,
  routes: [{
    path: '/',
    name: 'Home',
    component: () => import('./views/Home.vue')
  }, {
    path: '/post/:id',
    name: 'Post',
    component: () => import('./views/Post.vue')
  }, {
    path: '/tags',
    name: 'Tags',
    component: () => import('./views/Tags.vue')
  }, {
    path: '/archives',
    name: 'Archives',
    component: () => import('./views/Archives.vue')
  }, {
    path: '/posts',
    name: 'Posts',
    component: () => import('./views/AllPosts.vue')
  }, {
    path: '/tags/:id/:page',
    name: 'TagPosts',
    component: () => import('./views/TagPosts.vue')
  }, {
    path: '/tags/:id',
    redirect: '/tags/:id/1'
  }, {
    path: '/files',
    name: 'Files',
    component: () => import('./views/Files.vue')
  }, {
    path: '*',
    name: 'NotFound',
    component: () => import('./views/NotFound.vue')
  }]
})