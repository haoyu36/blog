import Vue from 'vue'
import App from './App.vue'
import router from './router'

import 'bulma/css/bulma.min.css' // 开源CSS框架
import './icons' // icon

Vue.config.productionTip = false

Vue.use(require('vue-moment'));

import VuePaginateAl from 'vue-paginate-al' // 分页
Vue.component('vue-paginate-al', VuePaginateAl);

import VueFuse from 'vue-fuse' // 模糊搜索
Vue.use(VueFuse)

import 'bulma-timeline/dist/css/bulma-timeline.min.css';
import 'bulma-badge/dist/css/bulma-badge.min.css';

import hljs from 'highlight.js' // 代码高亮
import 'highlight.js/styles/github.css' // 高亮样式文件

Vue.directive('highlight', function (el) {
  let blocks = el.querySelectorAll('pre code');
  blocks.forEach((block) => {
    hljs.highlightBlock(block)
  })
})

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')