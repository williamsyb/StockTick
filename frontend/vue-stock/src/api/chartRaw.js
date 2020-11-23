/*
 * @Author: your name
 * @Date: 2020-11-21 14:14:53
 * @LastEditTime: 2020-11-22 11:54:53
 * @LastEditors: Please set LastEditors
 * @Description: In User Settings Edit
 * @FilePath: \vue-admin-template\src\api\charts.js
 */
import request from '@/utils/request'

export function showRawData() {
  return  request({
    url: '/api/v1/show_raw_data',
    method: 'get',
    headers: {
      'Content-Type': 'application/json'
    },
  })
}

