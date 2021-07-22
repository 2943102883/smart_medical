// app.js
App({
  onLaunch() {
    // 展示本地存储能力
    const logs = wx.getStorageSync('logs') || []
    logs.unshift(Date.now())
    wx.setStorageSync('logs', logs)

    // 获取用户信息
    wx.getSetting({
      success: res => {
        if (res.authSetting['scope.userInfo']) {
          // 已经授权，可以直接调用 getUserInfo 获取头像昵称，不会弹框
          wx.getUserInfo({
            success: res => {
              // 可以将 res 发送给后台解码出 unionId
              this.globalData.userInfo = res.userInfo
              console.log(res.userInfo);
              // 由于 getUserInfo 是网络请求，可能会在 Page.onLoad 之后才返回
              // 所以此处加入 callback 以防止这种情况
              if (this.userInfoReadyCallback) {
                this.userInfoReadyCallback(res)
              }
            }
          })
        }
      }
    })
  },
  getnowhours(){
    var timestamp = Date.parse(new Date());  
   
    var now = new Date(timestamp)
    return now.getHours()
  },
  getnowmin(){
    var timestamp = Date.parse(new Date());  
   
    var now = new Date(timestamp)
    return now.getMinutes()
  },

  countdown(currentDate){
    this.globalData.currentDate = currentDate

    var timestamp = Date.parse(new Date());  
    var now = new Date(timestamp)
    var nowtime = (parseInt(now.getHours())*60*60+parseInt(now.getMinutes())*60+parseInt(now.getSeconds()))*1000
   
    if(parseInt(nowtime) < parseInt(currentDate)){
      var countdown = parseInt(currentDate) - parseInt(nowtime) 
    }else{
      var countdown = 0
    }
    
    return countdown
  },
  getOutTimeMed(){
    var _this = this
    wx.request({
      url: 'http://api.sunshinego.online:9876/time/'+this.globalData.token,
      header: {
        'content-type': 'application/json',
      },
      success(res) {
        
        _this.globalData.outTimeCode = res.data.code
       
         _this.globalData.theOutTimeMed = res.data
      },
      fail(res) {
        console.log("请求失败")      
      },
      complete() {      
      }
    })
  },
  globalData: {
    userInfo: null,
    token:'1840707266',
    onedoor:false,
    currentDate:null,
    url:'http://api.sunshinego.online:9876',
    // str1 = 'ff920ecf9df8f5fdc162287ad8e363d0',
    // str2 = '8110004ee3f544cb2a983cfbc72ad055',
    theOutTimeMed:null,
    outTimeCode:null
  }
})
