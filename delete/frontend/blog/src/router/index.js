import Vue from 'vue'
import Router from 'vue-router'
import Tags from '@/components/Tags'
import Home from '@/components/Home'
import Post from '@/components/Post'
import TagPost from '@/components/TagPost'
import Search from '@/components/Search'
import Archives from '@/components/Archives'
import Books from '@/components/Books'
import About from '@/components/About'
import NotFound from '@/components/NotFound'


Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home
    },{
      path: '/post/:id',
      name: 'Post',
      component: Post
    },{
      path: '/tags',
      name: 'Tags',
      component: Tags
    },{
      path: '/tags/:id/:page',
      name: 'TagPost',
      component: TagPost
    },{ 
      path: '/tags/:id', 
      redirect: '/tags/:id/1' 
    },{
      path: '/search',
      name: 'Search',
      component: Search
    },{
      path: '/archives',
      name: 'Archives',
      component: Archives
    },{
      path: '/books',
      name: 'Books',
      component: Books
    },{
      path: '/about',
      name: 'About',
      component: About
    },{
      path: '*',
      name: 'NotFound',
      component: NotFound
    },
  ]
})