# StockTick
## 股票收益日行情前后端全栈项目

> 项目描述

本项目采用前后端分离技术，将股票日内行情数据K线图与价量数据通过浏览器显示，原始数据时间精度为毫秒级，
项目分别提供了1分钟、5分钟与10分钟的聚合数据，同时也对订单量、成交量做了类似的处理与展示。

> 技术方案
### 前端部分
前端使用Vue+ElementUi+Echart完成，请求部分使用了Axios发送。

### 后端部分
后端使用Flask+Gunicorn+Nginx+Redis，数据库方面没有使用Mysql，使用了简单的Sqlite3.

> 项目部署

本项目部署在阿里云， 地址：http://139.196.20.149

> 项目展示

![image](https://github.com/williamsyb/StockTick/master/screenshot/stockTick01.png)
![image](https://github.com/williamsyb/StockTick/master/screenshot/stockTick02.png)
