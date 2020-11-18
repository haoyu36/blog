import Vue from 'vue'
import axios from 'axios'
import router from './router'


// 基础配置

axios.defaults.baseURL = 'http://127.0.0.1:5000'
// axios.defaults.baseURL = 'http://haoyu36.cn/admin/'
axios.defaults.retry = 2 // 重试次数


// // 请求拦截器
// axios.interceptors.request.use(function (config) {
//   // 发送请求前给请求头增加认证字段
//   const token = window.localStorage.getItem('madblog-token')
//   if (token) {
//     config.headers.Authorization = `Bearer ${token}`
//   }
//   return config
// }, function (error) {
//   // 请求错误执行
//   return Promise.reject(error)
// })

// // 响应拦截器
// axios.interceptors.response.use(function (response) {
//   return response
// }, function (error) {
//   if (error.response) {
//     // 匹配不同的响应码
//     switch (error.response.status) {
//       case 401:
//         // 清除 Token 及 已认证 等状态
//         window.localStorage.removeItem('madblog-token')
//         // 跳转到登录页
//         if (router.currentRoute.path !== '/login') {
//           router.replace({
//             path: '/login',
//             query: {
//               redirect: router.currentRoute.path
//             },
//           })
//         }
//         break
//       case 404:
//         this.$router.push({
//           path: '/*'
//         });
//         break
//     }
//   }
//   return Promise.reject(error)
// })

export default axios