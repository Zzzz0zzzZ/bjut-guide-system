<template>
    <van-nav-bar title="BJUT校园导航" :safe-area-inset-top='true' :fixed="true" :placeholder="true" />
    <!-- 首页背景图片待定 -->
    <!-- <img src="@/assets/background.png" style="filter: blur(5px); width: 100%; height: 100%;"> -->
    <MapContainer />
    <!-- 今日面板 -->
    <TodayCard id="card" />
    <div class="btn-area" id="btn-area-obj">
        <!-- 信息提示栏 -->
        <van-row v-if="showSelectAreaFlag" style="margin:5px">
            <van-col span="1" style="line-height: 32px;">
                <van-icon name="points" color="#508aeb" size="22" />
            </van-col>
            <van-col span="11" style="font-display:left;line-height: 32px; color: #3d8af2;">
                &nbsp;&nbsp;选择您的目的地！
            </van-col>
            <van-col span="4" style="font-display:right;line-height: 32px;">已选择</van-col>
            <van-col span="1" :activeCount="activeCount" style="color: #3d8af2 ;text-align: center;line-height: 32px;">
                {{ activeCount }}
            </van-col>
            <van-col span="1" style="line-height: 32px;">个</van-col>
            <van-col span="1"></van-col>
            <van-col span="5" style="justify-content:right; text-align: right;line-height: 32px;">
                <van-button type="default" icon="close" size="small" style="line-height: 32px;" @click="clearActiveId">
                    清空
                </van-button>
            </van-col>
        </van-row>
        <!-- 树形选择 -->
        <van-tree-select v-if="showSelectAreaFlag" v-model:active-id="activeId" v-model:main-active-index="activeIndex"
            :items="items" style="margin: 5px;" />
        <div v-if="showHistoryGuideFlag" style="height: 83%; overflow: scroll; border-bottom: dashed #3d8af2;">
            <van-row
                style="line-height: 32px; position: sticky; top: 0px; background-color: white; border-bottom: dashed #3d8af2;">
                <van-col span="1">&nbsp;&nbsp;</van-col>
                <van-col span="1">
                    <van-icon name="clock-o" color="#3d8af2" size="22" />
                </van-col>
                <van-col span="10" style="color: #3d8af2;">
                    <h4 style="margin: 0px;">&nbsp;&nbsp;近期十条规划记录</h4>
                </van-col>
            </van-row>
            <div v-for="(content, index) in guideHistoryData.history_data" :key="index"
                style="border-bottom: dashed lightgrey; padding: 10px;">
                <div>
                    <span style="font-weight: bold;">路线:</span>
                    &nbsp;{{ content.path }}
                </div>
                <div><span style="font-weight: bold;">路线长度:</span>&nbsp;{{ content.path_length }}米</div>
                <div style="text-align: right; color: grey; font-size: small;">
                    <span>规划于</span>
                    &nbsp;{{ content.processed_time }}
                </div>
            </div>
        </div>
    </div>
    <div class="btn-float-area" id="btn-float-obj">
        <!-- 开始导航 & 规划历史 按钮 -->
        <van-row v-if="!showSelectAreaFlag && !showHistoryGuideFlag" gutter="20" justify="center"
            style="position: relative; top: 16px;" id="btn-row">
            <van-col span="10">
                <van-button type="primary" icon="guide-o" style="border-radius: 8px" @click="showSelectArea">开始导航
                </van-button>
            </van-col>
            <van-col span="10">
                <van-button type="primary" icon="clock-o" @click="showHistoryGuide"
                    style="border-radius: 8px; background-color: grey; border:grey">
                    规划历史
                </van-button>
            </van-col>
        </van-row>
        <!-- 确认导航 & 取消导航 按钮 -->
        <van-row v-if="showSelectAreaFlag" gutter="20" justify="center" style="position: relative; top: 16px;"
            id="btn-row-select">
            <van-col span="10">
                <van-button type="primary" icon="play-circle-o" style="border-radius: 8px" @click="beginGuide">
                    &nbsp;&nbsp;确认&nbsp;&nbsp;&nbsp;&nbsp;
                </van-button>
            </van-col>
            <van-col span="10">
                <van-button type="primary" icon="revoke" style="border-radius: 8px; background-color: grey; border:grey"
                    @click="closeSelectArea">&nbsp;&nbsp;返回&nbsp;&nbsp;&nbsp;&nbsp;
                </van-button>
            </van-col>
        </van-row>
        <!-- 历史规划页面 返回按钮 -->
        <van-row v-if="showHistoryGuideFlag" justify="center"
            style="position:relative; top:16px; margin-left: 5%; margin-right: 5%;" id="btn-row-history">
            <van-button type="primary" style="border-radius: 8px; background-color: grey; border:grey" block
                @click="onClickHistoryBack">
                返回
            </van-button>
        </van-row>
    </div>
