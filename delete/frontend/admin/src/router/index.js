import Vue from 'vue'
import Router from 'vue-router'
import EditPost from '@/components/EditPost'
import NewPost from '@/components/NewPost'
import Home from '@/components/Home'
import Login from '@/components/Login'
import Tag from '@/components/Tag'
import Upload from '@/components/Upload'
import Files from '@/components/Files'
import NotFound from '@/components/NotFound'


Vue.use(Router)

const router = new Router({
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home,
      // meta: {
      //   requiresAuth: true
      // }
    },{
      path: '/post/:id',
      name: 'EditPost',
      component: EditPost,
      // meta: {
      //   requiresAuth: true
      // }
    },{
      path: '/newpost',
      name: 'NewPost',
      component: NewPost,
      // meta: {
      //   requiresAuth: true
      // }
    },{
      path: '/login',
      name: 'Login',
      component: Login
    },{
      path: '/tag/:id',
      name: 'Tag',
      component: Tag,
      // meta: {
      //   requiresAuth: true
      // }
    },{
      path: '/upload',
      name: 'Upload',
      component: Upload,
      // meta: {
      //   requiresAuth: true
      // }
    },{
      path: '/files',
      name: 'Files',
      component: Files,
      // meta: {
      //   requiresAuth: true
      // }
    },{
      path: '*',
      name: 'NotFound',
      component: NotFound
    },
  ]
})



router.beforeEach((to, from, next) => {
  const token = window.localStorage.getItem('madblog-token')
  // 判断路由是否需要登录权限且token是否存在
  if (to.matched.some(record => record.meta.requiresAuth) && (!token || token === null)) {
    next({
      path: '/login',
      // 将跳转的路由path作为参数，登录成功后跳转到该路由
      query: { redirect: to.fullPath }
    })
  } else if (token && to.name == 'Login') {
    // 已登录用户不能访问登录页面
    next({
      path: from.fullPath
    })
  } else {
    next()
  }
})

export default router 
