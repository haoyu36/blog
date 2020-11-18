// vue.config.js

// 导入compression-webpack-plugin
// const CompressionPlugin = require('compression-webpack-plugin')
// 定义压缩文件类型
// const productionGzipExtensions = ['js', 'css']


module.exports = {
    // 选项...
  outputDir: '../../dist',       // 运行 npm run build 时生成的生产环境构建文件的目录
  assetsDir: 'static/blog/',            // 放置生成的静态资源的目录 (相对于 outputDir) 
  indexPath: 'index.html',       // 指定生成的 index.html 的输出路径 (相对于 outputDir)
  productionSourceMap: false,       // 不需要生产环境的 source map
	// 压缩文件配置
	// configureWebpack: config => {
	// 	if (process.env.NODE_ENV === 'production') {
	// 	    return {
	// 		    plugins: [new CompressionPlugin({
	// 		        test: /\.js$|\.html$|\.css/,     // 匹配文件名
	// 		        threshold: 1024,       // 对超过1k的数据进行压缩
	// 		        deleteOriginalAssets: false,     // 是否删除源文件
	// 		    })]
	// 	    }
	// 	}
	// },
}
