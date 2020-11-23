/*
 * @Author: your name
 * @Date: 2020-11-22 20:22:33
 * @LastEditTime: 2020-11-22 21:21:43
 * @LastEditors: Please set LastEditors
 * @Description: In User Settings Edit
 * @FilePath: \vue-stock\src\api\summary.js
 */
import request from '@/utils/request'

export function showStatistic(data) {
  return request({
    url: '/api/v1/show_statistic?start_time=' + data['start_time']+"&end_time="+data['end_time'],
    method: 'get',
    headers: {
      'Content-Type': 'application/json'
    },
    // data:data
    
  })
}