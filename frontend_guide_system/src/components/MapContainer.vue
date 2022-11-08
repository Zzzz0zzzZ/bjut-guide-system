<template>
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
const converted_list = ref([])  // 高德坐标系下的经纬度

// 获取百度坐标系经纬度
axios.get('http://127.0.0.1:8000/lng_lat_list').then(res => {
    lng_lat_ori.value = res.data
    console.log(lng_lat_ori.value)
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

        // map.value.
        // 百度地图坐标系 转换 高德地图坐标系
        AMap.convertFrom(lng_lat_ori.value, 'baidu', function (status, result) {
            if (result.info === 'ok') {
                converted_list.value = result.locations
                lnglat_st.lnglat_converted_list = result.locations  /////////////////
                console.log('cvr-list', converted_list.value);
                // 添加、绘制坐标点 [待更改为大数组, 利于添加点击事件]
                for (let item of converted_list.value) {
                    let marker = new AMap.Marker({
                        position: [item.lng, item.lat],     // 根据高德api返回结果写的
                    });
                    map.value.add(marker);                  // 创建一个点标记
                }
            }
        })
    })
        .catch(e => {
            console.log(e);
        })
})

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