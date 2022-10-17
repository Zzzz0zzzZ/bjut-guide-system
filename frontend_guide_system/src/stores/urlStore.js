import { defineStore } from "pinia"

export const urlStore = defineStore('urlStore', {
    state: () => {
        return {
            my_url: 'http://127.0.0.1:8000',
            todolist_url: 'http://152.136.154.181:8060'
        }
    },
})