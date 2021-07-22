// pages/owner/owner.js
import Notify from '/../../../miniprogram_npm/@vant/weapp/notify/notify';

const app = getApp()
const apikey = 'AgYDqGIvReJlaznT5z2ooQImI6g='//masterapikey
const deviceid = '720373994'//设备ID
var deviceConnected = false
var current_value = 0
const deviceInfoURL = "https://api.heclouds.com/devices/" + deviceid
const getDataStreamURL = "https://api.heclouds.com/devices/" + deviceid + "/datastreams"
const getDataPointsURL = "https://api.heclouds.com/devices/" + deviceid + "/datapoints"
const sendMqttURL = "https://api.heclouds.com/mqtt?topic="
const sendCommandURL = "https://api.heclouds.com/cmds"
var led = 0
var feng =2
var door=5
var temp=1
function getDeviceInfo(that) {
  //查看设备连接状态，并刷新按钮状态
  wx.request({
    url: deviceInfoURL,
    header: {
      'content-type': 'application/x-www-form-urlencoded',
      "api-key": apikey,
    },
    data: {
    },
    success(res) {
      // console.log(res)
      if (res.data.data.online) {
        console.log("设备已经连接")
        deviceConnected = true
      } else {
        console.log("设备还未连接")
        deviceConnected = false
      }
    },
    fail(res) {
      console.log("请求失败")
      deviceConnected = false
    },
    complete() {
      if (deviceConnected) {
        that.setData({ deviceConnected: true })
      } else {
        that.setData({ deviceConnected: false })
      }
    }
  })
}

function deviceInit(that) {
  console.log("开始初始化按钮")
  //初始化各个硬件的状态
  wx.request({
    url: getDataStreamURL,
    header: {
      'content-type': 'application/json',
      "api-key": apikey,
    },
    data: {
      
    },
    success(res) {
      for(var i=0; i<res.data.data.length; i++) {
        var info = res.data.data[i]
        
        if(info.current_value == 1) {
          that.setData({ led_checked : true})
        } else {
          that.setData({ led_checked : false})
        }
      }
    }
  })
}

function getDataStreamLastest(that) {
  //查看设备连接状态，并刷新按钮状态
  wx.request({
    url: getDataStreamURL,
    header: {
      'content-type': 'application/x-www-form-urlencoded',
      "api-key": apikey
    },
    data: {
    },
    success(res) {
       console.log(res.data.data[0].current_value)  
      that.setData({
        wendudata:res.data.data[0].current_value,
        shidudata:res.data.data[1].current_value
      }
      )   
    },
    fail(res) {
      console.log("请求失败")      
    },
    complete() {      
    }
  })
}
function getDataPoints(that) {
  //查看设备连接状态，并刷新按钮状态
  wx.request({
    url: getDataPointsURL,
    header: {
      'content-type': 'application/json',
      "api-key": apikey
    },
    data: {
      limit:10
    },
    success(res) {
       console.log(res.data)
       that.setData({
        historydata: JSON.stringify(res.data)
        }
        )           
    },
    fail(res) {
      console.log("请求失败")      
    },
    complete() {      
    }
  })
}


function mqttcontrol(switch_value) {  
  //按钮发送命令控制硬件
  wx.request({
    url: sendMqttURL+"feng",
    method: 'POST',
    header: {
      'content-type': 'application/x-www-form-urlencoded',
      "api-key": apikey
    },
    data:switch_value,//注意格式
    success(res) {
      console.log("控制成功")
      console.log(res)      
    }
  })
}

function controlLED(hardware_id ,switch_value) {
  // console.log("发送命令：" + hardware_id + ":{" + switch_value + "}")
  console.log("发送命令：" + hardware_id + ":" +switch_value )
  //按钮发送命令控制硬件
  wx.request({
    url: sendCommandURL + "?device_id=" + deviceid,
    method: 'POST',
    header: {
      'content-type': 'application/json',
      "api-key": apikey
    },
    // data: hardware_id + ":{" + switch_value + "}",      //TODO 设计自定义语言 blueled:{V}, 预感这边可能会有问题
    data: switch_value ,
    success(res) {
      console.log("控制成功")
      console.log(res)
     console.log(res.data);
    }
  })
}

