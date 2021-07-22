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
          name: '诺氟沙星( 又名氟哌酸)',
          image:"https://www.315jiage.cn/upload/2017-07/17073014354059.jpg",
        },
        {
          child_id: 2,
          name: '阿莫西林',
          image: "http://m.360buyimg.com/pop/jfs/t23233/286/1763319067/86282/44e85bf7/5b696163N15369a1c.png"
        },
        {
          child_id: 3,
          name: '头孢氨苄',
          image: "http://www.byszc.com/upfile/2018/04/20180412143648_165.jpg"
        },
        
      ],
      two:[
        {
          child_id: 1,
          name: '维生素A',
          image: "https://www.315jiage.cn/upload/2016-11/16110317374695.jpg"
        },
        {
          child_id: 2,
          name: '维生素B1',
          image: "https://img01.hstyf360.com/group1/M00/04/30/wKgLOFpErAaAPao6AACQJfedbEM092.jpg"
        },
        {
          child_id: 3,
          name: '维生素C',
          image: "https://image.jianke.com/upload/prodimage/201608wm/201684154558782.jpg"
        },
       
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
        url: '/pages/Medicine/Meddetail/index?name=&num='+2
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
