<template>
    <van-nav-bar title="BJUT校园导航" :safe-area-inset-top='true' left-text="返回" left-arrow :fixed="true"
        @click-left="onClickLeftHead" />
    <!-- 蓝色大背景 -->
    <div style="background-color: #3d8af2; height: 100%; position: absolute; top: 1%%; width: 100%;">
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
        <div
            style="margin: 4%; padding:1%; border-radius: 5px ;background-color: white; overflow: scroll; height: 66%;">
            <van-tabs v-model:active="active_bar" swipeable color="#3d8af2">
                <van-tab v-for="index in 2" :key="index" :bar_title="bar_title">
                    <!-- index从1开始的, 所以为了与数组起始下标0对应, 需要减1 -->
                    <template #title>
                        {{ bar_title[index - 1] }}
                    </template>
                    <div style="height: 70%; overflow: scroll;">
                        <!-- 结果标题 -->
                        <h4 :onChangedBarRes="onChangedBarRes" style="margin-top: 8px; margin-bottom: 8px;">
                            {{ "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
                                    + bar_title[index - 1]
                                    + "全程耗时:&nbsp;"
                                    + onChangedBarRes
                                    + "分钟"
                            }}
                        </h4>
                        <!-- 提示文字 -->
                        <h5 style="margin-top: 8px; margin-bottom: 8px;">
                            {{ "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
                                    + "(点击列表地点查看:真实地图&详细路线)"
                            }}
                        </h5>
                        <!-- 结果内容 -->
                        <!-- 宽度90%, 美观 -->
                        <van-steps :active="active" active-icon="down" inactive-icon="down" active-color="#38f"
                            direction="vertical" @click-step="showTouchIndex" style="width: 90%;">
                            <div v-for="(content, index) in path_list.path_num_list" :key="index" style="width:100%">
                                <van-step style="padding:0px; border-bottom: dashed lightgrey; border-radius: 5px;">
                                    <van-cell center>
                                        <template #title>{{ content }}</template>
                                        <template #value>
                                            <span v-if="index === 0">出发时间:</span>
                                            <span
                                                v-else-if="index === path_list.path_num_list.length - 1">预计到达时间:</span>
                                            <span v-else>预计途经时间:</span>
                                            <!-- 绑定的time是一个数值, 单位是毫秒; 通过定义format可以规定时间显示格式 -->
                                            <van-count-down v-if="index !== 0" :time="arrival_time_show[index]"
                                                :auto-start="false" format="HH:mm" />
                                            <van-count-down v-else :time="arrival_time_show[0]" :auto-start="false"
                                                format="HH:mm" />
                                        </template>
                                        <template #label>
                                            <van-tag v-if="index === 0" type="success">{{ "起点" }}</van-tag>
                                            <van-tag v-else-if="index === path_list.path_num_list.length - 1"
                                                type="danger">
                                                {{ "终点" }}
                                            </van-tag>
                                            <van-tag v-else type="primary">{{ "途经点" + index }}</van-tag>
                                        </template>
                                    </van-cell>
                                </van-step>
                            </div>
                        </van-steps>
                        <!-- 结果图片 -->
                        <h5 v-if="showPicTitleFlag" style="margin-top: 8px; margin-bottom: 8px;">
                            {{ "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
                                    + "路线全程示意图(点击上方列表查看详细路线)"
                            }}
                        </h5>
                        <img :src="res_pic" style="width:100%">
                    </div>
                </van-tab>
            </van-tabs>
        </div>
    </div>
</template>

<script setup>
import { Toast } from 'vant'
import { ref, watch } from 'vue'
import { treeStore } from '@/stores/treeStore'
import { lnglatStore } from '@/stores/lnglatStore'
import { settingStore } from '@/stores/settingStore'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import qs from 'qs'

const base_time = ref(0)    // 当前时间
const arrival_time_show = ref([]);  // 到底时间, 数组, 第一个值是当前时间, 后面为到底第一个、第二个...的时间

