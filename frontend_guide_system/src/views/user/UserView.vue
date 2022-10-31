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
    <!-- 偏好设置[待完成] -->
    <div class="user-settings">
        <van-button icon="idcard" type="primary" color="#3d8af2" block plain>
            偏好设置
        </van-button>
    </div>
</template>

<script setup>
import axios from 'axios'
import { ref } from 'vue'

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