function cmdscontrol(switch_value) {  
  //按钮发送命令控制硬件
  wx.request({
    url: sendCommandURL+deviceid,
    method: 'POST',
    header: {
      'content-type': 'application/x-www-form-urlencoded',
      "api-key": apikey
    },
    data: switch_value,//注意格式
    success(res) {
      console.log("控制成功")
      console.log(res)      
    }
  })
}
Page({

  /**
   * 页面的初始数据
   */
  data: {
    show:true,
    activeNames: ['1'],
    wendu_state: "../images/temper.png",
    fan_state: "../images/fan_off.png",
    shidu_state: "../images/moist.png",
    led_state: "../images/led.jpg",
    wendudata:"0",
    shidudata:"0",
    historydata:"0",
    Mqttchecked:false,
    Dynamochecked:false,
    numberonedoor:false,
    numberonelight:false,
    nofiyshow:true,
    currentDate:null,

  },
  onChange(event) {
    this.setData({
      activeNames: event.detail,
    });
  },
  onOpen(event) {
    console.log("张开")
  },
  onClose(event) {
    console.log("关闭")
  },
  /**
   * 生命周期函数--监听页面加载
   */

   //获取用户数据
  onLoad: function (res) { 
    if (wx.getUserProfile) {
      this.setData({
        canIUseGetUserProfile: true
      })
    }
    var that = this //将当前对象赋值
    getDeviceInfo(that)
    getDataPoints(that)
    getDataStreamLastest(that)
    app.getOutTimeMed()
    console.log(app.globalData.theOutTimeMed)
  },

   getUserProfile(e) {
    this.setData({ show: false });
  
    // 推荐使用wx.getUserProfile获取用户信息，开发者每次通过该接口获取用户个人信息均需用户确认
    // 开发者妥善保管用户快速填写的头像昵称，避免重复弹窗
    wx.getUserProfile({
      desc: '用于完善会员资料', // 声明获取用户个人信息后的用途，后续会展示在弹窗中，请谨慎填写
      success: (res) => {
        this.setData({
          userInfo: res.userInfo,
          hasUserInfo: true
        })
        wx.login({
          success (res) {
            console.log(res.code)
            if (res.code) {
              var app =getApp()
              var url = app.globalData.url
              //发起网络请求
              wx.request({
                url: url+'/loginORcreate/',
                type:'POST',
                header: {
                  'content-type': 'application/json'
              },
                data:{
                  code:res.code
                },
                success: function(e) {
                  console.log(e)
                }
              })
            } else {
              console.log('登录失败！' + res.errMsg)
            }
          }
        })
      }
    })
  },
  getUserInfo(e) {
    this.setData({ show: false });
    // 不推荐使用getUserInfo获取用户信息，预计自2021年4月13日起，getUserInfo将不再弹出弹窗，并直接返回匿名的用户个人信息
    this.setData({
      userInfo: e.detail.userInfo,
      hasUserInfo: true
    })
  },
  detial(e){
    wx.navigateTo({
      url: '/pages/owners/my/my',
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
   
    var that = this    
    var timer = setInterval(function(){
      getDataStreamLastest(that)
    }, 5000)

    var app = getApp()
    setInterval(function(){  
      if(app.globalData.outTimeCode == 0){
      Notify({ type: 'danger', message: '您已有药品过期 尽快处理删除'});
    } }, 2000);

    var currentDate = app.globalData.currentDate
    if(currentDate != null){
      var countdown = app.countdown(currentDate)
      this.setData({
        nofiyshow : false,
        currentDate:countdown
      })
    }else{
      this.setData({
        nofiyshow : true,
       
      })
    }
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


  fengchange: function (event) {
    console.log(event.detail)
    // var cmdData = event.detail.value == true ? 2 : 3 //修改为约定的数据  电机对应风扇
    var cmdData
    //前端相关代码
    if(event.detail == true){
      cmdData = 2
      this.setData({
        Dynamochecked:true
      })
    }else{
      cmdData = 3
      this.setData({
        Dynamochecked:false
      })
    }

 //硬件相关代码
    if(cmdData==2)
    {
      led=2;
      controlLED("feng",2);
      
    }
    else  
    {
      led=3;
      controlLED("feng",3);
    }
  },
    ledchange: function (event) {
      // var cmdData = event.detail.value == true ? 1: 0 //修改为约定的数据,1号药箱门灯
       var cmdData
       //前端相关代码
      if(event.detail == true){
        cmdData = 0
        this.setData({
          numberonelight:true
        })
      }else{
        cmdData = 1
        this.setData({
          numberonelight:false
        })
      }

       //硬件相关代码
      if(cmdData==0)
      {
        led=0;
        controlLED("led",0);
        
      }
      else  
      {
        led=1;
        controlLED("led",1);
      }
      mqttcontrol(cmdData)
    },
    doorchange: function (event) {
      // var cmdData = event.detail.value == true ? 1: 0 //修改为约定的数据,1号药箱门灯
      var cmdData = event.detail.value == true ? 1 : 0 
      // controlLED("door",4);  
      console.log(cmdData)
      mqttcontrol(cmdData)
      // //前端相关代码
      // if(event.detail == true){
      //   cmdData = 4 
      //   this.setData({
      //    numberonedoor:true
      //   })
      // }else{
      //   cmdData = 5
      //   this.setData({
      //     numberonedoor:false
      //   })
      // }

      // //硬件相关代码
      // if(cmdData==4)
      // {
      //   door=4;
      //   controlLED("door",4);
      // }
      // else  
      // {
      //   door=5;
      //   controlLED("door",5);       
      // }
     
    },
   

  

})
