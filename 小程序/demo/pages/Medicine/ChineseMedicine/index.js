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
    one:[
      /* 鞋品list */
      {
        child_id: 1,
        name: '石膏',
        image:"https://p1.ssl.qhimg.com/t01056b5d6ca14feeba.jpg",
      },
      {
        child_id: 2,
        name: '寒水石',
        image: "https://tgi1.jia.com/115/005/15005981.jpg"
      },
      {
        child_id: 3,
        name: '知母',
        image: "http://image.yaosuce.com/upload/test/normal/2019/04/24/1556085572290402.png"
      },
      {
        child_id: 4,
        name: '芦根',
        image: "http://file.cnkang.com/cnkfile1/M00/15/EA/o4YBAFmHx_-AJ6cHAACgP7NRVMw86.jpeg"
      }
    ],
    two:[
      {
        child_id: 1,
        name: '小蓟',
        image: "https://img.xjlz365.com/zhongcaoyao/img_list/2018080815198524.jpg"
      },
      {
        child_id: 2,
        name: '大蓟',
        image: "http://file.cnkang.com/cnkfile1/M00/16/75/ooYBAFmlMVaAXQ9BAAJX8VmQQdc08.jpeg"
      },
      {
        child_id: 3,
        name: '地榆',
        image: "http://www.tcmdoc.cn/Images_ZhongYaoXue/diyu-YinPian.jpg"
      },
      {
        child_id: 4,
        name: '槐花（附药：槐角）',
        image: "https://img.ys991.com/uploads/allimg/20190615/1560606944697932.jpg"
      },
      {
        child_id: 5,
        name: '侧柏叶',
        image: "https://www.songmiao.net/uploads/allimg/190223/1-1Z223133522.jpg"
      },
      {
        child_id: 6,
        name: '白茅根',
        image: "http://yisheng.12120.net/uploads/allimg/151104/19-1511041J93M39.png"
      },
    ],
    three:[
      {
        child_id:1,
        name:"麻黄",
        image:"http://pic349.nipic.com/file/20201208/31186696_160440379085_2.jpg"
      }
    ],

    curNav: 1,
    curIndex: 0
  },
  // 数据监听器
  observers: {},
  // 组件方法
  methods: {
    init() {},
    tabchage(e){
      var _this = this;
      _this.setData({
        activeKey : e.detail
      })
    },
   
    detail(){
      wx.navigateTo({
        url: '/pages/Medicine/Meddetail/index?name=&num='+1
      })
    }
  
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