</template>

<script setup>
import { Toast } from "vant"
import { computed, onUpdated, ref } from "vue"
import { treeStore } from '@/stores/treeStore'
import { useRouter } from 'vue-router'
import { settingStore } from "@/stores/settingStore"
import TodayCard from "../../components/TodayCard.vue"
import MapContainer from "@/components/MapContainer.vue"
import axios from "axios"

// 使用路由
const router = useRouter()

const guideHistoryData = ref([])        // 规划历史记录数据列表
const showSelectAreaFlag = ref(false)   // 是否显示地点选择板
const showHistoryGuideFlag = ref(false) // 是否显示历史规划板
const tree_st = treeStore()             // 缓存已选的点，保证切换页面后数据不会丢失

// 初始化用户设置
const setting_st = settingStore()
axios.get('http://106.12.165.78:4554/get_settings').then(res => {
    setting_st.user_settings = res.data
})

// 动态更改btn-area大小，并更改显示的按钮，并显示Tree-Select组件
const showSelectArea = () => {
    // 清空已选
    tree_st.selected_list = []
    activeId.value = []
    let btn_area_obj = document.getElementById('btn-area-obj')
    btn_area_obj.style.height = '57%'   //  调整treeSelect和按钮栏的覆盖bug
    let btn_row = document.getElementById('btn-row')
    btn_row.style.top = '10px'
    showSelectAreaFlag.value = true
    visTodayCard()
}

// 关闭选择框，返回初始状态
const closeSelectArea = () => {
    let btn_area_obj = document.getElementById('btn-area-obj')
    btn_area_obj.style.height = '10%'
    let btn_row = document.getElementById('btn-row-select')
    btn_row.style.top = '16px'
    showSelectAreaFlag.value = false
    visTodayCard()
}

// 地点列表不为空时才能进行导航
const beginGuide = () => {
    if (tree_st.selected_list.length > 0) {
        router.push({
            name: 'guide'
        })
    }
    else {
        Toast.fail({
            message: '目的地个数\n不能为空',
            duration: 800
        })
    }

}

// 查看历史信息
const showHistoryGuide = () => {
    axios.get('http://106.12.165.78:4554/history_guide').then(res => {
        guideHistoryData.value = res.data
    })
    let btn_area_obj = document.getElementById('btn-area-obj')
    btn_area_obj.style.height = '57%'
    btn_area_obj.style.overflow = 'scroll'
    let btn_row = document.getElementById('btn-row')
    btn_row.style.top = '10px'
    showHistoryGuideFlag.value = true
    visTodayCard()
}

// 从历史规划面板返回初始状态
const onClickHistoryBack = () => {
    showHistoryGuideFlag.value = false
    showSelectAreaFlag.value = false
    let btn_area_obj = document.getElementById('btn-area-obj')
    btn_area_obj.style.height = '10%'
    let btn_row = document.getElementById('btn-row-history')
    btn_row.style.top = '16px'
    visTodayCard()
}

const clearActiveId = () => {
    activeId.value = []
    Toast.success({
        message: '已清空',
        duration: 500
    })
}

