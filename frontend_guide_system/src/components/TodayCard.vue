<template>
    <div class="td-card">
        <van-row align="center">
            <van-col span="8">
                <van-circle v-model:current-rate="currentRate" :rate="rate" color="#508aeb" :text="text"
                    :stroke-width="60" style="width: 80%; position: relative; top: 5px;" />
            </van-col>
            <van-col span="16">
                <van-row>
                    1
                </van-row>
                <van-row>
                    2
                </van-row>
                <van-row>
                    3
                </van-row>
            </van-col>
        </van-row>
    </div>

</template>

<script setup>
import { computed } from '@vue/reactivity'
import { ref } from 'vue'

const rate = ref(75)
const currentRate = ref(50)
const text = computed(() => '%')

</script>

<style scoped>
.td-card {
    position: fixed;
    top: 65px;
    left: 2.5%;
    width: 95%;
    height: 15%;
    justify-content: center;
    text-align: center;
    background-color: rgba(211, 211, 211, 0.802);
    border-radius: 15px;
}
</style>