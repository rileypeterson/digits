<script setup lang="ts">
import DigitsRound from './DigitsRound.vue'
import { nextTick, onMounted, reactive, ref } from 'vue'

type PuzzleData = {
  puzzleDate: string | null
  r1: Record<string, unknown>
  r2: Record<string, unknown>
  r3: Record<string, unknown>
  r4: Record<string, unknown>
  r5: Record<string, unknown>
}

function emptyPuzzleData(): PuzzleData {
  return {
    puzzleDate: null,
    r1: {},
    r2: {},
    r3: {},
    r4: {},
    r5: {}
  }
}

async function fetchPuzzleData(branch: string, filename: string): Promise<PuzzleData> {
  const response = await fetch(
    `https://raw.githubusercontent.com/rileypeterson/digits/${branch}/data/${filename}`
  )
  if (!response.ok) {
    throw new Error(`Failed to load ${filename}: ${response.status}`)
  }
  return response.json()
}

// Get the localize date string for the player
const today = new Date()
const todayDate = [
  today.getFullYear(),
  ('0' + (today.getMonth() + 1)).slice(-2),
  ('0' + today.getDate()).slice(-2)
].join('-')
const TOTAL_ROUNDS = 5
const data = reactive<PuzzleData>(emptyPuzzleData())
const puzzleDate = ref('')
const dataLoaded = ref(false)
const r1Complete = ref(false)
const r2Complete = ref(false)
const r3Complete = ref(false)
const r4Complete = ref(false)
const r5Complete = ref(false)
const r1Failed = ref(false)
const r2Failed = ref(false)
const r3Failed = ref(false)
const r4Failed = ref(false)
const r5Failed = ref(false)

function resetStoredRoundStatuses() {
  for (let round = 1; round <= TOTAL_ROUNDS; round++) {
    localStorage.setItem(`r${round}Complete`, 'false')
    localStorage.setItem(`r${round}Failed`, 'false')
  }
}

function syncRoundStatusRefs() {
  r1Complete.value = (localStorage.getItem('r1Complete') || 'false') === 'true'
  r2Complete.value = (localStorage.getItem('r2Complete') || 'false') === 'true'
  r3Complete.value = (localStorage.getItem('r3Complete') || 'false') === 'true'
  r4Complete.value = (localStorage.getItem('r4Complete') || 'false') === 'true'
  r5Complete.value = (localStorage.getItem('r5Complete') || 'false') === 'true'
  r1Failed.value = (localStorage.getItem('r1Failed') || 'false') === 'true'
  r2Failed.value = (localStorage.getItem('r2Failed') || 'false') === 'true'
  r3Failed.value = (localStorage.getItem('r3Failed') || 'false') === 'true'
  r4Failed.value = (localStorage.getItem('r4Failed') || 'false') === 'true'
  r5Failed.value = (localStorage.getItem('r5Failed') || 'false') === 'true'
}

async function initializePuzzleData() {
  const storedDateString = localStorage.getItem('lastVisitDateString')
  const lastData = localStorage.getItem('lastData')
  if (!storedDateString || !lastData || todayDate !== storedDateString) {
    // Never been to site or it's a new date, then the data needs to be update
    localStorage.clear()
    localStorage.setItem('lastVisitDateString', todayDate)
    resetStoredRoundStatuses()

    // Fetch data
    const branch = 'main'
    const [dYesterday, dToday, dTomorrow] = await Promise.all([
      fetchPuzzleData(branch, 'data_yesterday.json'),
      fetchPuzzleData(branch, 'data_today.json'),
      fetchPuzzleData(branch, 'data_tomorrow.json')
    ])

    // Get the date that comes with each payload
    const dYesterdayDate = dYesterday.puzzleDate
    const dTodayDate = dToday.puzzleDate
    const dTomorrowDate = dTomorrow.puzzleDate

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

  const storedPuzzleData = JSON.parse(localStorage.getItem('lastData') || 'null')
  Object.assign(data, storedPuzzleData || emptyPuzzleData())
  puzzleDate.value = localStorage.getItem('puzzleDate') || ''
  syncRoundStatusRefs()
  dataLoaded.value = true
  await nextTick()
  advanceToNextRound()

  for (let r = 1; r <= 5; r++) {
    const el = document.querySelector('#r' + r + '-tab')
    el?.addEventListener('shown.bs.tab', function () {
      disableButtons(r.toString())
    })
  }
}
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
  void initializePuzzleData()
})
</script>

