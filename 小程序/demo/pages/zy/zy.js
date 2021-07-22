// pages/sort/sort.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    activeKey: 0,
  backgroundItems:[
      "http://wann12138.gitee.io/imgbed_yiban/image/background/封面.png",
      "http://wann12138.gitee.io/imgbed_yiban/image/background/adv.png",
      "http://wann12138.gitee.io/imgbed_yiban/image/background/封面.png"
  ],
  indicatorDots:true,
  autoplay:true,
  circular:true,
  interval:2000,
  duration:500,

    /* list */
    clotherItems: [
      {
        clother_id: 1,
        clother_name: "中药",
        ishaveChild: true,
        children:
        [
          /* 鞋品list */
          {
            child_id: 1,
            name: '帆布鞋',
            image:"http://wann12138.gitee.io/imgbed_yiban/image/sort/shoes/帆布鞋.jpg",
          },
          {
            child_id: 2,
            name: '篮球鞋',
            image: "http://wann12138.gitee.io/imgbed_yiban/image/sort/shoes/篮球鞋.jpg"
          },
          {
            child_id: 3,
            name: '运动鞋',
            image: "http://wann12138.gitee.io/imgbed_yiban/image/sort/shoes/运动鞋.jpg"
          },
          {
            child_id: 4,
            name: '靴子',
            image: "http://wann12138.gitee.io/imgbed_yiban/image/sort/shoes/靴子.jpg"
          }
        ]
      },
      /* 衣物list */
      {
        clother_id: 2,
        clother_name: "西药",
        ishaveChild: true,
        children:
        [
          {
            child_id: 1,
            name: 'T恤',
            image: "http://wann12138.gitee.io/imgbed_yiban/image/sort/clother/T恤.jpg"
          },
          {
            child_id: 2,
            name: '长袖衫',
            image: "http://wann12138.gitee.io/imgbed_yiban/image/sort/clother/长袖衫.jpg"
          },
          {
            child_id: 3,
            name: '羽绒服（短）',
            image: "http://wann12138.gitee.io/imgbed_yiban/image/sort/clother/羽绒服短.jpg"
          },
          {
            child_id: 4,
            name: '羽绒服（长）',
            image: "http://wann12138.gitee.io/imgbed_yiban/image/sort/clother/羽绒服长.jpg"
          },
          {
            child_id: 5,
            name: '长裤',
            image: "http://wann12138.gitee.io/imgbed_yiban/image/sort/clother/长裤.jpg"
          },
          {
            child_id: 6,
            name: '短裤',
            image: "http://wann12138.gitee.io/imgbed_yiban/image/sort/clother/短裤.jpg"
          },
        ]
      },
      {
        clother_id: 3,
        clother_name: "生物药剂",
        ishaveChild: true,
        children:
        [
          {
            child_id: 1,
            name: '床单',
            image: "http://wann12138.gitee.io/imgbed_yiban/image/sort/bedroom/床单四件套.jpg"
          },
        ]
      },
      {
        clother_id: 4,
        clother_name: "中成药",
        ishaveChild: true,
        children: [
          {
            child_id:1,
            name:"皮包",
            image:"http://wann12138.gitee.io/imgbed_yiban/image/sort/leatherware/皮具.jpg"
          }
        ]
      },
      {
        clother_id:5,
        clother_name:"其他药品",
        ishaveChild:false,
        children:[]
      }
    ],
    curNav: 1,
    curIndex: 0
  },
 
   //事件处理函数  
   switchRightTab: function (e) {
    // 获取item项的id，和数组的下标值  
    let id = e.target.dataset.id,
      index = parseInt(e.target.dataset.index);
    // 把点击到的某一项，设为当前index  
    this.setData({
      curNav: id,
      curIndex: index
    })
  },
  tabchage(e){
    console.log(e.detail);
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    let id=options.id;
    console.log(id);
    let index =parseInt(id);
    this.setData({
      curNav: id,
      curIndex: index
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

  }
})