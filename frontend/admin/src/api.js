import request from '@/utils/request'


const login = (info) => {
    const url = '/admin/tokens'
    return request.post(url, {}, {
        auth: info
    })
}

// 博客相关

const getPostList = (n) => {
    const url = '/api/posts/' + n
    return request.get(url)
}

const updatePost = (data) => {
    const url = '/admin/post'
    return request.post(url, data)
}

const updatePostStatus = (id, method) => {
    return request({
        url: `/admin/post/${id}/status`,
        method: method
    })
}

const deletePost = (id) => {
    const url = '/admin/post/' + id
    return request.delete(url)
}

const fetchPost = (id) => {
    const url = '/api/post/' + id
    return request.get(url)
}

const fetchTags = () => {
    const url = '/api/tag-lst'
    return request.get(url)
}


// 文件相关

const fetchFile = (id) => {
    const url = '/file/' + id
    return request.get(url)
}

const getFileList = (n) => {
    const url = '/file/page/' + n
    return request.get(url)
}

const deleteFile = (id) => {
    const url = '/file/delete/' + id
    return request.get(url)
}

const updateFile = (data) => {
    const url = '/file/update'
    return request.post(url, data)
}

const updateFileStatus = (id, method) => {
    return request({
        url: `/file/${id}/status`,
        method: method
    })
}

const uploadFile = (data) => {
    return request({
        url: '/file/upload',
        headers: {
            'content-type': 'application/x-www-form-urlencoded'
        },
        method: 'post',
        data: data
    })
}


export {
    getPostList,
    updatePost,
    updatePostStatus,
    deletePost,
    fetchPost,
    fetchTags,
    login,
    getFileList,
    updateFileStatus,
    deleteFile,
    uploadFile,
    fetchFile,
    updateFile
}