const active = ref(0)       // 高亮的结果内容行
const res_pic = ref('')     // 结果图片
const tree_st = treeStore() // 用户选择的地点列表的缓存store
const lnglat_st = lnglatStore() // lntlat_list, 保存结果用于高德导航
const setting_st = settingStore()   // 自动舍弃算法-用户设置

const active_bar = ref(0)   // 选择出行方式的下标, 1-2-3
const bar_title = ref(["推荐路线", "完整路线", "驾车"]) // 出行方式对应的名称

const date = new Date()

// 如果没有数据/路径错误, 进行路由重定向    如果正确，就展示加载图标
const route = useRoute()
const router = useRouter()
if (route.path !== '/' && tree_st.selected_list.length === 0) {
    router.push({
        name: 'home'
    })
}
else {
    let msg = ref('规划中...')
    if (tree_st.selected_list.length > 10 && setting_st.user_settings == '0') {
        msg.value = '规划中...\n选择地点过多\n将为您\n自动舍弃'
    }
    else if (tree_st.selected_list.length > 15 && setting_st.user_settings == '1') {
        msg.value = '规划中...\n选择地点过多\n将为您\n自动舍弃'
    }
    else if (tree_st.selected_list.length > 20 && setting_st.user_settings == '2') {
        msg.value = '规划中...\n选择地点过多\n将为您\n自动舍弃'
    }
    Toast.loading({
        message: msg.value,
        forbidClick: true,
        duration: 0    // 0为一直展示, 知道axios完成, 执行Toast.clear()关闭
    })
}

// 接受后端返回的路线结果
const path_list = ref({
    path_idx_list: [],
    path_num_list: [],
    path_between_list: [],
    path_length: 0
})

// 两点之间的预计时间花费, n个点就有n-1个数据  单位:毫秒
const arrival_time = ref({
    by_walk: [],
    by_bike: [],
    by_car: []
})

// 各种交通方式的base前进速度  单位: m/min
const forward_velocity = ref({
    walk: 60,
    bike: 60,
    car: 350,
})

// 获取当前时间, 以毫秒为单位, 并作为arrival_time_show的第一个元素
base_time.value = date.getHours() * 60 * 60 * 1000 + date.getMinutes() * 60 * 1000 + date.getSeconds() * 1000
arrival_time_show.value.push(base_time.value)

// 返回上一级
const onClickLeftHead = () => history.back()

const showPicTitleFlag = ref(false) // 是否显示图片提示信息的标志

// 根据treeStore内容，获取路线结果
axios({
    method: 'POST',
    url: 'http://106.12.165.78:4554/guide',
    data: qs.stringify({
        "chosen_list": tree_st.selected_list.toString()
    })
}).then(res => {
    showPicTitleFlag.value = true
    // 步骤条 active 下标，默认最后一个
    active.value = tree_st.selected_list.length
    // 获取数据
    path_list.value.path_idx_list = res.data.path_idx_list
    path_list.value.path_num_list = res.data.path_num_list
    path_list.value.path_between_list = res.data.path_between_list  // 两个地点之间距离
    path_list.value.path_length = res.data.path_length
    // 保存name_list
    lnglat_st.path_num_list = res.data.path_num_list
    // 获取每两个点之间的所需时间
    for (let i = 0; i < path_list.value.path_between_list.length; i++) {
        arrival_time.value.by_walk.push((path_list.value.path_between_list[i] / forward_velocity.value.walk).toFixed(2) * 60 * 1000)
        arrival_time.value.by_bike.push((path_list.value.path_between_list[i] / forward_velocity.value.bike).toFixed(2) * 60 * 1000)
        arrival_time.value.by_car.push((path_list.value.path_between_list[i] / forward_velocity.value.car).toFixed(2) * 60 * 1000)
    }
    // arrival_time_show数组, 初始化时push了一个base_time, 这里继续向里追加, 每一次用前一个时间加需要的derta时间, 获得结果  单位: 毫秒
    for (let i = 0; i < path_list.value.path_between_list.length; i++) {
        arrival_time_show.value.push(arrival_time_show.value[i] + arrival_time.value.by_walk[i])
    }
    // 用arrival_time_show数组的首尾两个元素相减, 获得全程耗时, 四舍五入  单位: 分钟
    onChangedBarRes.value = Math.round((arrival_time_show.value.slice(-1)[0] - arrival_time_show.value[0]) / (1000 * 60))
    // 清空treeStore缓存的值
    // tree_st.selected_list = []
    // 请求[结果图片]
    axios({
        method: 'POST',
        url: 'http://106.12.165.78:4554/result',
        responseType: 'blob'
    }).then(res => {
        let blob = new Blob([res.data])
        let url = window.URL.createObjectURL(blob)
        res_pic.value = url
        Toast.clear()
    })
})

