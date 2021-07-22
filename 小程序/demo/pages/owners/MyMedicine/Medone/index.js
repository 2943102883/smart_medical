import Dialog from '/../../../../miniprogram_npm/@vant/weapp/dialog/dialog';
const componentOptions = {
  // 组件选项
  options: {
    multipleSlots: true,
  },
  behaviors: [],
  properties: {},
  // 组件数据
  data: {
    isPageHidden: false, // 页面是否处于隐藏状态
    list:null
  },
  // 数据监听器
  observers: {},
  // 组件方法
  methods: {
    init() {},
    change(e){
      var name = e.currentTarget.dataset.name
      wx.navigateTo({
        url: '/pages/owners/MyMedicine/ChangeMyMed/index?name='+name,
      })
    },
    delete(e){
      var _this = this
      var app =getApp()
      var url = app.globalData.url
      var token = app.globalData.token
      var name = e.currentTarget.dataset.name
      Dialog.confirm({
        width:350,
        context: this,
        title: '删除确认',
        message: '是否删除'+name,
      })
        .then(() => {
          wx.request({
            url: url+'/delete/'+name+'/'+token,
            method: 'GET', // OPTIONS, GET, HEAD, POST, PUT, DELETE, TRACE, CONNECT
            // header: {}, // 设置请求的 header
            success: function(res){
              wx.request({
                url: url+'/showmedical/'+token,
        
                method: 'GET', // OPTIONS, GET, HEAD, POST, PUT, DELETE, TRACE, CONNECT
                // header: {}, // 设置请求的 header
                success: function(res){
                  _this.setData({
                    list:res.data.data
                  })
                },
                fail: function() {
                  // fail
                },
                complete: function() {
                  // complete
                }
              })
            },
            fail: function() {
              // fail
            },
            complete: function() {
              // complete
            }
          })
        })
        .catch(() => {
          // on cancel
        });
    }
  },
  // 组件生命周期
  lifetimes: {
    created() {},
    attached() {
   
      this.init()
      var _this = this
     
      var app =getApp()
      var url = app.globalData.url
      var token = app.globalData.token

      wx.request({
        url: url+'/showmedical/'+token,

        method: 'GET', // OPTIONS, GET, HEAD, POST, PUT, DELETE, TRACE, CONNECT
        // header: {}, // 设置请求的 header
        success: function(res){
          console.log(res.data.data)
          _this.setData({
            list:res.data.data
          })
        },
        fail: function() {
          // fail
        },
        complete: function() {
          // complete
        }
      })
    },
    ready() {},
    moved() {},
    detached() {},
  },
  definitionFilter() {},
  // 页面生命周期
  pageLifetimes: {
    // 页面被展示
    show() {
      const { isPageHidden } = this.data

      // show事件发生前，页面不是处于隐藏状态时
      if (!isPageHidden) {
        return
      }
     
      var _this = this
     
      var app =getApp()
      var url = app.globalData.url
      var token = app.globalData.token

      wx.request({
        url: url+'/showmedical/'+token,

        method: 'GET', // OPTIONS, GET, HEAD, POST, PUT, DELETE, TRACE, CONNECT
        // header: {}, // 设置请求的 header
        success: function(res){
         
          _this.setData({
            list:res.data.data
          })
        },
        fail: function() {
          // fail
        },
        complete: function() {
          // complete
        }
      })
      // 重新执行定时器等操作
    },
    // 页面被隐藏
    hide() {
      this.setData({
        isPageHidden: true,
      })

      // 清除定时器等操作
    },
    // 页面尺寸变化时
    resize() {},
  },
}

Component(componentOptions)
