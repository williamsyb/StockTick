<!--
 * @Author: your name
 * @Date: 2020-11-21 14:34:40
 * @LastEditTime: 2020-11-23 20:47:41
 * @LastEditors: Please set LastEditors
 * @Description: In User Settings Edit
 * @FilePath: \vue-admin-template\src\views\stocks\chart_raw.vue
-->
<template>
  
  <div class="app-container" :style="{margin:'0px',padding:'0px',height:'90vh'}" ref="mychart" >
        <h2 :style="{width: '100%', 'margin':'5px', 'marget-left':'10px'}">
          最高价:{{max_price}},最低价:{{min_price}},总委托量:{{total_order}},总成交量:{{total_trade}}, 总时间：{{total_second}}秒
        </h2>
      <div id="myChart" style="width: 100%;height:87vh; margin:0; margin-top:0"></div>
  </div>
</template>

<script>
import { showRawData } from '@/api/chartRaw'
import { showStatistic } from '@/api/summary'
import { mapGetters } from 'vuex'
export default {
  filters: {
    statusFilter(status) {
      const statusMap = {
        published: 'success',
        draft: 'gray',
        deleted: 'danger'
      }
      return statusMap[status]
    }
  },
  mounted(){
      this.stock_chart && this.stock_chart.resize()
  },
  computed: {
    ...mapGetters([
      'sidebar',
    ])
  },
  activated(){
      this.stock_chart && this.stock_chart.resize()
  },
  watch:{
      'sidebar.opened'(val ){
          console.log(val)
          console.log(this.stock_chart)
        setTimeout(_ => {
            this.stock_chart && this.stock_chart.resize()
        }, 200)
      }
  },
  data() {
    return {
      stock_chart:null,
      max_price:'0',
      min_price:'0',
      total_order:'0',
      total_trade:'0',
      total_second:0,
      list: null,
      price : null,
      order: null,
      trade: null,
      time: null,
      // listLoading: true
    }
  },
  created() {
    this.fetchData()
    // showStatistic({"start_time":"2020-11-20 09:30:03","end_time":"2020-11-20 09:30:16"}).then(response => {
    //             var data = response.data;
    //             console.log(data)
    //         });
  },
  methods: {
    fetchData() {
        this.listLoading = true
      // this.price = [12,234,43,2,1]
        showRawData().then(response => {
        var data = response.data['data']
        // console.log(data)
        console.log('------------------------------------')
          
        // console.log(data['data'])
        // console.log('------------------------------------')
        // console.log(JSON.parse(data)['data'])
        this.price=data['price']
        // this.price = [12,234,43,2,1]
        this.order=data['OrderVolume']
        this.trade=data['TradeVolume']
        this.time=data['time']
        // console.log(time)
        // console.log(orderVol)
        this.draw_raw();
      }) 
    },
    draw_raw(){
        this.stock_chart = this.$echarts.init(document.getElementById('myChart'),{width:'auto'})
        
        var ma5Color = "#39afe6";
        var ma10Color = "#da6ee8";
        var ma20Color = "#ffab42";
        var ma30Color = "#00940b";
        var bgColor = "#1f212d";//背景
        var upColor="#F9293E";//涨颜色
        var downColor="#00aa3b";//跌颜色

        // ma  颜色
        var ma5Color = "#39afe6";
        var ma10Color = "#da6ee8";
        var ma20Color = "#ffab42";
        var ma30Color = "#00940b";
        
        // console.log(kdata)
        // var data = this.splitData(kdata);
        // console.log('data.datas:', data.datas.slice(1,10))
        var option={
			tooltip: { //弹框指示器
				trigger: 'axis',
				axisPointer: {
					type: 'cross'
				}
			},
			legend: { //图例控件,点击图例控制哪些系列不显示
				icon: 'rect', 
				type:'scroll',
				itemWidth: 14,
				itemHeight: 2,
				left: 0,
				top: '-0.5%',  
				animation:true,
				textStyle: {
					fontSize: 12,
					color: '#0e99e2'
				},
				pageIconColor:'#0e99e2'
			},
			axisPointer: {
				show: true
			},
			color: [ma5Color, ma10Color, ma20Color, ma30Color],
			grid: [{
				id: 'gd1',
				left: '0%',
				right: '1%',
				height: '60%', //主K线的高度,
				top: '5%'
			}, {
				left: '0%',
				right: '1%',
				top: '66.5%',
				height: '10%' //交易量图的高度
			}, {
				left: '0%',
				right: '1%',
				top: '80%', //MACD 指标
                height: '14%',
                // bottom:400
			}],
			xAxis: [ //==== x轴
				{ //主图
					type: 'category',
                    data: this.time,
                    // data: data.times,
					scale: true,
					boundaryGap: false,
					axisLine: {
						onZero: false
					},
					axisLabel: { //label文字设置
						show: false
					},
					splitLine: {
						show: false,
						lineStyle: {
							color: '#3a3a3e'
						}
					},
					splitNumber: 10,
					min: 'dataMin',
					max: 'dataMax'
				}, { //交易量图
					type: 'category',
					gridIndex: 1,
					data: this.time,
					axisLabel: { //label文字设置
						color: '#9b9da9',
						fontSize: 10
					},
				}, { //幅图
					type: 'category',
					gridIndex: 2,
					data:  this.time,
					axisLabel: {
						show: false
					}
				}
			],
			yAxis: [ //y轴
				{ //==主图
					scale: true,
					z:4,
					axisLabel: { //label文字设置
						color: '#c7c7c7',
						inside: true, //label文字朝内对齐
					},
					splitLine: { //分割线设置
						show: false,
						lineStyle: {
							color: '#181a23'
						}
					},
				}, { //交易图
					gridIndex: 1, splitNumber: 3, z:4,
					axisLine: {
						onZero: false
					},
					axisTick: {
						show: false
					},
					splitLine: {
						show: false
					},
					axisLabel: { //label文字设置
						color: '#c7c7c7',
						inside: true, //label文字朝内对齐 
						fontSize: 8
					},
				}, { //幅图
					z:4, gridIndex: 2,splitNumber: 4,
					axisLine: {
						onZero: false
					},
					axisTick: {
						show: false
					},
					splitLine: {
						show: false
					},
					axisLabel: { //label文字设置
						color: '#c7c7c7',
						inside: true, //label文字朝内对齐 
						fontSize: 8
					},
				}
			],
			dataZoom: [{
					type: 'slider',
					xAxisIndex: [0, 1, 2], //控件联动
					start: 100,
					end: 80,
					throttle: 10,
					top: '94%',
					height: '6%',
					borderColor: '#696969',
					textStyle: {
						color: '#dcdcdc'
					},
					handleSize: '90%', //滑块图标
					handleIcon: 'M10.7,11.9v-1.3H9.3v1.3c-4.9,0.3-8.8,4.4-8.8,9.4c0,5,3.9,9.1,8.8,9.4v1.3h1.3v-1.3c4.9-0.3,8.8-4.4,8.8-9.4C19.5,16.3,15.6,12.2,10.7,11.9z M13.3,24.4H6.7V23h6.6V24.4z M13.3,19.6H6.7v-1.4h6.6V19.6z',
					dataBackground: {
						lineStyle: {
							color: '#fff'
						}, //数据边界线样式
						areaStyle: {
							color: '#696969'
						} //数据域填充样式
					}
				},
				// 		{
				// 			type: 'inside',
				// 			xAxisIndex: [0,1,2],//控件联动
				// 		},
			],
			animation: true, //禁止动画效果
			backgroundColor: bgColor,
            blendMode: 'source-over',
            
            
			series: [
        // {
        //     name: '股价',
        //     type: 'line',
        //     data: this.price,
        //               // data: data.datas,
        //     // barWidth: '50%',
        //     large: true,
        //     largeThreshold: 100,
        //     itemStyle: {
        //       normal: {
        //         color: upColor, //fd2e2e  ff4242
        //         color0: downColor,
        //         borderColor: upColor,
        //         borderColor0: downColor,
        //         //opacity:0.8
        //       }
        //     },
        //   }, 
          {
            name: 'TradeVolume',
            type: 'bar',
            xAxisIndex: 1,
            yAxisIndex: 1,
            data: this.trade,
            barWidth: '50%',
            large: true,
            largeThreshold: 100,
            itemStyle: {
              normal: {
                color: function(params) {
                                  
                                  var colorList;
                                  colorList = downColor;
                  // if (data.datas[params.dataIndex][1] > data.datas[params.dataIndex][0]) {
                  // 	colorList = downColor;
                  // } else {
                  // 	colorList = downColor;
                  // }
                  return colorList;
                },
              }
            }
          }, 
                {
					name: 'OrderVolume',
					type: 'bar',
					xAxisIndex: 2,
					yAxisIndex: 2,
                    // data: macd.macd,
          data: this.order,
          barWidth: '50%',
          large: true,
					largeThreshold: 100,
					itemStyle: {
						normal: {
							color: function(params) {
								var colorList;
								if (params.data >= 0) {
									colorList = upColor;
								} else {
									colorList = downColor;
								}
								return colorList;
							},
						}
					}
                }, 
                {
					name: '股价',
					type: 'line',
					data: this.price,
					smooth: true,
					symbol: "none", //隐藏选中时有小圆点
					lineStyle: {
						normal: {
							opacity: 0.8,
							color: '#39afe6',
							width: 1
						}
					},
				},
				// {
				// 	name: 'MA10',
				// 	type: 'line',
				// 	data: this.calculateMA(10,data),
				// 	smooth: true,
				// 	symbol: "none",
				// 	lineStyle: { //标线的样式
				// 		normal: {
				// 			opacity: 0.8,
				// 			color: '#da6ee8',
				// 			width: 1
				// 		}
				// 	}
				// },
				// {
				// 	name: 'MA20',
				// 	type: 'line',
				// 	data: this.calculateMA(20,data),
				// 	smooth: true,
				// 	symbol: "none",
				// 	lineStyle: {
				// 		opacity: 0.8,
				// 		width: 1,
				// 		color: ma20Color
				// 	}
				// },
				// {
				// 	name: 'MA30',
				// 	type: 'line',
				// 	data: this.calculateMA(30,data),
				// 	smooth: true,
				// 	symbol: "none",
				// 	lineStyle: {
				// 		normal: {
				// 			opacity: 0.8,
				// 			width: 1,
				// 			color: ma30Color
				// 		}
				// 	}
                // }, 
                
                // {
				// 	name: 'DIF',
				// 	type: 'line',
				// 	symbol: "none",
				// 	xAxisIndex: 2,
				// 	yAxisIndex: 2,
                //     // data: macd.dif,
                //     data:[1,2,4,6,7,9],
				// 	lineStyle: {
				// 		normal: {
				// 			color: '#da6ee8',
				// 			width: 1
				// 		}
				// 	}
                // },
                // {
				// 	name: 'DEA',
				// 	type: 'line',
				// 	symbol: "none",
				// 	xAxisIndex: 2,
				// 	yAxisIndex: 2,
                //     // data: macd.dea,
                //     data:[1,2,4,6,7,9],
				// 	lineStyle: {
				// 		normal: {
				// 			opacity: 0.8,
				// 			color: '#39afe6',
				// 			width: 1
				// 		}
				// 	}
				// }
			]
        };
        
        this.stock_chart.setOption(option);
        // let vm=this
        this.stock_chart.on('dataZoom',  (params) =>{
            var option = this.stock_chart.getOption();
            // console.log(option.dataZoom[0].startValue, option.dataZoom[0].endValue);
            
            // console.log(params)
            var startX=option.dataZoom[0].startValue;
            var endX=option.dataZoom[0].endValue;
            var axis = this.stock_chart.getModel().option.xAxis[0];
            // console.log(axis.data[])
            var  startTime=axis.data[startX];
            var endTime=axis.data[endX];
            console.log(startTime);//区间开始值："17-11-06"
            console.log(endTime);//区间结束值："17-11-08"
            
            showStatistic({'start_time':startTime, 'end_time':endTime}).then(response => {
                var data = response.data;
                console.log(data)
                // this.max_price=data.data['max_price']
                // console.log(this)
                this.max_price=data.data['max_price']
                this.min_price=data.data['min_price']
                this.total_order=data.data['total_order']
                this.total_trade=data.data['total_trade']
                this.total_second = endX-startX
            });
        });
    },
    drawLine(){
        // 基于准备好的dom，初始化echarts实例
        let myChart = this.$echarts.init(document.getElementById('myChart'))

        let xs = this.time;
        // let xs = ['2010', '2011', '2012','2013', '2014', '2015', '2016', '2017', '2018', '2019']
        var option = {
            tooltip: {
                trigger: 'axis',
                axisPointer: {
                    type: 'cross',
                    crossStyle: {
                        color: '#999'
                    }
                }
            },
            color: ['pink', 'green', '#a9b0d3', '#476fd4'],
            grid: [
                {
                    x: '7%',
                    y1: '7%',
                    height: '40%',
                    left: '10%'
                },
                {
                    x: '5%',
                    y2: '5%',
                    height: '35%',
                    left: '10%',
                    //bottom: '5%'
                }
            ],
            xAxis: [
                {
                    show: false, //隐藏了x轴
                    type: 'category',
                    gridIndex: 0, //对应前面grid的索引位置（第一个）
                    axisTick: {
                        show: false
                    },
                    axisLabel: {
                        //interval:showNum,  //x轴显示的数量，我这里是动态算的
                    },
                    axisPointer: {
                        // show: false
                    },
                    data: xs,
                },
                {
                    type: 'category',
                    gridIndex: 1, //对应前面grid的索引位置（第二个）
                    axisTick: {
                        show: false
                    },
                    axisLabel: {
                        //interval:showNum,
                    },
                    data: xs,
                }
            ],
            //y轴，不管有几个x轴，几个y轴，或者图，只要找到他对应的grid图的序号索引就可以精准匹配

            yAxis: [
                {
                    type: 'value',
                    gridIndex: 1, //对应前面grid的索引位置（第二个）
                    name: '订单量/成交量',
                    //nameLocation:'end',
                    splitLine: {
                        show: true
                    },
                    top: 50,
                    nameLocation: 'middle',
                    nameTextStyle: {
                        padding: 50
                    },
                    position: 'left',
                    axisLine: {
                        show: false,
                    },
                    axisLabel: {
                        formatter: '{value}'
                    }
                },
                {
                    show: false,
                    type: 'value',
                    gridIndex: 1,
                    nameLocation: 'middle',
                    name: '订单量/成交量',
                    nameTextStyle: {
                        padding: 25
                    },
                    splitLine: {
                        show: true
                    },
                    position: 'left',
                    axisLine: {
                        show: false,
                    },
                    axisLabel: {
                        formatter: '{value}'
                    }
                },
                {
                    type: 'value',
                    gridIndex: 0,
                    name: '股价',
                    nameTextStyle: {
                        padding: 50
                    },
                    position: 'left',
                    nameLocation: 'middle',
                    splitLine: {
                        show: true
                    },
                    //nameLocation: 'start',//y轴name的位置
                    //inverse: true,
                    axisLine: {
                        show: false,
                    },
                    axisLabel: {
                        formatter: '{value}',
                        textStyle: {
                            fontSize: 12 //y轴坐标轴上的字体大小
                        }

                    },
                },
            ],
            series: [{
                    name: '股价',
                    // type:'bar',
                    // name: "累产气量"
                    type: "line",
                    xAxisIndex: 0,
                    yAxisIndex: 2,

                    data: this.price
                },
                {
                    type: 'bar',
                    stack: 'OrderVolume',
                    name:'OrderVolume',
                    // barWidth: 30,
                    xAxisIndex: 1, 
                    yAxisIndex: 0,
                    data: this.order
                },
                {
                    type: 'bar',
                    stack: 'TradeVolume',
                    name:'TradeVolume',
                    // barWidth: 30,
                    xAxisIndex: 1,
                    yAxisIndex: 0,
                    data: this.trade
                }
            ]
        };
        
        myChart.setOption(option);
    }
  
  }
}
</script>