<template>
  <div class="container-fluid w-100">
    <div class="text-center">{{ puzzleDate }}</div>
    <ul v-if="dataLoaded" class="nav nav-tabs justify-content-center row px-0 mx-0" id="myTab" role="tablist">
      <li class="nav-item col-4 col-lg-2 mx-0 px-0" role="presentation">
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
          <p class="m-0 p-0 d-flex align-items-center">
            Round 1
            <img
              id="r1-complete"
              v-bind:class="r1Complete ? 'scale align-top ms-1' : 'scale align-top d-none'"
              src="@/assets/images/check-mark.png"
            />
            <img
              id="r1-failed"
              v-bind:class="r1Failed ? 'scale align-top ms-1' : 'scale align-top d-none'"
              src="@/assets/images/red-x.png"
            />
          </p>
        </button>
      </li>
      <li class="nav-item col-4 col-lg-2 mx-0 px-0" role="presentation">
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
          <p class="m-0 p-0 d-flex align-items-center">
            Round 2
            <img
              id="r2-complete"
              v-bind:class="r2Complete ? 'scale align-top ms-1' : 'scale align-top d-none'"
              src="@/assets/images/check-mark.png"
            />
            <img
              id="r2-failed"
              v-bind:class="r2Failed ? 'scale align-top ms-1' : 'scale align-top d-none'"
              src="@/assets/images/red-x.png"
            />
          </p>
        </button>
      </li>
      <li class="nav-item col-4 col-lg-2 mx-0 px-0" role="presentation">
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
          <p class="m-0 p-0 d-flex align-items-center">
            Round 3
            <img
              id="r3-complete"
              v-bind:class="r3Complete ? 'scale align-top ms-1' : 'scale align-top d-none'"
              src="@/assets/images/check-mark.png"
            />
            <img
              id="r3-failed"
              v-bind:class="r3Failed ? 'scale align-top ms-1' : 'scale align-top d-none'"
              src="@/assets/images/red-x.png"
            />
          </p>
        </button>
      </li>
      <li class="nav-item col-4 col-lg-2 mx-0 px-0" role="presentation">
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
          <p class="m-0 p-0 d-flex align-items-center">
            Round 4
            <img
              id="r4-complete"
              v-bind:class="r4Complete ? 'scale align-top ms-1' : 'scale align-top d-none'"
              src="@/assets/images/check-mark.png"
            />
            <img
              id="r4-failed"
              v-bind:class="r4Failed ? 'scale align-top ms-1' : 'scale align-top d-none'"
              src="@/assets/images/red-x.png"
            />
          </p>
        </button>
      </li>
      <li class="nav-item col-4 col-lg-2 mx-0 px-0" role="presentation">
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
          <p class="m-0 p-0 d-flex align-items-center">
            Round 5
            <img
              id="r5-complete"
              v-bind:class="r5Complete ? 'scale align-top ms-1' : 'scale align-top d-none'"
              src="@/assets/images/check-mark.png"
            />
            <img
              id="r5-failed"
              v-bind:class="r5Failed ? 'scale align-top ms-1' : 'scale align-top d-none'"
              src="@/assets/images/red-x.png"
            />
          </p>
        </button>
      </li>
      <li class="nav-item col-4 col-lg-2 mx-0 px-0" role="presentation">
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
    <div v-if="dataLoaded" class="tab-content" id="myTabContent">
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
        <a target="_blank" rel="noopener noreferrer" href="https://www.nytimes.com/games/digits">discontinued</a>. So, I built
        this version of it.
        <br />
        The source code is available
        <a target="_blank" rel="noopener noreferrer" href="https://github.com/rileypeterson/digits">here</a>.
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
  font-size: 0.8rem;
}

#about-tab {
  width: 105px;
}

@media (min-width: 400px) {
  .scale {
    height: auto;
    width: 1.5em;
  }

  .nav-link {
    font-size: 1.05rem;
  }

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
