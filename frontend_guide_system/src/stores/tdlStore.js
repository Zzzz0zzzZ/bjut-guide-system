import { defineStore } from "pinia"
import { Toast } from "vant"
import { SHA256 } from '@/utils/sha256'
import axios from 'axios'

export const tdlStore = defineStore('tdlStore', {
    state: () => {
        return {
            token: null,
            count_total: null,         // 帖子总数
            count_finish: null,        // 帖子完成数
        }
    },
    actions: {
        updateCount() {
            axios({
                method: 'POST',
                url: '/todolist/login',
                data: ({
                    "username": "课设",
                    "password": SHA256("123")
                })
            }).then(res => {
                if (res.data.token === undefined) {
                    Toast({
                        message: "获取待办\n事项失败"
                    })
                } else {
                    this.token = res.data.token
                }
                axios({
                    method: "GET",
                    url: '/todolist/count_finish/13',
                    headers: ({
                        "token": this.token
                    })
                }).then(res => {
                    this.count_finish = parseInt(res.data)
                })
                axios({
                    method: "GET",
                    url: '/todolist/count_total/13',
                    headers: ({
                        "token": this.token
                    })
                }).then(res => {
                    this.count_total = parseInt(res.data)
                })
            })

        }
    },
    getters: {
        getPortion(state) {
            if (state.count_total === 0) {
                return 100
            }
            else if (state.count_finish === 0) {
                return 0
            }
            else {
                return parseInt((state.count_finish / state.count_total).toFixed(2) * 100)
            }
        },
        // 获取待办事项总数
        getListCount(state) {
            return state.count_total - state.count_finish
        }
    }
})