<template>
    <van-nav-bar title="BJUT待办事项" />
    <!-- 蓝色大背景 -->
    <div style="background-color: #3d8af2; height: 90%; position: absolute; top: 1%%; width: 100%;">
        <!-- 添加待办的输入栏 -->
        <div style="width: 100%; height:3%"> </div>
        <van-cell-group inset>
            <van-field v-model="todo_value" center autosize clearable placeholder="添加一条待办事项">
                <template #label>
                    <span style="font-weight: bold; text-decoration: underline;">待办事项</span>
                </template>
                <template #button>
                    <van-button size="small" type="primary" @click="onClickAddButton(todo_value)">添加</van-button>
                </template>
            </van-field>
        </van-cell-group>
        <!-- 待办列表 -->
        <div
            style="width: 92%; left: 4%; top: 2%; position: relative; background-color: white; height: 80%; border-radius: 5px; overflow: scroll;">
            <div style="width:100%; height: 6%; padding-top: 2%; font-weight: bold;">
                &nbsp;&nbsp;&nbsp;待办列表
            </div>
            <template v-for="(content, index) in content_list.value">
                <div v-if="content.status === 0" :key="index">
                    <van-swipe-cell>
                        <template #left>
                            <van-button square type="primary" text="完成" @click="onClickComplete(content)" />
                        </template>
                        <van-cell :border="true">
                            <template #title>
                                <van-tag mark type="primary">{{ index }}</van-tag>
                                {{ content.content }}
                            </template>
                            <template #value>
                                <div v-if="content.deadline">{{ getLastingDays(content) === 0 ? '就是今天!' :
                                        (getLastingDays(content) > 0) ? `还剩${getLastingDays(content)}天`
                                            : `过期${Math.abs(getLastingDays(content))}天`
                                }}</div>
                            </template>
                        </van-cell>
                        <template #right>
                            <van-button square type="danger" text="删除" @click="onClickDelete(content)" />
                            <van-button square type="primary" text="更改" @click="onClickSettings(content)">
                            </van-button>
                        </template>
                    </van-swipe-cell>
                </div>
            </template>
        </div>
        <!-- 定制主题 -->
        <van-config-provider :theme-vars="themeVars">
            <!-- DatePicker设置到期日 -->
            <van-calendar v-model:show="showCalendarPicker" @confirm="onConfirm" />
        </van-config-provider>
    </div>
</template>

<script setup>
import { Dialog } from 'vant'
import { ref, reactive, toRaw } from 'vue'
import { tdlStore } from '@/stores/tdlStore'
import axios from 'axios'
import dayjs from 'dayjs'

// 主题定制-日期选择
const themeVars = {
    buttonDangerBackgroundColor: '#3d8af2',
    buttonDangerBorderColor: '#3d8af2'
}

const tdl_st = tdlStore()           // 模拟登陆, 获取token
const content_list = reactive([])   // 获取的待办事项
tdl_st.updateCount()                // 模拟登陆, 获取token

// 获取待办
axios({
    url: `/todolist/todos/${tdl_st.user_id}`,
    method: 'GET',
    headers: ({
        "token": tdl_st.token
    })
}).then(res => {
    content_list.value = res.data
    content_list.value = content_list.value.reverse()
})


const todo_value = ref('')      // 添加待办的内容

// 点击添加按钮时
const onClickAddButton = (val) => {
    axios({
        url: '/todolist/add',
        method: 'POST',
        headers: ({
            "token": tdl_st.token
        }),
        data: ({
            "userid": tdl_st.user_id,
            "content": val
        })
    }).then(() => {
        content_list.value.unshift(val)
        axios({
            url: `/todolist/todos/${tdl_st.user_id}`,
            method: 'GET',
            headers: ({
                "token": tdl_st.token
            })
        }).then(res => {
            content_list.value = res.data
            content_list.value = content_list.value.reverse()
            tdl_st.updateCount()
        })
    })
    todo_value.value = ''
}

// 点击完成按钮时
const onClickComplete = (content) => {
    let content_ori = toRaw(content)
    axios({
        url: '/todolist/update',
        method: 'POST',
        data: ({
            id: content_ori.id,
            userid: content_ori.userid,
            content: content_ori.content,
            status: 1
        }),
        headers: ({
            "token": tdl_st.token
        })
    }).then(() => {
        content.status = 1
        tdl_st.updateCount()
    })
}

// 点击删除按钮时
const onClickDelete = (content) => {
    Dialog.confirm({
        title: '确认要删除这条待办事项吗？',
        message:
            `【待办内容】${content.content}\n【到期日】${content.deadline}\ntips:距离到期还剩[${getLastingDays(content)}]天`,
    })
        // 点击确认时
        .then(() => {
            axios({
                url: '/todolist/delete',
                method: 'POST',
                data: toRaw(content),
                headers: ({
                    "token": tdl_st.token
                })
            }).then(() => {
                content.status = 1
                tdl_st.updateCount()
            })
        })
        // 点击取消时
        .catch(() => {
            // on cancel
        });
}

const showCalendarPicker = ref(false)   // 是否展示DatePicker
const currentSettingsId = ref(0)        // 当前正在设置的待办id

// 点击[更改]按钮时
const onClickSettings = (content) => {
    currentSettingsId.value = content.id
    showCalendarPicker.value = true
}

// 设置到期日, 点击确认按钮时
const onConfirm = (value) => {
    const formatDate = (date) => `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()}`;
    let select_date = formatDate(value);
    axios({
        url: '/todolist/update',
        method: 'POST',
        data: ({
            id: currentSettingsId.value,
            deadline: select_date
        }),
        headers: ({
            "token": tdl_st.token
        })
    }).then(() => {
        showCalendarPicker.value = false
        refresh_list()
    })
};

// 刷新待办, 重新请求接口
const refresh_list = () => {
    axios({
        url: `/todolist/todos/${tdl_st.user_id}`,
        method: 'GET',
        headers: ({
            "token": tdl_st.token
        })
    }).then(res => {
        content_list.value = res.data
        content_list.value = content_list.value.reverse()
        tdl_st.updateCount()
    })
}

// 根据content.deadline的日期和当前日期, 获取剩余天数
const getLastingDays = (content) => {
    let ddl = content.deadline
    let todayDate = new Date()
    let today = todayDate.toISOString().split('T')[0]
    let days_left = dayjs(ddl).diff(today, 'day') - 1
    return days_left
}

</script>