import Toast from '/../../../miniprogram_npm/@vant/weapp/toast/toast';
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
    list:null,
    name:null
  },
  // 数据监听器
  observers: {},
  // 组件方法
  methods: {
    
    init() {},
    detail(e){
      var name = this.data.name
     
      wx.navigateTo({
        url: '/pages/Medicine/Meddetail/index?num='+e.currentTarget.dataset.num+"&name="+name,
      })
    },
    onSearch(e){

      Toast.loading({
        message: '加载中...',
        forbidClick: true,
        duration:1500
      });
      var _this = this
      _this.setData({
        list:null
      })
      var str = e.detail
      var app =getApp()
      var url = app.globalData.url
      console.log(str)
      wx.request({
        url: url+'/show2/'+str,
        type:'GET',
        header: {
          'content-type': 'application/x-www-form-urlencoded'
      },
       
        success: function(e) {
          console.log("成功")
          console.log(e.data.data)
          var list = e.data.data
          
          _this.setData({
            list:list,
            name:str
          })
        },
        fail: function(e) {
          console.log(e)
          console.log("失败")
        }
      })
    }
  },
  // 组件生命周期
  lifetimes: {
    created() {},
    attached() {
      this.init()
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
