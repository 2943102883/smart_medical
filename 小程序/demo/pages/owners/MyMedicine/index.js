const app = getApp()
const apikey = 'eabgmXNaX7XmfhiAr=MQjHuUiuU='//masterapikey
const deviceid = '702213339'//设备ID
var deviceConnected = false
const deviceInfoURL = "https://api.heclouds.com/devices/" + deviceid
const getDataStreamURL = "https://api.heclouds.com/devices/" + deviceid + "/datastreams"
const getDataPointsURL = "https://api.heclouds.com/devices/" + deviceid + "/datapoints"
const sendMqttURL = "https://api.heclouds.com/mqtt?topic="
const sendCommandURL = "https://api.heclouds.com/cmds"

var door=5
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
    show:false,
    isFirstOnShow: true, // 是否为首次执行onShow
    currentDate: '12:00',
    time: 30 * 60 * 60 * 1000,
    minHour: 0,
    maxHour: 24,
    minMinute:0,
    choosebuttonshow:true,
    countdownshow:true,
    theOutTimeMed:null
  },
  // 数据监听器
  observers: {},
  // 组件方法
  methods: {
    doorchange: function (event) {
      // var cmdData = event.detail.value == true ? 1: 0 //修改为约定的数据,1号药箱门灯
      var cmdData
      //前端相关代码
      if(event.detail == true){
        cmdData = 4 
        this.setData({
         numberonedoor:true
        })
      }else{
        cmdData = 5
        this.setData({
          numberonedoor:false
        })
      }

      //硬件相关代码
      if(cmdData==4)
      {
        door=4;
        controlLED("door",4);
      }
      else  
      {
        door=5;
        controlLED("door",5);       
      }
      mqttcontrol(cmdData)
    },

    finished(){
      controlLED("door",4);
      setTimeout (function(){
        controlLED("door",5);

      },3000)
    },
    deleteTime(){
      this.setData({
        choosebuttonshow:true,
        countdownshow:true
      })
      var app = getApp()
      app.globalData.currentDate = null
    },
    onClose(){
      this.setData({
        show:false
      })
    },
    chooseTime(){
      this.setData({
        show:true
      })
    },
    onInput(event) {
      var app = getApp()
  
      var time = event.detail
      var times = time.split(":")
    
      var currentDate = (parseInt(times[0])*60*60+parseInt(times[1])*60)*1000 
      var currentDate =  app.countdown(currentDate)

      this.setData({
        currentDate:currentDate,
        show:false,
        countdownshow:false,
        choosebuttonshow:false
      });
    },
    init() {},
    addMyMedicine(){
      wx.navigateTo({
        url: '/pages/owners/MyMedicine/addMyMedicine/index',
      })
    }
  },
  // 组件生命周期
  lifetimes: {
    created() {
    
    },
    attached() {
      this.init()
      var app = getApp()
      var theoutTimeMed = app.globalData.theOutTimeMed
      var nowhour = app.getnowhours()
      var nowmin = app.getnowmin()
      
      this.setData({
        minHour:nowhour,
        minMinute:nowmin,
        theOutTimeMed:theoutTimeMed.data
      })
      console.log(this.data.theOutTimeMed)
      var currentDate = app.globalData.currentDate
      if(currentDate != null){
      var countdown = app.countdown(currentDate)
      this.setData({
        currentDate:countdown,
        choosebuttonshow:false,
        countdownshow:false
      })
    }
    
    var that = this //将当前对象赋值
    getDeviceInfo(that)

    //getDataStreamLastest(that)

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
      var app = getApp()
    console.log(app.getnowhours())
   
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
