import Notify from '/../../miniprogram_npm/@vant/weapp/notify/notify';
Page({

  /**
   * 页面的初始数据
   */
  data: {
    show:false,
    newslist:null
  },

  scanCode:function(){
    var that=this;
    wx.scanCode({
      onlyFromCamera:false,   //调用摄像头相册选择二维码
      scanType:[],      //不指定扫码类型
      success:function(res){
        that.setData({
          resCode:res
        })
      }
    })
  },
  detail(e){
    var src = e.currentTarget.dataset.src
    console.log(src)
    
    wx.navigateTo({
      url:'/pages/index/newsdetail/index?src='+src
    })
   
  },
  morenews(){
    wx.navigateTo({
      url: '/pages/index/morenews/index'
    })
  },
  onSearch:function(e){
    console.log(e);
  },
  onTap:function(){
    wx.navigateTo({
      url: '/pages/Medicine/MedicineSearch/index',
    })
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    var app = getApp()
    app.getOutTimeMed()

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

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {
    
  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {
    var _this = this;
    _this.setData({
      show:true
    });
    var app = getApp()
    setInterval(function(){  if(app.globalData.outTimeCode == 0){
      Notify({ type: 'danger', message: '您已有药品过期 尽快处理删除' });
    } }, 2000);
  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {
    
  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {
    
  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {
    
  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {
    
  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {
    
  }

 
})