const visTodayCard = () => {
    let today_card = document.getElementById('card')
    if (showHistoryGuideFlag.value || showSelectAreaFlag.value) {
        today_card.style.top = '0px'
        today_card.style.height = '0%'
        today_card.style.opacity = 0
    }
    else {
        today_card.style.top = '65px'
        today_card.style.height = '15%'
        today_card.style.opacity = 1
    }
}

onUpdated(() => {
    tree_st.saveSelectChange(activeId)
})

// Tree-Select
const activeId = ref(tree_st.selected_list);
const activeIndex = ref(0);
const activeCount = computed(() => activeId.value.length)
const items = [
    {
        text: '餐厅',
        children: [
            { text: '天天餐厅', id: 0 },
            { text: '美食园、风味、奥运', id: 1 },
        ],
    },
    {
        text: '教学楼',
        children: [
            { text: '第一教学楼', id: 2 },
            { text: '第二教学楼', id: 3 },
            { text: '第三教学楼', id: 4 },
            { text: '第四教学楼', id: 5 },
        ],
    },
    {
        text: '图书馆',
        children: [
            { text: '逸夫图书馆', id: 6 },
            { text: '旧图', id: 7 },
        ],
    },
    {
        text: '浴室',
        children: [
            { text: '北浴', id: 8 },
            { text: '南浴', id: 9 },
        ],
    },
    {
        text: '宿舍楼',
        children: [
            { text: '1、2号楼', id: 10 },
            { text: '3、4号楼', id: 11 },
            { text: '5、6号楼', id: 12 },
            { text: '7、8号楼', id: 13 },
            { text: '9号楼', id: 14 },
            { text: '10号楼', id: 15 },
            { text: '12号楼', id: 16 },
            { text: '13、14号楼', id: 17 },
        ],
    },
    {
        text: '校门',
        children: [
            { text: '东门', id: 18 },
            { text: '西门', id: 19 },
            { text: '南门', id: 20 },
            { text: '北门', id: 21 },
        ],
    },
    {
        text: '体育场馆',
        children: [
            { text: '北操', id: 22 },
            { text: '南操', id: 23 },
            { text: '网球场', id: 24 },
            { text: '篮球场', id: 25 },
            { text: '奥运体育馆', id: 26 },
            { text: '游泳馆', id: 27 },
        ],
    },
    {
        text: '学科楼',
        children: [
            { text: '材料楼', id: 28 },
            { text: '数理楼', id: 29 },
            { text: '能源楼', id: 30 },
            { text: '信息楼', id: 31 },
            { text: '艺设楼', id: 32 },
            { text: '生命楼', id: 33 },
            { text: '经管楼', id: 34 },
            { text: '科学楼', id: 35 },
            { text: '人文楼', id: 36 },
            { text: '软件楼', id: 37 },
            { text: '城建楼', id: 38 },
        ],
    },
    {
        text: '其他',
        children: [
            { text: '月亮湖', id: 39 },
            { text: '知心园', id: 40 },
            { text: '礼堂', id: 41 },
            { text: '校医院', id: 42 },
            { text: '工程实践中心', id: 43 },
        ],
    }
];

</script>

<style scoped>
.btn-area {
    /* 背景颜色与圆角大小 */
    background-color: rgba(255, 255, 255, 0.892);
    border-radius: 15px;
    /* fixed定位 相对eft和bottom */
    position: fixed;
    left: 2.5%;
    bottom: 90px;
    /* 框大小，相对父元素（窗口）大小的百分比 */
    width: 95%;
    height: 10%;
    /* 阴影 */
    box-shadow: 0px 5px 5px lightgrey;
    /* 居中 */
    justify-content: center;
    /* text-align: center; */
    /* 动态更改大小后的过渡动画 */
    transition: all 0.5s ease;
}

.btn-float-area {
    position: fixed;
    bottom: 85px;
    left: 2.5%;
    width: 95%;
    height: 10%;
    justify-content: center;
    text-align: center;
    transition: 300ms;
}
</style>