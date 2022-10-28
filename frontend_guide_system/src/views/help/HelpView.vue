<template>
    <van-nav-bar title="BJUT校园攻略" />
    <van-search v-model="value" background="#3d8af2" shape="round" show-action placeholder="请选择搜索类别,并输入搜索关键词"
        @search="onSearch">
        <template #action>
            <div @click="onClickButton" style="color:#ffffff;">搜索</div>
        </template>
        <template #label>
            <van-popover v-model:show="showPopover" :actions="actions" placement="bottom-start">
                <template #reference>
                    <div>资讯
                        <span style="font-size: 8px;">▼</span>
                    </div>
                </template>
            </van-popover>
        </template>
    </van-search>
</template>

<script setup>
import { ref } from 'vue'
import { Toast } from 'vant'

const value = ref('');
const onSearch = (val) => Toast(val);
const onClickButton = () => Toast(value.value);
const showPopover = ref(false);
const actions = [
    { text: '分类一', icon: 'add-o' },
    { text: '分类二', icon: 'music-o' },
    { text: '分类三', icon: 'more-o' },
];
</script>