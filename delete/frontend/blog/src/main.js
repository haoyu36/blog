// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import axios from 'axios'

import 'bulma/css/bulma.css'     // 开源CSS框架
import VuePaginateAl from 'vue-paginate-al'   // 分页
import VueFuse from 'vue-fuse'   // 模糊搜索
import hljs from 'highlight.js'   // 代码高亮
import 'highlight.js/styles/googlecode.css' // 高亮样式文件


Vue.directive('highlight',function (el) {
  let blocks = el.querySelectorAll('pre code');
  blocks.forEach((block)=>{
    hljs.highlightBlock(block)
  })
})


Vue.config.productionTip = false;
Vue.use(VueFuse);
Vue.component('vue-paginate-al', VuePaginateAl);
Vue.use(require('vue-moment'));


axios.defaults.baseURL = 'http://192.168.43.20:5000/api'
// axios.defaults.baseURL = 'http://haoyu36.cn/api/'
Vue.prototype.$axios = axios

/* eslint-disable */
new Vue({
  router,
  render: h => h(App),
}).$mount('#app')