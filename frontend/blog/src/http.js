import axios from 'axios'
import router from './router'


// axios.defaults.baseURL = 'http://127.0.0.1:5000'
axios.defaults.baseURL = 'http://haoyu36.cn'
axios.defaults.retry = 2 // 重试次数


// 响应拦截器
axios.interceptors.response.use(function (response) {
    return response
}, function (error) {
    if (error.response) {
        // 匹配不同的响应码
        switch (error.response.status) {
            case 403:
                router.back()
                break

            case 404:
                this.$router.push("/notfound")
                break

            case 500:
                router.back()
                break
        }
    } else {
        // router.back()
    }
    return Promise.reject(error)
})

export default axios