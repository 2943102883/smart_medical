// pages/mychange/change.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    moveshow: false,
    sex: '1',
    brishow: false,
    currentDate: new Date().getTime(),
    minDate: new Date(1960 / 1 / 1),
    brithday: null,
    telephone: null,
    name: null,
    age: null,
    contacts: null,
    health: null,
    height: null,

    weight: null,
  },

  //日期逻辑
  showPopup() {
    this.setData({ brishow: true });
  },

  onClose() {
    this.setData({ brishow: false });
  },
  confirm(res) {
    var seconds = Number(res.detail)

    var date = new Date(seconds)
    var year = date.getFullYear();
    var month = date.getMonth() + 1;
    var day = date.getDate();
    var bri = year + "-" + month + "-" + day;

    console.log(bri)
    this.setData({ brishow: false, brithday: bri });

  },

  //性别逻辑
  onClick(event) {
    const { name } = event.currentTarget.dataset;
    this.setData({
      sex: name,
    });
    console.log(this.data.sex)
  },

  //表单提交
  submit(e) {
    var _this = this
    var app =getApp()
    var url = app.globalData.url
    var token = app.globalData.token
    console.log(e)
    var ssex
    if (_this.data.sex == '1') {
      ssex = 0
    } else {
      ssex = 1
    }
    if (e.detail.value.name == null) {
      wx.showToast({

        title: '名字不能为空',

        duration: 2000,

        icon: 'none'

      });
      return false;
    }
    if (!(/^1[34578]\d{9}$/.test(e.detail.value.phone))) {

      wx.showToast({

        title: '手机号码有误',

        duration: 2000,

        icon: 'none'

      });

      return false;

    }

    wx.request({
      url: url+'/loginORcreate/',
      data: {
        token: token,
        name: e.detail.value.name,
        sex: ssex,
        brithday: e.detail.value.brithday,
        height: e.detail.value.height,
        health: e.detail.value.health,
        contacts: e.detail.value.contacts,
        weight:e.detail.value.weight
      },
      header: { 'content-type': 'application/json' },
      method: 'PUT',
      success: (result) => {
        console.log(result)
        wx.showToast({

          title: '修改成功',
  
          duration: 2000,
  
          icon: 'none'
  
        });

        wx.navigateBack({
          delta: 1, // 回退前 delta(默认为1) 页面
          success: function(res){
            // success
          },
          fail: function() {
            // fail
          },
          complete: function() {
            // complete
          }
        })
        
  
      },
      fail: () => { },
      complete: () => { }
    });

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
      url: url+'/showuser/' + token,
      header: { 'content-type': 'application/x-www-form-urlencoded' },
      type: 'GET',
      success: function (e) {
        console.log("成功")
        // console.log(e.data)
        _this.setData({
          name: e.data.message.name,
          age: e.data.message.age,
          contacts: e.data.message.contacts,
          health: e.data.message.health,
          height: e.data.message.height,
          sex: e.data.message.sex,
          weight: e.data.message.weight
        })
      },
      fail: function (e) {
        console.log(e)
        console.log("失败")
      }
    });
    this.setData({
      moveshow: true
    })
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
