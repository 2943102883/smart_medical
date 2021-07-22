
Page({

  /**
   * 页面的初始数据
   */
  data: {
  
          name:'空',
          height:'空',
          weight:'空',
          telephone:'空',
          contacts:'空',
          health:'空',
          sex:'空',
          age:'空',
          emply:false,

  },
  load:function(){
    wx.navigateTo({
      url: '/pages/owners/mychange/change',
    })
  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    var _this = this
    var app =getApp()
    var url = app.globalData.url
    var token = app.globalData.token
    wx.request({
      url: url+'/showuser/'+token,
      header: {'content-type': 'application/x-www-form-urlencoded'},
      type: 'GET',
      success: function(e) {
        console.log("成功")
        console.log(e.data)
        _this.setData({
          name:e.data.message.name,
          age:e.data.message.age,
          contacts:e.data.message.contacts,
          health:e.data.message.health,
          height:e.data.message.height,
          sex:e.data.message.sex,
          weight:e.data.message.weight
        })
      },
      fail: function(e) {
        console.log(e)
        console.log("失败")
      }
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

  },
  
});
