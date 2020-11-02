import axios from 'axios'
import {
  Message
} from 'element-ui'
import {
  getToken
} from '@/utils/auth'


// axios.defaults.baseURL = 'http://127.0.0.1:5000'
axios.defaults.baseURL = 'http://haoyu36.cn'
axios.defaults.retry = 2 // 重试次数



// request interceptor
axios.interceptors.request.use(
  config => {
    // Do something before request is sent
    if (getToken()) {
      config.headers['authorization'] = `Bearer ${getToken()}`
    }
    return config
  },
  error => {
    // Do something with request error
    console.log(error) // for debug
    Promise.reject(error)
  }
)

// response interceptor
axios.interceptors.response.use(
  response => response,
  error => {
    if (error.response) {
      // 匹配不同的响应码
      switch (error.response.status) {
        case 401:
          Message({
            message: '你没有相关权限，操作无效',
            type: 'error',
            duration: 5 * 1000
          })
          break

        case 500:
          Message({
            message: '服务器错误',
            type: 'error',
            duration: 5 * 1000
          })
          break
      }
    } else {
      Message({
        message: error.message,
        type: 'error',
        duration: 5 * 1000
      })
    }
    return Promise.reject(error)
  }
)

export default axios