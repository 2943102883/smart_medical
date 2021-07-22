import Notify from '/../../../../miniprogram_npm/@vant/weapp/notify/notify';
import Toast from '/../../../../miniprogram_npm/@vant/weapp/toast/toast';
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
    moveshow: false,

    name:null,
    category:null,
    introduce:null,
    suit:null,
    bad:null,
    life:null,
    use:null,
    taboo:null,
    heed:null,
    savemethod:null,
    fileList:[],
    maxcount:3
  },
  // 数据监听器
  observers: {},
  // 组件方法
  methods: {
    afterRead(event) {
      var _this = this
      const file = event.detail.file
      let list = _this.data.fileList
  
      console.log(file.length)
      if(list.length == 0){
        for(var i=0;i<file.length;i++){
          list = list.concat(file[i])
          console.log(list)
        }
      }else if(list.length == 1){
        for(var i=0;i<file.length;i++){
          list = list.concat(file[i])
          if(i == 2){
            break
          }
          console.log(list)
        }
      }else if(list.length == 2){
        list = list.concat(file[0])
        console.log(list)
      }
     
     _this.setData({
      fileList: list
     })
     console.log("list:"+_this.data.fileList)
      // // 当设置 mutiple 为 true 时, file 为数组格式，否则为对象格式
     

      //test上传
      // wx.request({
       
      //   url: 'http://172.16.176.120:8000/imgtest/',
      //   data: {
      //     picture:_this.data.fileList
      //   },
      //   method: 'POST', // OPTIONS, GET, HEAD, POST, PUT, DELETE, TRACE, CONNECT
      //   header: {
      //     'content-type': 'application/x-www-form-urlencoded'
      // },
      //   success: function(res){
      //    console.log(res)
       
      //   },
      //   fail: function() {
         
      //   },
      //   complete: function() {
      //     // complete
      //   }
      // })
    },
    deletepic(e){
      var _this = this
      var index = e.detail.index

      let list = _this.data.fileList
      list.splice(index,1);
    
      _this.setData({
        fileList:list
      })
    },


    submit(e){
      var app =getApp()
      var url = app.globalData.url
      var token = app.globalData.token
      var name = e.detail.value.name

      console.log(e.detail.value.life+"//"+name)
      if(name && e.detail.value.life){
        console.log("进入")
        wx.request({
       
          url: url+'/medical/'+name+'/'+token,
          data: {
            bad:e.detail.value.bad,
            category:e.detail.value.category,
            heed:e.detail.value.heed,
            life:e.detail.value.life,
            savemethod:e.detail.value.savemethod,
            suit:e.detail.value.suit,
            taboo:e.detail.value.taboo,
            use:e.detail.value.use,
            introduce:e.detail.value.introduce
          },
          method: 'GET', // OPTIONS, GET, HEAD, POST, PUT, DELETE, TRACE, CONNECT
          // header: {}, // 设置请求的 header
          success: function(res){
           console.log(res)
           Toast(name+'添加成功');
           wx.navigateBack({
             delta: 1, // 回退前 delta(默认为1) 页面
           })
          },
          fail: function() {
            Toast(name+'添加失败');
          },
          complete: function() {
            // complete
          }
        })
      }else{
        Notify('药品名与保质期不能为空');
      }
     
    },
    note(e){
      Toast('当前的药品保质期为'+'\n'+e.detail.value+'\n'+'若不为月份请修改');
    },
    init() {
      this.setData({
        moveshow:true
      })
    },
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
