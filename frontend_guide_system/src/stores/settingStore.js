import { defineStore } from "pinia"

export const settingStore = defineStore('settingStore', {
    // 相当于 data
    state: () => {
        return {
            user_settings: null     // 用户[自动舍弃算法]偏好： 0 --- '10'  1 --- '15'  2 --- '20'
        }
    },
    // 相当于 methods
    actions: {

    },
    // 相当于 computed 调用时可直接当作属性
    getters: {

    }
})