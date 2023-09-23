<script setup lang="ts">
import DigitsRound from './DigitsRound.vue'
import { reactive } from 'vue'
// @ts-ignore
import $ from 'jquery'


let dYesterday = { r1: {}, r2: {}, r3: {}, r4: {}, r5: {} }
function getYesterdayData() {
  $.ajax({
    url: 'https://raw.githubusercontent.com/rileypeterson/digits/main/data/data_yesterday.json',
    type: 'get',
    dataType: 'json',
    crossDomain: true,
    async: false,
    success: function (resp: any) {
      dYesterday = resp
    }
  })
}
getYesterdayData()

let dTomorrow = { r1: {}, r2: {}, r3: {}, r4: {}, r5: {} }
function getTomorrowData() {
  $.ajax({
    url: 'https://raw.githubusercontent.com/rileypeterson/digits/main/data/data_tomorrow.json',
    type: 'get',
    dataType: 'json',
    crossDomain: true,
    async: false,
    success: function (resp: any) {
      dTomorrow = resp
    }
  })
}
getTomorrowData()

// Get the right payload depending on the date
let today = new Date()
let todayString = today.toLocaleDateString()
let storedDateString = localStorage.getItem("lastVisitDateString")
let lastData = localStorage.getItem("lastData")
if (!storedDateString) {
  // Never been to site
  localStorage.setItem("lastVisitDateString", todayString)
  // Set yesterday's data as the last data
  localStorage.setItem("lastData", JSON.stringify(dYesterday))
} else {
  // Been to the site
  if (todayString === storedDateString && lastData) {
    // Use last data
  } else if (todayString !== storedDateString && lastData) {
    // New day use next data
    localStorage.setItem("lastData", JSON.stringify(dTomorrow))
    localStorage.setItem("lastVisitDateString", todayString)
  }
}

const data = reactive(JSON.parse(localStorage.getItem("lastData") || "{}"))
</script>

<template>
  <div class="container-fluid w-100">
    <ul class="nav nav-tabs" id="myTab" role="tablist">
      <li class="nav-item mx-auto" role="presentation" v-for="n in 5" :key="n">
        <button
          class="nav-link"
          :class="`${n == 1 ? 'active' : ''}`"
          :id="`r${n}-tab`"
          data-bs-toggle="tab"
          :data-bs-target="`#r${n}`"
          type="button"
          role="tab"
          :aria-controls="`r${n}`"
          :aria-selected="`${n == 1 ? 'true' : 'false'}`"
          style="color: var(--round-green)"
        >
          Round {{ n }}
        </button>
      </li>
      <li class="nav-item mx-auto" role="presentation">
        <button
          class="nav-link"
          id="about-tab"
          data-bs-toggle="tab"
          data-bs-target="#about"
          type="button"
          role="tab"
          aria-controls="about"
          aria-selected="false"
          style="color: #000"
        >
          About
        </button>
      </li>
    </ul>
    <div class="tab-content" id="myTabContent">
      <div class="tab-pane fade show active" id="r1" role="tabpanel" aria-labelledby="r1-tab">
        <DigitsRound :data="data['r1']"></DigitsRound>
      </div>
      <div class="tab-pane fade" id="r2" role="tabpanel" aria-labelledby="r2-tab">
        <DigitsRound :data="data['r2']"></DigitsRound>
      </div>
      <div class="tab-pane fade" id="r3" role="tabpanel" aria-labelledby="r3-tab">
        <DigitsRound :data="data['r3']"></DigitsRound>
      </div>
      <div class="tab-pane fade" id="r4" role="tabpanel" aria-labelledby="r4-tab">
        <DigitsRound :data="data['r4']"></DigitsRound>
      </div>
      <div class="tab-pane fade" id="r5" role="tabpanel" aria-labelledby="r5-tab">
        <DigitsRound :data="data['r5']"></DigitsRound>
      </div>
      <div
        class="tab-pane fade text-center mt-5"
        id="about"
        role="tabpanel"
        aria-labelledby="about-tab"
      >
        I loved to play the New York Times Digits game. Unfortunately, it was
        <a target="_blank" href="https://www.nytimes.com/games/digits">discontinued</a>. So, I built this version of
        it.
        <br>
        The source code is available <a target="_blank" href="https://github.com/rileypeterson/digits">here</a>.
      </div>
    </div>
  </div>
</template>

<style scoped>
@media (min-width: 400px) {
  #myTab {
    width: 100%;
  }
}

/* Small devices (landscape phones, 576px and up) */
@media (min-width: 576px) {
}

/* Medium devices (tablets, 768px and up) */
@media (min-width: 768px) {
}

/* Large devices (desktops, 992px and up) */
@media (min-width: 992px) {
}

/* X-Large devices (large desktops, 1200px and up) */
@media (min-width: 1200px) {
}
</style>