// 展示用户点击的行的下标，调试用
const showTouchIndex = (idx) => {
    // 如果选起点，就展示起点和第二个点之间的路线
    if (idx === 0) {
        lnglat_st.raw_start = idx
        lnglat_st.raw_end = idx + 1
        lnglat_st.current_start = path_list.value.path_idx_list[idx]
        lnglat_st.current_end = path_list.value.path_idx_list[idx + 1]
    }
    // 其他情况，选 i 和 i-1 两个点
    else {
        lnglat_st.raw_start = idx - 1
        lnglat_st.raw_end = idx
        lnglat_st.current_start = path_list.value.path_idx_list[idx - 1]
        lnglat_st.current_end = path_list.value.path_idx_list[idx]
    }
    // 进入详情界面
    router.push({
        name: 'sroute'
    })
}

// 不同行进方式的不同返回结果
const onChangedBarRes = ref(0)

// 监听出行方式变化, 动态修改到达时间
watch(active_bar, (idx) => {
    if (idx === 0) {
        const msg = ref('规划中...')
        if (tree_st.selected_list.length > 10 && setting_st.user_settings == '0') {
            msg.value = '规划中...\n选择地点过多\n将为您\n自动舍弃'
        }
        else if (tree_st.selected_list.length > 15 && setting_st.user_settings == '1') {
            msg.value = '规划中...\n选择地点过多\n将为您\n自动舍弃'
        }
        else if (tree_st.selected_list.length > 20 && setting_st.user_settings == '2') {
            msg.value = '规划中...\n选择地点过多\n将为您\n自动舍弃'
        }
        Toast.loading({
            message: msg.value,
            forbidClick: true,
            duration: 0    // 0为一直展示, 知道axios完成, 执行Toast.clear()关闭
        })
        axios({
            method: 'POST',
            url: 'http://106.12.165.78:4554/guide',
            data: qs.stringify({
                "chosen_list": tree_st.selected_list.toString()
            })
        }).then(res => {
            // 获取当前时间, 以毫秒为单位, 并作为arrival_time_show的第一个元素
            arrival_time_show.value = []
            base_time.value = date.getHours() * 60 * 60 * 1000 + date.getMinutes() * 60 * 1000 + date.getSeconds() * 1000
            arrival_time_show.value.push(base_time.value)
            // 步骤条 active 下标，默认最后一个
            active.value = tree_st.selected_list.length
            showPicTitleFlag.value = true
            lnglat_st.path_num_list = res.data.path_num_list
            // 获取数据
            path_list.value.path_idx_list = res.data.path_idx_list
            path_list.value.path_num_list = res.data.path_num_list
            path_list.value.path_between_list = res.data.path_between_list  // 两个地点之间距离
            path_list.value.path_length = res.data.path_length
            // 获取每两个点之间的所需时间
            for (let i = 0; i < path_list.value.path_between_list.length; i++) {
                arrival_time.value.by_walk.push((path_list.value.path_between_list[i] / forward_velocity.value.walk).toFixed(2) * 60 * 1000)
                arrival_time.value.by_bike.push((path_list.value.path_between_list[i] / forward_velocity.value.bike).toFixed(2) * 60 * 1000)
                arrival_time.value.by_car.push((path_list.value.path_between_list[i] / forward_velocity.value.car).toFixed(2) * 60 * 1000)
            }
            // arrival_time_show数组, 初始化时push了一个base_time, 这里继续向里追加, 每一次用前一个时间加需要的derta时间, 获得结果  单位: 毫秒
            for (let i = 0; i < path_list.value.path_between_list.length; i++) {
                arrival_time_show.value.push(arrival_time_show.value[i] + arrival_time.value.by_walk[i])
            }
            // 用arrival_time_show数组的首尾两个元素相减, 获得全程耗时, 四舍五入  单位: 分钟
            onChangedBarRes.value = Math.round((arrival_time_show.value.slice(-1)[0] - arrival_time_show.value[0]) / (1000 * 60))
            // 清空treeStore缓存的值
            // tree_st.selected_list = []
            // 请求[结果图片]
            axios({
                method: 'POST',
                url: 'http://106.12.165.78:4554/result',
                responseType: 'blob'
            }).then(res => {
                let blob = new Blob([res.data])
                let url = window.URL.createObjectURL(blob)
                res_pic.value = url
                Toast.clear()
            })
        })
    }
    else if (idx === 1) {
        Toast.loading({
            message: '规划中...\n完整地点\n(未舍弃)',
            forbidClick: true,
            duration: 0,    // 0为一直展示, 知道axios完成, 执行Toast.clear()关闭
        })
        axios({
            method: 'POST',
            url: 'http://106.12.165.78:4554/guide_aco',
            data: qs.stringify({
                "chosen_list": tree_st.selected_list.toString()
            })
        }).then(res => {
            // 获取当前时间, 以毫秒为单位, 并作为arrival_time_show的第一个元素
            arrival_time_show.value = []
            base_time.value = date.getHours() * 60 * 60 * 1000 + date.getMinutes() * 60 * 1000 + date.getSeconds() * 1000
            arrival_time_show.value.push(base_time.value)
            // 步骤条 active 下标，默认最后一个
            active.value = tree_st.selected_list.length
            showPicTitleFlag.value = true
            lnglat_st.path_num_list = res.data.path_num_list
            // 获取数据
            path_list.value.path_idx_list = res.data.path_idx_list
            path_list.value.path_num_list = res.data.path_num_list
            path_list.value.path_between_list = res.data.path_between_list  // 两个地点之间距离
            path_list.value.path_length = res.data.path_length
            // 获取每两个点之间的所需时间
            for (let i = 0; i < path_list.value.path_between_list.length; i++) {
                arrival_time.value.by_walk.push((path_list.value.path_between_list[i] / forward_velocity.value.walk).toFixed(2) * 60 * 1000)
                arrival_time.value.by_bike.push((path_list.value.path_between_list[i] / forward_velocity.value.bike).toFixed(2) * 60 * 1000)
                arrival_time.value.by_car.push((path_list.value.path_between_list[i] / forward_velocity.value.car).toFixed(2) * 60 * 1000)
            }
            // arrival_time_show数组, 初始化时push了一个base_time, 这里继续向里追加, 每一次用前一个时间加需要的derta时间, 获得结果  单位: 毫秒
            for (let i = 0; i < path_list.value.path_between_list.length; i++) {
                arrival_time_show.value.push(arrival_time_show.value[i] + arrival_time.value.by_walk[i])
            }
            // 用arrival_time_show数组的首尾两个元素相减, 获得全程耗时, 四舍五入  单位: 分钟
            onChangedBarRes.value = Math.round((arrival_time_show.value.slice(-1)[0] - arrival_time_show.value[0]) / (1000 * 60))
            // 清空treeStore缓存的值
            // tree_st.selected_list = []
            // 请求[结果图片]
            axios({
                method: 'POST',
                url: 'http://106.12.165.78:4554/result_aco',
                responseType: 'blob'
            }).then(res => {
                let blob = new Blob([res.data])
                let url = window.URL.createObjectURL(blob)
                res_pic.value = url
                Toast.clear()
            })
        })
    }
    else {
        Toast('待定捏')
    }
})
</script>