<template>
    <van-nav-bar title="BJUT个人信息" />
    <!-- 蓝色大背景 -->
    <div class="container" style="background-color: #3d8af2; height: 90%; position: absolute; top: 1%%; width: 100%;">
        <!-- 用户卡片 -->
        <div class="user-card">
            <div style="width: 100%; height:18%"></div>
            <van-row justify="center" align="center">
                <van-col span="4"></van-col>
                <van-col span="6">
                    <img :src="user_photo"
                        style="position: relative; height:80%; width:50%; border-radius:50%; justify-content: center; text-align: center;">
                </van-col>
                <van-col span="14" style="font-size: 20px; text-align: left; justify-content: left;">下午好，王思哲！</van-col>
            </van-row>
        </div>
        <!-- 课程卡片 -->
        <div class="user-courses">
            <div style="position: relative; top:3%; left:4%; font-weight: bold;">我的课表</div>
            <img :src="course_pic" style="position: relative; height:90%; width:100%; top: 7%;">
        </div>
    </div>
    <!-- 偏好设置 -->
    <div class="user-settings">
        <van-button icon="idcard" type="primary" color="#3d8af2" block plain @click="showPopup">
            偏好设置
        </van-button>
    </div>
    <van-popup v-model:show="showSettings" round closeable position="bottom" :style="{ height: '50%' }">
        <!-- 自动舍弃算法设置 -->
        <h3 style="text-align: center; margin-bottom: 0;">偏好设置</h3>
        <div style="position:relative; top:5%">
            <!-- 子设置标题 -->
            <div style="width: 90%; left:5%; position:relative">
                <h4 style="margin-top: 10px; margin-bottom:5px">自动舍弃算法阈值</h4>
                <div style="color: grey; margin-bottom: 10px;">当选择地点超过一定数量时，系统会为您自动舍弃部分较远的点，优先去较近的地点。</div>
            </div>

            <!-- 选择部分 -->
            <van-radio-group v-model="checked">
                <van-cell-group inset>
                    <van-cell title="&nbsp;多于10个点自动舍弃" clickable @click="checked = '0'" style="padding: 10px 0;">
                        <template #right-icon>
                            <van-radio name="0" />
                        </template>
                    </van-cell>
                    <van-cell title="&nbsp;多于15个点自动舍弃(推荐)" clickable @click="checked = '1'" style="padding: 10px 0; ">
                        <template #right-icon>
                            <van-radio name="1" />
                        </template>
                    </van-cell>
                    <van-cell title="&nbsp;多于20个点自动舍弃(不推荐,规划时间较长)" clickable @click="checked = '2'"
                        style="padding: 10px 0;">
                        <template #right-icon>
                            <van-radio name="2" />
                        </template>
                    </van-cell>
                </van-cell-group>
            </van-radio-group>
        </div>
        <van-button style="position: relative; top:10%; width:90%; left:5%" type="primary" block @click="saveSettings">
            保存设置</van-button>
    </van-popup>

</template>

<script setup>
import axios from 'axios'
import qs from 'qs'
import { ref } from 'vue'
import { settingStore } from '@/stores/settingStore'
import { Toast } from 'vant';

const setting_st = settingStore()       // user-settings store
const checked = ref(setting_st.user_settings)   // user选择(包含后端加载的默认选择)
const showSettings = ref(false)                 // 是否展示选择面板

// 展示设置面板
const showPopup = () => {
    showSettings.value = true
}

// 保存设置, 并隐藏设置面板
const saveSettings = () => {
    axios({
        method: 'POST',
        url: '/api/set_settings',
        data: qs.stringify({
            "choose": checked.value
        })
    }).then(res => {
        if (res.status === 200) {
            showSettings.value = false
            Toast({
                type: 'success',
                duration: 600,
                message: '保存设置成功'
            })
        }
    })
}

// 获取用户头像
const user_photo = ref('')
axios({
    method: 'POST',
    url: '/api/user_photo',
    responseType: 'blob'
}).then(res => {
    let blob = new Blob([res.data])
    let url = window.URL.createObjectURL(blob)
    user_photo.value = url
})

// 获取课表图片
const course_pic = ref('')
axios({
    method: 'POST',
    url: '/api/course',
    responseType: 'blob'
}).then(res => {
    let blob = new Blob([res.data])
    let url = window.URL.createObjectURL(blob)
    course_pic.value = url
})
</script>

<style scoped>
.user-card {
    background-color: white;
    height: 12%;
    width: 90%;
    position: absolute;
    top: 3%;
    left: 5%;
    border-radius: 5px;
    line-height: 12%;
}

.user-courses {
    background-color: white;
    height: 60%;
    width: 90%;
    position: absolute;
    top: 19%;
    left: 5%;
    border-radius: 5px;
}

.user-settings {
    position: absolute;
    top: 81%;
    left: 5%;
    width: 90%;
}
</style>