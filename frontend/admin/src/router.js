import Vue from 'vue'
import Router from 'vue-router'
import Layout from '@/views/layout/Layout'
import {
    getToken
} from '@/utils/auth'


Vue.use(Router)
const whiteList = ['/login']

export const constantRouterMap = [{
        path: '/redirect',
        component: Layout,
        hidden: true,
        children: [{
            path: '/redirect/:path*',
            component: () => import('@/views/redirect')
        }]
    },
    {
        name: 'login',
        path: '/login',
        component: () => import('@/views/login'),
        hidden: true
    },
    {
        path: '/',
        component: Layout,
        redirect: '/home',
        children: [{
            path: 'home',
            component: () => import('@/views/home'),
            name: 'Home',
            meta: {
                title: 'Home',
                icon: 'dashboard',
                affix: true
            }
        }]
    },
    {
        path: '/post',
        component: Layout,
        redirect: '/post/list',
        name: 'Post',
        meta: {
            title: 'Post',
            icon: 'documentation'
        },
        children: [{
                path: 'create',
                component: () => import('@/views/post/create'),
                name: 'CreatePost',
                meta: {
                    title: 'CreatePost',
                    icon: 'edit'
                }
            },
            {
                path: ':id(\\d+)/edit',
                component: () => import('@/views/post/edit'),
                name: 'EditPost',
                meta: {
                    title: 'EditPost',
                    noCache: true
                },
                hidden: true
            },
            {
                path: 'list',
                component: () => import('@/views/post/list'),
                name: 'PostList',
                meta: {
                    title: 'PostList',
                    icon: 'list'
                }
            }
        ]
    },
    {
        path: '/file',
        component: Layout,
        redirect: '/file/list',
        name: 'File',
        meta: {
            title: 'File',
            icon: 'documentation'
        },
        children: [{
                path: 'list',
                component: () => import('@/views/file/list'),
                name: 'FilestList',
                meta: {
                    title: 'FileList',
                    icon: 'list'
                }
            },
            {
                path: 'create',
                component: () => import('@/views/file/create'),
                name: 'createFile',
                meta: {
                    title: 'CreateFile',
                    icon: 'edit'
                }
            }, {
                path: ':id(\\d+)/update',
                component: () => import('@/views/file/update'),
                name: 'UpdateFile',
                meta: {
                    title: 'UpdateFile',
                    noCache: true
                },
                hidden: true
            },
        ]
    },
    {
        path: '/404',
        component: () => import('@/views/404'),
        hidden: true
    },
    {
        path: '*',
        redirect: '/404',
        hidden: true
    }
]

let router = new Router({
    base: process.env.BASE_URL,
    routes: constantRouterMap
})

router.beforeEach((to, from, next) => {
    if (getToken()) {
        /* has token*/
        if (to.path === '/login') {
            next({
                path: '/'
            })
        } else {
            next()
        }
    } else {
        /* has no token*/
        if (whiteList.indexOf(to.path) !== -1) { // 在免登录白名单，直接进入
            next()
        } else {
            next(`/login?redirect=${to.path}`) // 否则全部重定向到登录页
        }
    }
})

export default router