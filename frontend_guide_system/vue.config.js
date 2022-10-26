const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    proxy: {
      '/weather': {
        target: "http://www.weather.com.cn/data/cityinfo/101010100.html",
        ws: true,
        changeOrigin: true,
        pathRewrite: {
          "^/weather": "",
        }
      },
      '/api': {
        target: "http://127.0.0.1:8000/",
        ws: true,
        changeOrigin: true,
        pathRewrite: {
          "^/api": "",
        }
      },
      '/todolist': {
        target: "http://152.136.154.181:8060/",
        ws: true,
        changeOrigin: true,
        pathRewrite: {
          "^/todolist": "",
        }
      }
    }
  }
})
