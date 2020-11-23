/*
 * @Author: your name
 * @Date: 2020-11-21 14:17:22
 * @LastEditTime: 2020-11-22 17:11:46
 * @LastEditors: Please set LastEditors
 * @Description: In User Settings Edit
 * @FilePath: \vue-admin-template\src\api\kLine.js
 */

import request from '@/utils/request'

export function showBarData(freq) {
  return request({
    url: '/api/v1/show_bar_data/'+freq,
    method: 'get',
    headers: {
      'Content-Type': 'application/json'
    },
    // freq
    
  })
}