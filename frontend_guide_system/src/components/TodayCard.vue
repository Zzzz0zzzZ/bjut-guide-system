<template>
    <van-row align="center" class="td-card font-title" id="card">
        <van-col span="8">
            <van-circle v-model:current-rate="currentRate" :rate="rate" color="#508aeb" :text="text" :speed="100"
                :stroke-width="60" style="width: 80%; position: relative; top: 5px;" />
        </van-col>
        <van-col span="16">
            <van-row>
                <van-col span="14">{{ today_info.time_info.today_date }}</van-col>
                <van-col span="10">{{ today_info.time_info.weekday_list[today_info.time_info.today_weekday] }}
                </van-col>
            </van-row>
            <van-row style="text-align:center; justify-content:center">
                <van-col span="4">{{ today_info.weather_info.city }}</van-col>
                <van-col span="8">{{ today_info.weather_info.wea }}</van-col>
                <van-col span="12">{{ today_info.weather_info.tem2 }}℃&nbsp;-&nbsp;{{ today_info.weather_info.tem1
                }}℃</van-col>
            </van-row>
            <van-divider :style="{ color: '#1989fa', borderColor: '#1989fa', padding: '0px', margin: '5px' }" />
            <van-row style="text-align:center; justify-content:center">
                {{ notice }}
            </van-row>
        </van-col>
    </van-row>
</template>

<script setup>
import { computed } from '@vue/reactivity'
import { ref } from 'vue'
import { tdlStore } from '@/stores/tdlStore'
import axios from 'axios';

const tdl_st = tdlStore()
tdl_st.updateCount()
const rate = ref(0)
const currentRate = ref(0)
const text = computed(() => '今日待办:' + String(tdl_st.count_finish) + '/' + String(tdl_st.count_total))
const today_info = ref({
    weather_info: {},
    time_info: {
        today_date: '',
        today_weekday: '',
        weekday_list: ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"]
    }
})
const notice = ref('')
const date = new Date()

setTimeout(() => {
    // TodayCard入场动画
    let td_card = document.getElementById('card')
    td_card.style.top = '65px'
    td_card.style.height = '15%'
    td_card.style.opacity = 1
    // 进度条动画
    rate.value = tdl_st.getPortion
}, 20)

axios.get('https://v0.yiketianqi.com/api?unescape=1&version=v61&appid=43429654&appsecret=qSjImVc6').then(res => {
    today_info.value.weather_info = res.data
})
today_info.value.time_info.today_date = date.getFullYear() + '年' + (date.getMonth() + 1) + '月' + date.getDate() + '日'
today_info.value.time_info.today_weekday = date.getDay()

axios.get('/api/next_course').then(res => {
    notice.value = res.data
})

</script>

<style scoped>
.td-card {
    position: fixed;
    top: 0px;
    left: 2.5%;
    width: 95%;
    height: 0%;
    justify-content: center;
    text-align: center;
    background-color: rgba(255, 255, 255, 0.9);
    border-radius: 15px;
    transition: 500ms;
    opacity: 0;
}

.font-title {
    font-family: "站酷酷黑 Regular";
    font-weight: bolder;
    src: url("//at.alicdn.com/wf/webfont/thn1lMFJ8K4a/CBopGTQxjP2mk9OlxDMGZ.woff2") format("woff2"),
        url("//at.alicdn.com/wf/webfont/thn1lMFJ8K4a/QP6dA6oMVAoUu_UG5Cc73.woff") format("woff");
    font-display: swap;
}
</style>