/*
 * @Author: your name
 * @Date: 2020-11-21 16:54:55
 * @LastEditTime: 2020-11-21 22:06:23
 * @LastEditors: Please set LastEditors
 * @Description: In User Settings Edit
 * @FilePath: \vue-stock\src\api\user.js
 */
import request from '@/utils/request'

export function login(data) {
  // console.log(data)
  // var qs=require('qs')
  // databody=qs.stringify(data)
  // console.log(databody)
  return request({
    url: '/auth/oauth/token',
    method: 'post',
    data,
    headers:{'Content-Type': 'application/x-www-form-urlencoded'}
  })
}

// export function getInfo(token) {
//   return request({
//     url: '/vue-admin-template/user/info',
//     method: 'get',
//     params: { token }
//   })
// }

// export function logout() {
//   return request({
//     url: '/vue-admin-template/user/logout',
//     method: 'post'
//   })
// }
