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
    newslist:null,
    page:1
  },
  // 数据监听器
  observers: {},
  // 组件方法
  methods: { 
    detail(e){
      var src = e.currentTarget.dataset.src
      console.log(src)
      wx.navigateTo({
        url:'/pages/index/newsdetail/index?src='+src
      })
    },
  onReachBottom: function () {
    this.setData({
      page:this.data.page + 1
    })

    var str1 = 'ff920ecf9df8f5fdc162287ad8e363d0'
    var str2 = '8110004ee3f544cb2a983cfbc72ad055'
    wx.request({
      url: 'http://v.juhe.cn/toutiao/index?type=jiankang&key='+str2+'&page_size=10&page='+this.data.page,
      header: {'content-type':'application/json'},
      method: 'GET',
      dataType: 'json',
      responseType: 'text',
      success: (result)=>{
        this.setData({
          newslist: this.data.newslist.concat(result.data.result.data)
        })
      },
      fail: ()=>{},
      complete: ()=>{}
    });
},

  },
  // 组件生命周期
  lifetimes: {
   
    created() {},
    attached() {
      var str1 = 'ff920ecf9df8f5fdc162287ad8e363d0'
      var str2 = '8110004ee3f544cb2a983cfbc72ad055'
      wx.request({
        url: 'http://v.juhe.cn/toutiao/index?type=jiankang&key='+str2+'&page_size=10',
        header: {'content-type':'application/json'},
        method: 'GET',
        dataType: 'json',
        responseType: 'text',
        success: (result)=>{
          console.log(result.data)
          this.setData({
            newslist:result.data.result.data
          })
        
        },
        fail: ()=>{},
        complete: ()=>{}
      });
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
