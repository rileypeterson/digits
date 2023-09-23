<script setup lang="ts">
import DigitsRound from './DigitsRound.vue'
import { reactive } from 'vue'

const data = reactive({
  r1: {
    n: [3, 5, 8, 10, 12, 14],
    how: {
      '129': [
        '(12 + 8) --> (20 + 3) --> (23 * 5) --> (115 + 14) --> 129',
        '(12 - 8) --> (4 * 3) --> (12 * 10) --> (120 + 14) --> (134 - 5) --> 129',
        '(12 - 8) --> (4 + 5) --> (9 * 14) --> (126 + 3) --> 129',
        '(12 - 8) --> (4 + 10) --> (14 - 5) --> (9 * 14) --> (126 + 3) --> 129',
        '(12 + 3) --> (15 * 8) --> (120 + 14) --> (134 + 5) --> (139 - 10) --> 129',
        '(12 / 3) --> (4.0 + 8) --> (12.0 * 10) --> (120.0 + 14) --> (134.0 - 5) --> 129',
        '(12 - 3) --> (9 * 14) --> (126 + 8) --> (134 - 5) --> 129',
        '(12 / 3) --> (4.0 + 14) --> (18.0 * 8) --> (144.0 - 5) --> (139.0 - 10) --> 129',
        '(12 + 5) --> (17 * 8) --> (136 + 3) --> (139 - 10) --> 129',
        '(12 * 10) --> (120 - 8) --> (112 + 3) --> (115 + 14) --> 129',
        '(12 - 10) --> (2 * 14) --> (28 * 5) --> (140 - 8) --> (132 - 3) --> 129',
        '(12 * 10) --> (120 + 14) --> (134 - 5) --> 129',
        '(8 + 3) --> (11 * 10) --> (110 + 14) --> (124 + 5) --> 129',
        '(8 * 14) --> (112 + 12) --> (124 + 5) --> 129',
        '(8 + 14) --> (22 * 12) --> (264 * 5) --> (1320 / 10) --> (132.0 - 3) --> 129',
        '(8 * 14) --> (112 + 12) --> (124 - 5) --> (119 + 10) --> 129',
        '(8 + 5) --> (13 * 12) --> (156 - 3) --> (153 - 14) --> (139 - 10) --> 129',
        '(14 - 10) --> (4 * 12) --> (48 - 5) --> (43 * 3) --> 129',
        '(14 * 10) --> (140 - 8) --> (132 - 3) --> 129',
        '(14 + 10) --> (24 * 5) --> (120 + 12) --> (132 - 3) --> 129',
        '(10 - 8) --> (2 * 12) --> (24 + 14) --> (38 + 5) --> (43 * 3) --> 129',
        '(10 / 5) --> (2.0 + 12) --> (14.0 * 8) --> (112.0 + 3) --> (115.0 + 14) --> 129'
      ]
    },
    target: 129,
    n_ways: 22,
    round: 1
  },
  r2: {
    n: [5, 7, 12, 15, 17, 19],
    how: {
      '172': [
        '(12 * 17) --> (204 + 7) --> (211 - 5) --> (206 - 15) --> (191 - 19) --> 172',
        '(12 + 17) --> (29 - 5) --> (24 * 7) --> (168 - 15) --> (153 + 19) --> 172',
        '(12 + 17) --> (29 * 5) --> (145 - 7) --> (138 + 15) --> (153 + 19) --> 172',
        '(12 * 17) --> (204 + 5) --> (209 * 15) --> (3135 / 19) --> (165.0 + 7) --> 172',
        '(12 + 15) --> (27 * 7) --> (189 - 17) --> 172',
        '(12 + 19) --> (31 * 5) --> (155 + 17) --> 172',
        '(17 + 15) --> (32 * 5) --> (160 + 12) --> 172',
        '(17 + 15) --> (32 * 5) --> (160 - 7) --> (153 + 19) --> 172',
        '(7 - 5) --> (2 * 12) --> (24 - 15) --> (9 * 17) --> (153 + 19) --> 172',
        '(7 * 15) --> (105 / 5) --> (21.0 - 12) --> (9.0 * 17) --> (153.0 + 19) --> 172',
        '(19 - 7) --> (12 * 17) --> (204 - 12) --> (192 - 5) --> (187 - 15) --> 172'
      ]
    },
    target: 172,
    n_ways: 11,
    round: 2
  },
  r3: {
    n: [5, 7, 13, 16, 18, 20],
    how: {
      '251': [
        '(16 - 5) --> (11 * 20) --> (220 + 13) --> (233 + 18) --> 251',
        '(16 * 13) --> (208 + 5) --> (213 + 20) --> (233 + 18) --> 251',
        '(16 - 13) --> (3 * 5) --> (15 + 18) --> (33 * 7) --> (231 + 20) --> 251',
        '(16 + 18) --> (34 * 7) --> (238 + 13) --> 251',
        '(5 + 7) --> (12 * 20) --> (240 + 16) --> (256 + 13) --> (269 - 18) --> 251',
        '(13 * 20) --> (260 - 16) --> (244 + 7) --> 251',
        '(13 * 20) --> (260 + 16) --> (276 - 7) --> (269 - 18) --> 251',
        '(20 - 5) --> (15 * 16) --> (240 - 7) --> (233 + 18) --> 251',
        '(7 + 18) --> (25 - 13) --> (12 * 20) --> (240 + 16) --> (256 - 5) --> 251'
      ]
    },
    target: 251,
    n_ways: 9,
    round: 3
  },
  r4: {
    n: [6, 8, 11, 17, 19, 25],
    how: {
      '460': [
        '(11 * 19) --> (209 + 6) --> (215 * 17) --> (3655 + 25) --> (3680 / 8) --> 460',
        '(17 + 25) --> (42 * 11) --> (462 - 8) --> (454 + 6) --> 460',
        '(25 * 19) --> (475 - 17) --> (458 + 8) --> (466 - 6) --> 460',
        '(8 - 6) --> (2 * 11) --> (22 * 19) --> (418 + 17) --> (435 + 25) --> 460'
      ]
    },
    target: 460,
    n_ways: 4,
    round: 4
  },
  r5: {
    n: [8, 13, 19, 21, 23, 25],
    how: {
      '478': [
        '(19 * 23) --> (437 - 13) --> (424 + 8) --> (432 + 25) --> (457 + 21) --> 478',
        '(19 * 25) --> (475 + 13) --> (488 - 23) --> (465 - 8) --> (457 + 21) --> 478',
        '(23 * 21) --> (483 - 13) --> (470 + 8) --> 478',
        '(25 * 21) --> (525 - 13) --> (512 - 19) --> (493 - 23) --> (470 + 8) --> 478'
      ]
    },
    target: 478,
    n_ways: 4,
    round: 5
  }
})
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
          style="color:var(--round-green)"
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
          style="color:#000"
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
      <div class="tab-pane fade text-center mt-5" id="about" role="tabpanel" aria-labelledby="about-tab">
        I loved to play the New York Times digits game. Unfortunately, it was <a href="https://www.nytimes.com/games/digits">discontinued</a>. So, I built this version of it.

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
