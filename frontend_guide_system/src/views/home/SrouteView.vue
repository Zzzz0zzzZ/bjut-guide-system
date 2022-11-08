<template>
    <van-nav-bar title="BJUT校园导航" :safe-area-inset-top='true' left-text="返回" left-arrow :fixed="true"
        @click-left="onClickLeftHead" />
    <div style="position: absolute; top:8%; z-index: 10; width: 100%; ">
        <van-cell-group inset :path_list="path_list">
            <van-cell icon="location-o">
                <template #title>
                    <span style="font-weight:bold; font-size: larger;">起点:&nbsp;</span>
                    <span style="font-size: larger;">{{ path_list.path_start }}</span>
                </template>
                <template #value>
                    预计需要{{ Math.round(path_list.path_time / 60) }}分钟
                </template>
            </van-cell>
            <van-cell icon="location-o">
                <template #title>
                    <span style="font-weight: bold; font-size: larger;">终点:&nbsp;</span>
                    <span style="font-size: larger;">{{ path_list.path_end }}</span>
                </template>
                <template #value>
                </template>
                <template #label>
                    路线全长{{ path_list.path_length }}米
                </template>
            </van-cell>
        </van-cell-group>
    </div>
    <div style="position: fixed; bottom:8%; width: 90%; left: 5%; background-color: rgba(255, 255, 255, 0.9); z-index: 10; height: 15%; border-radius: 8px;"
        :path_detail="path_detail">
        <div style="position: relative; top:10%; left: 5%; font-weight: bold;">
            路线详情
        </div>
        <div style="position: relative; top:25%; ">
            <van-row justify="space-between" align="center">
                <van-col span="6" @click="onClickLeftBtn">
                    <van-icon name="arrow-left" size="36" />
                </van-col>
                <van-col span="12" style="font-size: 18px; color:#3d8af2; text-align: center;">{{
                        path_detail.details[path_detail.current_show_idx]
                }}
                </van-col>
                <van-col span="6">
                    <van-icon name="arrow" size="36" style="float: right;" @click="onClickRightBtn" />
                </van-col>
            </van-row>
        </div>

    </div>
    <div class="home_div">
        <div id="container"></div>
    </div>
</template>

<script setup>
import AMapLoader from "@amap/amap-jsapi-loader"
import { shallowRef } from '@vue/reactivity'
import { ref } from "vue"
import { lnglatStore } from "@/stores/lnglatStore"
import axios from "axios"

const lnglat_st = lnglatStore()

const lng_lat_ori = ref([])     // 百度坐标系下的经纬度
const converted_list = ref(lnglat_st.lnglat_converted_list)  // 高德坐标系下的经纬度
console.log(lnglat_st.path_num_list);
console.log(lnglat_st.raw_start, lnglat_st.raw_end);
const path_list = ref({
    path_start: lnglat_st.path_num_list[lnglat_st.raw_start],
    path_end: lnglat_st.path_num_list[lnglat_st.raw_end],
    path_length: 0,
    path_time: 0
})
const path_detail = ref({
    details: [],
    current_show_idx: 0
})

const onClickLeftBtn = () => {
    if (path_detail.value.current_show_idx !== 0) {
        path_detail.value.current_show_idx--;
    }
}
const onClickRightBtn = () => {
    if (path_detail.value.current_show_idx !== path_detail.value.details.length - 1) {
        path_detail.value.current_show_idx++;
    }
}

// 获取百度坐标系经纬度
axios.get('http://127.0.0.1:8000/lng_lat_list').then(res => {
    lng_lat_ori.value = res.data
    // console.log(lng_lat_ori.value)
    // 创建initMap函数
    AMapLoader.load({
        key: 'c1d53c0c4e919bd417b76365a05c2e8a',  // 高德key
        version: "2.0",
        plugins: ['AMap.ToolBar', 'AMap.Driving', 'Amap.Walking'],  // 插件
        AMapUI: {
            version: "1.1",
            plugins: ['overlay/SimpleMarker'],
        },
        Loca: {
            version: "2.0.0"
        },
    }).then((AMap) => {
        // 创建map视图
        const map = shallowRef(null);   // map对象

        map.value = new AMap.Map("container", {
            viewMode: "3D",
            zoom: 17,                           // 默认缩放
            center: [116.479676, 39.874858],    // 视图中心点[逸夫图书馆]
        });

        // walking-route
        AMap.plugin('AMap.Walking', function () {
            var walking = new AMap.Walking({
                map: map.value,
            })
            // 设置起始点、终止点
            var startLngLat = [converted_list.value[lnglat_st.current_start].lng, converted_list.value[lnglat_st.current_start].lat]
            var endLngLat = [converted_list.value[lnglat_st.current_end].lng, converted_list.value[lnglat_st.current_end].lat]
            walking.search(startLngLat, endLngLat, function (status, result) {
                // 未出错时，result即是对应的路线规划方案
                path_list.value.path_length = result.routes[0].distance
                path_list.value.path_time = result.routes[0].time
                // 路线指示
                for (let i = 0; i < result.routes[0].steps.length; i++) {
                    path_detail.value.details.push(result.routes[0].steps[i].instruction)
                }
            })
        })
    })
})
    .catch(e => {
        console.log(e);
    })

// 返回上一级
const onClickLeftHead = () => history.back()

</script>

<style scoped>
.home_div {
    height: 100%;
    width: 100%;
    padding: 0px;
    margin: 0px;
    position: relative;
}

#container {
    height: 100%;
    width: 100%;
    padding: 0px;
    margin: 0px;
    position: fixed;
}
</style>

