import { defineStore } from "pinia"

export const lnglatStore = defineStore('lnglatStore', {
    // 相当于 data
    state: () => {
        return {
            lnglat_converted_list: null,     // 总list
            current_start: null,            // 映射后下标
            current_end: null,
            path_num_list: null,            // 结果名字list, 用的是映射前下标
            raw_start: null,                // 映射前下标
            raw_end: null
        }
    },
    // 相当于 methods
    actions: {

    },
    // 相当于 computed 调用时可直接当作属性
    getters: {

    }
})