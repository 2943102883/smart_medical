import Toast from '/../../../miniprogram_npm/@vant/weapp/toast/toast';
const pageOptions = {
  // 页面数据
  data: {
    isFirstOnShow: true, // 是否为首次执行onShow
    detail:null,
    name:null,
   
    medname:"",
    suit :"",
    savemethod :"",
    err : "",
    bad :"",
    usemethod : ""
  },
  // 页面载入时
  onLoad(e) {
    Toast.loading({
      message: '加载中...',
      forbidClick: true,
      duration:1500
    });
    var app = getApp()
    var url = app.globalData.url
    this.init(e)
    var _this = this
    console.log(e.name+":"+e.num)
    var name = e.name
    var num =e.num

    _this.setData({
      name:name
    })

    if(name != ''){
      wx.request({
        url: url+'/search/'+name,
        type:'GET',
        data:{
          num:num
        },
        header: {
          'content-type': 'application/x-www-form-urlencoded'
      },
       
        success: function(e) {
          console.log("成功")
          
          var detail = e.data.data[num]
          console.log(detail)
          _this.setData({
            detail:detail
          })
        },
        fail: function(e) {
          console.log(e)
          console.log("失败")
        }
      })
    }else{
      if(num == 1){
        console.log("asdsa")
        _this.setData({
         
          medname:"石膏",
            suit :" 白虎汤和单味石膏煎剂对实验性致热家兔都具有一定的退热作用；不含石膏的知母甘草合剂和去钙白虎汤等均未见明显 退热效果, 可以认为石膏是白虎汤退热作用的主要药物, 石膏作用可被处方中的其他药物所加强, 但不随石膏的用量增加而增加",
            savemethod :"阴凉处",
            err : "用量过大，服后会出现疲倦乏力、精神不振、胃口欠佳等情况。",
            bad :"脾胃虚寒及血虚、阴虚发热者忌服。",
            usemethod : ""
          
        })
       
      }else{
        _this.setData({
       
          medname : "诺氟沙星（Norfloxacin）",
            
            suit : "本品为类白色至淡黄色结晶性粉末；无臭，味微苦；有引湿性。本品在二甲基甲酰胺中略溶，在水或乙醇中极微溶解；在醋酸、盐酸或氢氧化钠溶液中易溶。熔点 本品的熔点为218～224℃（2010年版药典二部附录ⅥC）。",
            savemethod : "遮光，密封，在干燥处保存。",
            err :  "对该品及氟喹诺酮类药过敏的患者禁用。" ,
            bad : "用于泌尿生殖道感染，包括尿路感染、前列腺炎、急慢性肾盂肾炎 消化系统感染，伤寒及其它沙门菌属所致胃肠道感染及胆囊炎等 吸道感染，如急性支气管炎、慢性支气管炎急性发作、肺炎",
            usemethod :""
          
        })
      }
    
    }
   
  },
  // 页面初始化
  init(e) {},
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
