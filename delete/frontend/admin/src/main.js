// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
// 导入配置了全局拦截器后的 axios
import axios from './http'
import 'bulma/css/bulma.css'
import VuePaginateAl from 'vue-paginate-al'
import mavonEditor from 'mavon-editor'
import 'mavon-editor/dist/css/index.css'
import Multiselect from 'vue-multiselect'


// register globally
Vue.component('multiselect', Multiselect)


Vue.component('vue-paginate-al', VuePaginateAl)
Vue.use(mavonEditor)


Vue.config.productionTip = false
// 将 $axios 挂载到 prototype 上，在组件中可以直接使用 this.$axios 访问
Vue.prototype.$axios = axios


new Vue({
  router,
  render: h => h(App),
}).$mount('#app')
