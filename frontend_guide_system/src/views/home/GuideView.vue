<template>
    <van-nav-bar title="BJUT校园导航" :safe-area-inset-top='true' left-text="返回" left-arrow :fixed="true"
        @click-left="onClickLeftHead" />
    <div style="background-color: #3d8af2;">
        <div style="height:55px"></div>
        <!-- 粘性定位, 好像没用 -->
        <van-sticky>
            <van-cell-group inset :path_list="path_list">
                <van-cell icon="location-o">
                    <template #title>
                        <span style="font-weight:bold; font-size: larger;">起点:&nbsp;</span>
                        <span style="font-size: larger;">{{ path_list.path_num_list[0] }}</span>
                    </template>
                    <template #value>
                        等{{ path_list.path_idx_list.length }}个地点...
                    </template>
                </van-cell>
                <van-cell icon="location-o">
                    <template #title>
                        <span style="font-weight: bold; font-size: larger;">终点:&nbsp;</span>
                        <span style="font-size: larger;">{{ path_list.path_num_list.slice(-1)[0] }}</span>
                    </template>
                    <template #value>
                    </template>
                    <template #label>
                        路线全长{{ path_list.path_length }}米
                    </template>
                </van-cell>
            </van-cell-group>
        </van-sticky>
        <!-- 下方导航信息栏 -->
        <div style="margin: 4%; padding:1%; border-radius: 5px ;background-color: white; overflow: scroll;">
            <van-tabs v-model:active="active_bar" swipeable color="#3d8af2">
                <van-tab v-for="index in 3" :key="index" :bar_title="bar_title">
                    <template #title>
                        {{ bar_title[index - 1] }}
                    </template>
                    <div style="height: 420px; overflow: scroll;">
                        <!-- 结果图片 -->
                        <img :src="res_pic" style="width:100%">
                        <!-- 结果内容 -->
                        <van-steps :active="active" active-icon="success" active-color="#38f" direction="vertical"
                            @click-step="showTouchIndex">
                            <div v-for="(content, index) in path_list.path_num_list" :key="index">
                                <van-step>
                                    {{ content }}
                                    <van-icon name="arrow" />
                                </van-step>
                            </div>
                        </van-steps>
                        <!-- 结果标题 -->
                        <h3 :onChangedBarRes="onChangedBarRes">{{ onChangedBarRes }}</h3>
                    </div>
                </van-tab>
            </van-tabs>
        </div>
        <!-- 底部颜色栏, 暂时解决程序底部覆盖不全的bug -->
        <div style="background-color:#3d8af2; height: 50px;"></div>
    </div>
</template>

<script setup>
import { Toast } from 'vant'
import { ref, watch } from 'vue'
import { treeStore } from '@/stores/treeStore'
import axios from 'axios'
import qs from 'qs'

const active = ref(0)       // 高亮的结果内容行
const res_pic = ref('')     // 结果图片
const tree_st = treeStore() // 用户选择的地点列表的缓存store

const active_bar = ref(0)   // 选择出行方式的下标, 1-2-3
const bar_title = ref(["步行", "骑行", "驾车"]) // 出行方式对应的名称

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

// 不同行进方式的不同返回结果
const onChangedBarRes = ref(0)

// 监听出行方式变化
watch(active_bar, () => {
    axios.get(`/api/items/${active_bar.value}`).then(res => {
        onChangedBarRes.value = res.data["item_id"]
    })
})
</script>