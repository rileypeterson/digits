<script setup lang="ts">
import DigitsRound from './DigitsRound.vue'
import { reactive, ref } from 'vue'
// @ts-ignore
import $ from 'jquery'

// Get the localize date string for the player
let today = new Date()
let todayDate = [
  today.getFullYear(),
  ('0' + (today.getMonth() + 1)).slice(-2),
  ('0' + today.getDate()).slice(-2)
].join('-')
let storedDateString = localStorage.getItem('lastVisitDateString')
let lastData = localStorage.getItem('lastData')
if (!storedDateString || ((todayDate !== storedDateString) && lastData)) {
  // Never been to site or it's a new date, then the data needs to be update
  localStorage.setItem('lastVisitDateString', todayDate)

  // Fetch data
  let branch = "7-two-players-in-the-same-timezone-should-have-the-same-puzzle"
  let dYesterday = { puzzleDate: null, r1: {}, r2: {}, r3: {}, r4: {}, r5: {} }
  function getYesterdayData() {
    $.ajax({
      url: 'https://raw.githubusercontent.com/rileypeterson/digits/' + branch + '/data/data_yesterday.json',
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

  let dToday = { puzzleDate: null, r1: {}, r2: {}, r3: {}, r4: {}, r5: {} }
  function getTodayData() {
    $.ajax({
      url: 'https://raw.githubusercontent.com/rileypeterson/digits/' + branch + '/data/data_today.json',
      type: 'get',
      dataType: 'json',
      crossDomain: true,
      async: false,
      success: function (resp: any) {
        dToday = resp
      }
    })
  }
  getTodayData()

  let dTomorrow = { puzzleDate: null, r1: {}, r2: {}, r3: {}, r4: {}, r5: {} }
  function getTomorrowData() {
    $.ajax({
      url: 'https://raw.githubusercontent.com/rileypeterson/digits/' + branch + '/data/data_tomorrow.json',
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

  // Get the date that comes with each payload
  let dYesterdayDate = dYesterday['puzzleDate']
  let dTodayDate = dToday['puzzleDate']
  let dTomorrowDate = dTomorrow['puzzleDate']

  // Get the date which corresponds to the correct date
  if (todayDate == dYesterdayDate) {
    localStorage.setItem('puzzleDate', dYesterdayDate)
    localStorage.setItem('lastData', JSON.stringify(dYesterday))
  } else if (todayDate == dTodayDate) {
    localStorage.setItem('puzzleDate', dTodayDate)
    localStorage.setItem('lastData', JSON.stringify(dToday))
  } else if (todayDate == dTomorrowDate) {
    localStorage.setItem('puzzleDate', dTomorrowDate)
    localStorage.setItem('lastData', JSON.stringify(dTomorrow))
  }
}

const data = reactive(JSON.parse(localStorage.getItem('lastData') || '{}'))
const puzzleDate = ref(localStorage.getItem('puzzleDate') || '')
</script>

<template>
  <div class="container-fluid w-100">
    <ul class="nav nav-tabs justify-content-center row px-0 mx-0" id="myTab" role="tablist">
      <li class="nav-item col-4 col-md-2" role="presentation">
        <button
          class="nav-link active text-nowrap mx-auto"
          id="r1-tab"
          data-bs-toggle="tab"
          data-bs-target="#r1"
          type="button"
          role="tab"
          aria-controls="r1"
          aria-selected="true"
          style="color: var(--round-green)"
        >
          Round 1
        </button>
      </li>
      <li class="nav-item col-4 col-md-2" role="presentation">
        <button
          class="nav-link text-nowrap mx-auto"
          id="r2-tab"
          data-bs-toggle="tab"
          data-bs-target="#r2"
          type="button"
          role="tab"
          aria-controls="r2"
          aria-selected="false"
          style="color: var(--round-green)"
        >
          Round 2
        </button>
      </li>
      <li class="nav-item col-4 col-md-2" role="presentation">
        <button
          class="nav-link text-nowrap mx-auto"
          id="r3-tab"
          data-bs-toggle="tab"
          data-bs-target="#r3"
          type="button"
          role="tab"
          aria-controls="r3"
          aria-selected="false"
          style="color: var(--round-green)"
        >
          Round 3
        </button>
      </li>
      <li class="nav-item col-4 col-md-2" role="presentation">
        <button
          class="nav-link text-nowrap mx-auto"
          id="r4-tab"
          data-bs-toggle="tab"
          data-bs-target="#r4"
          type="button"
          role="tab"
          aria-controls="r4"
          aria-selected="false"
          style="color: var(--round-green)"
        >
          Round 4
        </button>
      </li>
      <li class="nav-item col-4 col-md-2" role="presentation">
        <button
          class="nav-link text-nowrap mx-auto"
          id="r5-tab"
          data-bs-toggle="tab"
          data-bs-target="#r5"
          type="button"
          role="tab"
          aria-controls="r5"
          aria-selected="false"
          style="color: var(--round-green)"
        >
          Round 5
        </button>
      </li>
      <li class="nav-item col-4 col-md-2" role="presentation">
        <button
          class="nav-link text-nowrap mx-auto"
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
        <div class="text-center">{{ puzzleDate }}</div>
      </div>
      <div class="tab-pane fade" id="r2" role="tabpanel" aria-labelledby="r2-tab">
        <DigitsRound :data="data['r2']"></DigitsRound>
        <div class="text-center">{{ puzzleDate }}</div>
      </div>
      <div class="tab-pane fade" id="r3" role="tabpanel" aria-labelledby="r3-tab">
        <DigitsRound :data="data['r3']"></DigitsRound>
        <div class="text-center">{{ puzzleDate }}</div>
      </div>
      <div class="tab-pane fade" id="r4" role="tabpanel" aria-labelledby="r4-tab">
        <DigitsRound :data="data['r4']"></DigitsRound>
        <div class="text-center">{{ puzzleDate }}</div>
      </div>
      <div class="tab-pane fade" id="r5" role="tabpanel" aria-labelledby="r5-tab">
        <DigitsRound :data="data['r5']"></DigitsRound>
        <div class="text-center">{{ puzzleDate }}</div>
      </div>
      <div
        class="tab-pane fade text-center mt-5 px-4"
        id="about"
        role="tabpanel"
        aria-labelledby="about-tab"
      >
        I loved to play the New York Times Digits game. Unfortunately, it was
        <a target="_blank" href="https://www.nytimes.com/games/digits">discontinued</a>. So, I built
        this version of it.
        <br />
        The source code is available
        <a target="_blank" href="https://github.com/rileypeterson/digits">here</a>.
      </div>
    </div>
  </div>
</template>

<style scoped>
.nav-link {
  font-size: 1.2rem;
}

#about-tab {
  width: 105px;
}

@media (min-width: 400px) {
  #myTab {
    width: 100%;
  }
}

/* Small devices (landscape phones, 576px and up) */
@media (min-width: 576px) {
  .container-fluid {
    padding-left: 10%;
    padding-right: 10%;
  }
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
