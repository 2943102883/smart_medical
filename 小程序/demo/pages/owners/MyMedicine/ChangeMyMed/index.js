import Toast from '/../../../../miniprogram_npm/@vant/weapp/toast/toast';
const pageOptions = {
  // 页面数据
  data: {
    isFirstOnShow: true, // 是否为首次执行onShow
    moveshow: false,
    oldname:null,

    name:null,
    category:null,
    introduce:null,
    suit:null,
    bad:null,
    life:null,
    use:null,
    taboo:null,
    heed:null,
    savemethod:null
  },
  // 页面载入时
  onLoad(e) {
    this.init(e)
  },
  // 页面初始化
  init(e) {
   var name = e.name
      this.setData({
        moveshow:true,
        oldname:name
      })
      var _this = this
     
      var app = getApp()
      var token = app.globalData.token
      var url = app.globalData.url
      wx.request({
        url: url+'/showmedical/'+token,

        method: 'GET', // OPTIONS, GET, HEAD, POST, PUT, DELETE, TRACE, CONNECT
        // header: {}, // 设置请求的 header
        success: function(res){
         
        
          var array = res.data.data[0]
          var arrays = res.data.data
          
          for (var k = 0, length = array.length; k <= length; k++) {
           if(arrays[k][0].name == name){
               _this.setData({
                name:arrays[k][0].name,
                category:arrays[k][0].category,
                introduce:arrays[k][0].introduce,
                suit:arrays[k][0].suit,
                bad:arrays[k][0].bad,
                life:arrays[k][0].life,
                use:arrays[k][0].use,
                taboo:arrays[k][0]. taboo,
                heed:arrays[k][0].heed,
                savemethod:arrays[k][0].savemethod
          })
              } 
          }
        },
        fail: function() {
          // fail
        },
        complete: function() {
          // complete
        }
      })
  },
  submit(e){
    var app =getApp()
    var url = app.globalData.url
    var token = app.globalData.token
    var oldname = this.data.oldname
   
    if(oldname == e.detail.value.name){
      wx.request({
        url: url+'/medical/'+oldname+'/'+token+'/',
      // url: 'http://101.201.181.46:9876/medical/'+oldname+'/'+token+'/',
      data: {
        newname:0,
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
      method: 'PUT', // OPTIONS, GET, HEAD, POST, PUT, DELETE, TRACE, CONNECT
      header: {
        'content-type': 'application/json'
    },
      success: function(res){
     
       Toast(oldname+'修改成功');
       wx.navigateBack({
         delta: 1, // 回退前 delta(默认为1) 页面
       })
      },
      fail: function() {
        Toast(oldname+'修改失败');
      },
      complete: function() {
        // complete
      }
    })
    }else{
       wx.request({
           url: url+'/medical/'+oldname+'/'+token+'/',
  
      data: {
        newname:e.detail.value.name,
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
      method: 'PUT', // OPTIONS, GET, HEAD, POST, PUT, DELETE, TRACE, CONNECT
      header: {
        'content-type': 'application/json'
    },
      success: function(res){
       
       Toast(oldname+'修改成功');
       wx.navigateBack({
         delta: 1, // 回退前 delta(默认为1) 页面
       })
      },
      fail: function() {
        Toast(oldname+'修改失败');
      },
      complete: function() {
        // complete
      }
    })
    }
    
   
  },
  // 页面准备好时
  onReady() {},
  // 页面显示时
  onShow() {
    const { isFirstOnShow } = this.data

    if (isFirstOnShow) {
      // 首次执行时
      this.setData({
        isFirstOnShow: false,
      })
      return
    }
  },
  // 页面隐藏时
  onHide() {},
  // 页面卸载时
  onUnload() {},
  // 下拉页面时
  onPullDownRefresh() {},
  // 到达页面底部时
  onReachBottom() {},
  // 页面滚动时
  onPageScroll() {},
  // 分享时，注：onShareAppMessage不能为async异步函数，会导致不能及时取得返回值，使得分享设置无效
  onShareAppMessage() {
    /* const title = ''
    const path = ''
    const imageUrl = ``

    return {
      title,
      path,
      imageUrl,
    } */
  },
}

Page(pageOptions)
