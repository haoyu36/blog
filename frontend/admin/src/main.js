import Vue from 'vue'

import 'normalize.css/normalize.css' // A modern alternative to CSS resets

import Element from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'

import '@/styles/index.scss' // global css

import App from './App'
import store from './store'
import router from './router'

import './icons' // icon

import * as filters from './filters' // global filters


Vue.use(Element, 'medium')

Object.keys(filters).forEach(key => {
  Vue.filter(key, filters[key])
})

Vue.config.productionTip = false

import VuePaginateAl from 'vue-paginate-al' // 分页
Vue.component('vue-paginate-al', VuePaginateAl);



new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')