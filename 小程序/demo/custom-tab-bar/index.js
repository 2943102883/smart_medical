Component({
  "component": true,
  data: {
    active:0,
     "color": "#000000",
    "borderStyle": "white",
    "selectedColor": "#9999FF",
    list:[
      {
        "text":"้ฆ้กต",
        "url":"/pages/index/index",
        icon:"newspaper-o"
      },
      {
        "text":"ๆ็",
        "url":"/pages/owner/owner",
        icon:"wap-home"
      }
  ]
  },
  methods: {
    onChange:function(e){
      var i = e.detail;
      wx.switchTab({
        url: this.data.list[i].url,
      })
      this.setData({
        active : i
      })
    }
  }
})
