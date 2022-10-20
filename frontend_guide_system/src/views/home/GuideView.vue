<template>
    <van-nav-bar title="BJUT校园导航" :safe-area-inset-top='true' left-text="返回" left-arrow @click-left="onClickLeftHead" />
    <!-- 结果标题 -->
    <h3 v-if="active" :path_list="path_list">&nbsp;&nbsp;{{ "->共选择" + active + "个地点, " + "路线总长度: " +
    path_list.path_length + "米" }}
    </h3>
    <!-- 结果内容 -->
    <van-steps :active="active" active-icon="success" active-color="#38f" direction="vertical"
        @click-step="showTouchIndex">
        <div v-for="(content, index) in path_list.path_num_list" :key="index">
            <van-step>
                {{content}}
            </van-step>
        </div>
    </van-steps>
    <!-- 结果图片 -->
    <img :src="res_pic" style="width:100%">
</template>

<script setup>
import { Toast } from 'vant'
import { ref } from 'vue'
import { treeStore } from '@/stores/treeStore'
import axios from 'axios'
import qs from 'qs'

const active = ref(0)       // 高亮的结果内容行
const res_pic = ref('')     // 结果图片
const tree_st = treeStore() // 用户选择的地点列表的缓存store

// 接受后端返回的路线结果
const path_list = ref({
    path_idx_list: [],
    path_num_list: [],
    path_length: 0
})

// 返回上一级
const onClickLeftHead = () => history.back()

// 根据treeStore内容，获取路线结果
axios({
    method: 'POST',
    url: '/api/guide',
    data: qs.stringify({
        "bias": 0,
        "num": tree_st.selected_list.length
    })
}).then(res => {
    // 步骤条 active 下标，默认最后一个
    active.value = tree_st.selected_list.length
    // 获取数据
    path_list.value.path_idx_list = res.data.path_idx_list
    path_list.value.path_num_list = res.data.path_num_list
    path_list.value.path_length = res.data.path_length
    // 清空treeStore缓存的值
    tree_st.selected_list = []
    // 请求[结果图片]
    axios({
        method: 'POST',
        url: '/api/result',
        responseType: 'blob'
    }).then(res => {
        let blob = new Blob([res.data])
        let url = window.URL.createObjectURL(blob)
        res_pic.value = url
    })
})

Toast.loading({
    message: '加载中...',
    forbidClick: true,
    duration: 500
})

// 展示用户点击的行的下标，调试用
const showTouchIndex = (idx) => {
    Toast(idx)
}
</script>