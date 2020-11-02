module.exports = {
    outputDir: '../../dist/add',
    assetsDir: 'static/admin/',
    indexPath: 'admin.html',
    productionSourceMap: false,
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
    }
}

var path = require('path')

function resolve(dir) {
    return path.join(__dirname, './', dir)
}