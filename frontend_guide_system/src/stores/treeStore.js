import { defineStore } from "pinia"

export const treeStore = defineStore('treeStore', {
    // 相当于 data
    state: () => {
        return {
            selected_list: []
        }
    },
    // 相当于 methods
    actions: {
        saveSelectChange(activeId) {
            this.selected_list = activeId.value
        }
    },
    // 相当于 computed 调用时可直接当作属性
    getters: {

    }
})