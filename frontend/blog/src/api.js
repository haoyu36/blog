import request from '@/http'

const getpost = (n) => {
    const url = '/api/post/' + n
    return request.get(url)
}

const gettags = () => {
    const url = '/api/tags'
    return request.get(url)
}

const getarchives = () => {
    const url = '/api/archives'
    return request.get(url)
}

const getposts = (n) => {
    const url = '/api/posts/' + n
    return request.get(url)
}

const getfiles = (n) => {
    const url = '/file/page/' + n
    return request.get(url)
}

const gettagposts = (url) => {
    return request.get(url)
}

const getsearch = () => {
    const url = '/api/search'
    return request.get(url)
}

const gethomepost = () => {
    const url = '/api/homepost'
    return request.get(url)
}

const gethomefile = () => {
    const url = '/file/homefile'
    return request.get(url)
}

export {
    getpost,
    gettags,
    getarchives,
    getposts,
    gettagposts,
    getsearch,
    gethomepost,
    gethomefile,
    getfiles
}