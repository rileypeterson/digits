<script setup lang="ts">
import DigitsRound from './DigitsRound.vue'
import { reactive, ref, onMounted } from 'vue'
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
if (!storedDateString || (todayDate !== storedDateString && lastData)) {
  // Never been to site or it's a new date, then the data needs to be update
  localStorage.clear()
  localStorage.setItem('lastVisitDateString', todayDate)
  localStorage.setItem('r1Complete', 'false')
  localStorage.setItem('r2Complete', 'false')
  localStorage.setItem('r3Complete', 'false')
  localStorage.setItem('r4Complete', 'false')
  localStorage.setItem('r5Complete', 'false')
  localStorage.setItem('r1Failed', 'false')
  localStorage.setItem('r2Failed', 'false')
  localStorage.setItem('r3Failed', 'false')
  localStorage.setItem('r4Failed', 'false')
  localStorage.setItem('r5Failed', 'false')

  // Fetch data
  let branch = 'main'
  let dYesterday = { puzzleDate: null, r1: {}, r2: {}, r3: {}, r4: {}, r5: {} }
  function getYesterdayData() {
    $.ajax({
      url:
        'https://raw.githubusercontent.com/rileypeterson/digits/' +
        branch +
        '/data/data_yesterday.json',
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
      url:
        'https://raw.githubusercontent.com/rileypeterson/digits/' +
        branch +
        '/data/data_today.json',
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
      url:
        'https://raw.githubusercontent.com/rileypeterson/digits/' +
        branch +
        '/data/data_tomorrow.json',
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
const r1Complete = ref((localStorage.getItem('r1Complete') || 'false') === 'true')
const r2Complete = ref((localStorage.getItem('r2Complete') || 'false') === 'true')
const r3Complete = ref((localStorage.getItem('r3Complete') || 'false') === 'true')
const r4Complete = ref((localStorage.getItem('r4Complete') || 'false') === 'true')
const r5Complete = ref((localStorage.getItem('r5Complete') || 'false') === 'true')
const r1Failed = ref((localStorage.getItem('r1Failed') || 'false') === 'true')
const r2Failed = ref((localStorage.getItem('r2Failed') || 'false') === 'true')
const r3Failed = ref((localStorage.getItem('r3Failed') || 'false') === 'true')
const r4Failed = ref((localStorage.getItem('r4Failed') || 'false') === 'true')
const r5Failed = ref((localStorage.getItem('r5Failed') || 'false') === 'true')

function advanceToNextRound() {
  if (localStorage.getItem('roundFromRefreshedTab')) {
    document.getElementById('r' + localStorage.getItem('roundFromRefreshedTab') + '-tab')?.click()
    localStorage.removeItem('roundFromRefreshedTab')
    return
  }
  if (
    (localStorage.getItem('r1Complete') || 'false') === 'false' &&
    (localStorage.getItem('r1Failed') || 'false') === 'false'
  ) {
    document.getElementById('r1-tab')?.click()
  } else if (
    (localStorage.getItem('r2Complete') || 'false') === 'false' &&
    (localStorage.getItem('r2Failed') || 'false') === 'false'
  ) {
    document.getElementById('r2-tab')?.click()
  } else if (
    (localStorage.getItem('r3Complete') || 'false') === 'false' &&
    (localStorage.getItem('r3Failed') || 'false') === 'false'
  ) {
    document.getElementById('r3-tab')?.click()
  } else if (
    (localStorage.getItem('r4Complete') || 'false') === 'false' &&
    (localStorage.getItem('r4Failed') || 'false') === 'false'
  ) {
    document.getElementById('r4-tab')?.click()
  } else if (
    (localStorage.getItem('r5Complete') || 'false') === 'false' &&
    (localStorage.getItem('r5Failed') || 'false') === 'false'
  ) {
    document.getElementById('r5-tab')?.click()
  } else {
    document.getElementById('r5-tab')?.click()
  }
}

function disableButtons(round_value: string) {
  if (localStorage.getItem('r' + round_value + 'Complete') === 'true') {
    ;(document.getElementById('r' + round_value + '-upperRight') as HTMLButtonElement).setAttribute(
      'disabled',
      'disabled'
    )
    ;(
      document.getElementById('r' + round_value + '-upperCenter') as HTMLButtonElement
    ).setAttribute('disabled', 'disabled')
    ;(document.getElementById('r' + round_value + '-upperLeft') as HTMLButtonElement).setAttribute(
      'disabled',
      'disabled'
    )
    ;(document.getElementById('r' + round_value + '-lowerRight') as HTMLButtonElement).setAttribute(
      'disabled',
      'disabled'
    )
    ;(
      document.getElementById('r' + round_value + '-lowerCenter') as HTMLButtonElement
    ).setAttribute('disabled', 'disabled')
    ;(document.getElementById('r' + round_value + '-lowerLeft') as HTMLButtonElement).setAttribute(
      'disabled',
      'disabled'
    )
    ;(document.getElementById('r' + round_value + '-refresh') as HTMLButtonElement).setAttribute(
      'disabled',
      'disabled'
    )
    ;(document.getElementById('r' + round_value + '-plus') as HTMLButtonElement).setAttribute(
      'disabled',
      'disabled'
    )
    ;(document.getElementById('r' + round_value + '-minus') as HTMLButtonElement).setAttribute(
      'disabled',
      'disabled'
    )
    ;(document.getElementById('r' + round_value + '-times') as HTMLButtonElement).setAttribute(
      'disabled',
      'disabled'
    )
    ;(document.getElementById('r' + round_value + '-divide') as HTMLButtonElement).setAttribute(
      'disabled',
      'disabled'
    )
  }
}

// After mounted get the right round
onMounted(() => {
  advanceToNextRound()

  for (let r = 1; r <= 5; r++) {
    // console.log(r)
    var el = document.querySelector('#r' + r + '-tab')
    // console.log(el)
    el?.addEventListener('shown.bs.tab', function (event) {
      disableButtons(r.toString())
    })
  }
})
</script>

<template>
  <div class="container-fluid w-100">
    <div class="text-center">{{ puzzleDate }}</div>
    <ul class="nav nav-tabs justify-content-center row px-0 mx-0" id="myTab" role="tablist">
      <li class="nav-item col-4 col-lg-2" role="presentation">
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
          <p class="m-0 p-0">
            Round 1
            <img
              id="r1-complete"
              v-bind:class="r1Complete ? 'scale align-top' : 'scale align-top d-none'"
              src="@/assets/images/check-mark.png"
            />
            <img
              id="r1-failed"
              v-bind:class="r1Failed ? 'scale align-top' : 'scale align-top d-none'"
              src="@/assets/images/red-x.png"
            />
          </p>
        </button>
      </li>
      <li class="nav-item col-4 col-lg-2" role="presentation">
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
          <p class="m-0 p-0">
            Round 2
            <img
              id="r2-complete"
              v-bind:class="r2Complete ? 'scale align-top' : 'scale align-top d-none'"
              src="@/assets/images/check-mark.png"
            />
            <img
              id="r2-failed"
              v-bind:class="r2Failed ? 'scale align-top' : 'scale align-top d-none'"
              src="@/assets/images/red-x.png"
            />
          </p>
        </button>
      </li>
      <li class="nav-item col-4 col-lg-2" role="presentation">
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
          <p class="m-0 p-0">
            Round 3
            <img
              id="r3-complete"
              v-bind:class="r3Complete ? 'scale align-top' : 'scale align-top d-none'"
              src="@/assets/images/check-mark.png"
            />
            <img
              id="r3-failed"
              v-bind:class="r3Failed ? 'scale align-top' : 'scale align-top d-none'"
              src="@/assets/images/red-x.png"
            />
          </p>
        </button>
      </li>
      <li class="nav-item col-4 col-lg-2" role="presentation">
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
          <p class="m-0 p-0">
            Round 4
            <img
              id="r4-complete"
              v-bind:class="r4Complete ? 'scale align-top' : 'scale align-top d-none'"
              src="@/assets/images/check-mark.png"
            />
            <img
              id="r4-failed"
              v-bind:class="r4Failed ? 'scale align-top' : 'scale align-top d-none'"
              src="@/assets/images/red-x.png"
            />
          </p>
        </button>
      </li>
      <li class="nav-item col-4 col-lg-2" role="presentation">
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
          <p class="m-0 p-0">
            Round 5
            <img
              id="r5-complete"
              v-bind:class="r5Complete ? 'scale align-top' : 'scale align-top d-none'"
              src="@/assets/images/check-mark.png"
            />
            <img
              id="r5-failed"
              v-bind:class="r5Failed ? 'scale align-top' : 'scale align-top d-none'"
              src="@/assets/images/red-x.png"
            />
          </p>
        </button>
      </li>
      <li class="nav-item col-4 col-lg-2" role="presentation">
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
.scale {
  height: auto;
  width: 1.5em;
}

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
