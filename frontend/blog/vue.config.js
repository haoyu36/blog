module.exports = {
    outputDir: '../../dist', // 运行 npm run build 时生成的生产环境构建文件的目录
    assetsDir: 'static/blog/', // 放置生成的静态资源的目录 (相对于 outputDir) 
    indexPath: 'index.html', // 指定生成的 index.html 的输出路径 (相对于 outputDir)
    productionSourceMap: false, // 不需要生产环境的 source map
    chainWebpack: config => {
        config.module
            .rule('svg')
            .exclude.add(resolve('src/icons'))
            .end()

        config.module
            .rule('icons')
            .test(/\.svg$/)
            .include.add(resolve('src/icons'))
            .end()
            .use('svg-sprite-loader')
            .loader('svg-sprite-loader')
            .options({
                symbolId: 'icon-[name]'
            })
    },
}

var path = require('path')

function resolve(dir) {
    return path.join(__dirname, './', dir)
}