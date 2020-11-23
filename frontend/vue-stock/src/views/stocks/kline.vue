<!--
 * @Author: your name
 * @Date: 2020-11-21 14:34:40
 * @LastEditTime: 2020-11-23 21:03:28
 * @LastEditors: Please set LastEditors
 * @Description: In User Settings Edit
 * @FilePath: \vue-admin-template\src\views\stocks\chart_raw.vue
-->
<template>

  <div class="app-container" :style="{margin:'0px',padding:'0px',height:'90vh'}" ref="mychart">
      <el-select v-model="value" placeholder="请选择">
        <el-option
        v-for="item in options"
        :key="item.value"
        :label="item.label"
        :value="item.value">
        </el-option>
    </el-select>
    <el-button size="middle" type="primary" @click="start_task()" :disabled="cal_btn" plain>获取</el-button>
      <div id="kline" :style="{width: '100%',height:'87vh', 'margin':'0px'}"></div>
  </div>
</template>

<script>
import { showBarData } from '@/api/kLine'
// import { kdata } from './data.js'
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
  mounted(){
      this.stock_chart && this.stock_chart.resize()
    // this.drawLine();
    // setTimeout(() => {
    //     this.resize()
    // }, 0) 
    // window.onresize = this.resize
  },
  data() {
    return {
        stock_chart:null,
        cal_btn:false,
        time: null,
        trade: null,
        order: null,
        ohlc: null,
        options: [{
          value: '1min',
          label: '1min'
        }, {
          value: '5min',
          label: '5min'
        }, {
          value: '10min',
          label: '10min'
        }],
        value: '1min',
        activeName2: 'first',
        firstLoad: {
            'first': true,
            'second': true,
            'third': true
        },
        tabResize: {
            'first': false,
            'second': false
        },
    }
  },
  created() {
    this.fetchData(this.value)
    if (this.firstLoad[this.activeName2]) {
            this.firstLoad[this.activeName2] = false
        }
  },
  methods: {
      start_task(){
          console.log(this.value)
        this.fetchData(this.value)
      },
    fetchData(freq) {
      // this.listLoading = true
        showBarData(freq).then(response => {
        // this.list = response.data.items
        // this.listLoading = false
        // console.log('raw_data:', response.data)
        var data =response.data['data']
        // console.log('data:', data)
        this.time=data['time']
        this.trade=data['trade_volume']
        this.order=data['order_volume']
        this.ohlc=data['ohlc']
        this.draw_k()
      })
    },
    generateOHLC(count) {
        var data = [];
        
        

        var xValue = +new Date(2011, 0, 1);
        var minute = 60 * 1000;
        var baseValue = Math.random() * 12000;
        var boxVals = new Array(4);
        var dayRange = 12;

        for (var i = 0; i < count; i++) {
            baseValue = baseValue + Math.random() * 20 - 10;

            for (var j = 0; j < 4; j++) {
                boxVals[j] = (Math.random() - 0.5) * dayRange + baseValue;
            }
            boxVals.sort();

            var openIdx = Math.round(Math.random() * 3);
            var closeIdx = Math.round(Math.random() * 2);
            if (closeIdx === openIdx) {
                closeIdx++;
            }
            var volumn = boxVals[3] * (1000 + Math.random() * 500);

            // ['open', 'close', 'lowest', 'highest', 'volumn']
            // [1, 4, 3, 2]
            data[i] = [
                this.$echarts.format.formatTime('yyyy-MM-dd\nhh:mm:ss', xValue += minute),
                boxVals[openIdx].toFixed(2), // open
                boxVals[3].toFixed(2), // highest
                boxVals[0].toFixed(2), // lowest
                boxVals[closeIdx].toFixed(2),  // close
                volumn.toFixed(0),
                // volumn.toFixed(0)+100,
                getSign(data, i, +boxVals[openIdx], +boxVals[closeIdx], 4) // sign
            ];
            console.log(data[i])
        }

        return data;

        function getSign(data, dataIndex, openVal, closeVal, closeDimIdx) {
            var sign;
            if (openVal > closeVal) {
                sign = -1;
            }
            else if (openVal < closeVal) {
                sign = 1;
            }
            else {
                sign = dataIndex > 0
                    // If close === open, compare with close of last record
                    ? (data[dataIndex - 1][closeDimIdx] <= closeVal ? 1 : -1)
                    // No record of previous, set to be positive
                    : 1;
            }

            return sign;
        }
    },
    draw_k(){
        this.stock_chart = this.$echarts.init(document.getElementById('kline'))
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
            
            
			series: [{
					name: 'K线周期图表',
					type: 'candlestick',
                    data: this.ohlc,
                    // data: data.datas,
					barWidth: '50%',
					large: true,
					largeThreshold: 100,
					itemStyle: {
						normal: {
							color: upColor, //fd2e2e  ff4242
							color0: downColor,
							borderColor: upColor,
							borderColor0: downColor,
							//opacity:0.8
						}
					},
                }, 
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
			]
        };
        
        this.stock_chart.setOption(option);
        // console.log(myChart)
    },
    calcMACD(short,long,mid,data,field){
        var i,l,dif,dea,macd,result;
        result={};
        macd=[];
        dif=calcDIF(short,long,data,field);
        dea=calcDEA(mid,dif);
        for(i=0,l=data.length;i<l;i++){
            macd.push(((dif[i]-dea[i])*2).toFixed(3));
        }
        result.dif=dif;
        result.dea=dea;
        result.macd=macd;
        return result;
    },
    resize () {
        let h = document.body.clientHeight
        let chartHeight = (h - 210) + 'px'
        if (this.activeName2 === 'second') {            
            this.$nextTick(() => {
                this.$refs.mychart.style.height = chartHeight
            })
            if (!this.firstLoad[this.activeName2]) {
                this.tabResize['first'] = true
            }
        } else if (this.activeName2 === 'first') {
            // this.$nextTick(() => {
            //     this.$refs.mix_plot.style.height = chartHeight
            // })
            if (!this.firstLoad[this.activeName2]) {
                this.tabResize['second'] = true
            }                   
        } else {
            this.tabResize['first'] = true
            this.tabResize['second'] = true
        }
    },
    
  }
}
</script>
