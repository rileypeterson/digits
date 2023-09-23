<script setup lang="ts">
import NumberCircle from './NumberCircle.vue'
import OperatorCircle from './OperatorCircle.vue'
import { ref, reactive } from 'vue'
import { confetti } from 'tsparticles-confetti'

const props = defineProps({
  data: Object
})

// The circles that the user picks and in what order
const firstCircle = ref('')
const secondCircle = ref('')
const selectedOp = ref('')

// https://devblogs.microsoft.com/typescript/announcing-typescript-3-7-beta/#optional-chaining
// Receive the actual values for each circle from the AllRounds.vue parent
const target = ref(props?.data?.target)
const upperLeft = ref(props?.data?.n[0])
const upperCenter = ref(props?.data?.n[1])
const upperRight = ref(props?.data?.n[2])
const lowerLeft = ref(props?.data?.n[3])
const lowerCenter = ref(props?.data?.n[4])
const lowerRight = ref(props?.data?.n[5])
const round = ref(props?.data?.round)

// Used in merge animation
const t1 = ref('0%')
const t2 = ref('0%')

// State data
const numbers: any = reactive({
  upperLeft: { v: upperLeft, isClicked: false, isVisible: true, isShaked: false },
  upperCenter: { v: upperCenter, isClicked: false, isVisible: true, isShaked: false },
  upperRight: { v: upperRight, isClicked: false, isVisible: true, isShaked: false },
  lowerLeft: { v: lowerLeft, isClicked: false, isVisible: true, isShaked: false },
  lowerCenter: { v: lowerCenter, isClicked: false, isVisible: true, isShaked: false },
  lowerRight: { v: lowerRight, isClicked: false, isVisible: true, isShaked: false }
})
const ops: any = reactive({
  refresh: { isClicked: false, isShaked: false },
  plus: { isClicked: false, isShaked: false },
  minus: { isClicked: false, isShaked: false },
  times: { isClicked: false, isShaked: false },
  divide: { isClicked: false, isShaked: false }
})

let h0 = {
  numbers: JSON.parse(JSON.stringify(numbers)),
  ops: JSON.parse(JSON.stringify(ops)),
  firstCircle: firstCircle.value,
  secondCircle: secondCircle.value,
  selectedOp: selectedOp.value,
  upperLeft: upperLeft.value,
  upperCenter: upperCenter.value,
  upperRight: upperRight.value,
  lowerLeft: lowerLeft.value,
  lowerCenter: lowerCenter.value,
  lowerRight: lowerRight.value
}
let history = [h0]

// Start of functions
const isOp = (s: string) => {
  return ['refresh', 'plus', 'minus', 'times', 'divide'].includes(s)
}

function mapCircleToValue(s: string) {
  if (s == 'upperLeft') return upperLeft
  if (s == 'upperCenter') return upperCenter
  if (s == 'upperRight') return upperRight
  if (s == 'lowerLeft') return lowerLeft
  if (s == 'lowerCenter') return lowerCenter
  if (s == 'lowerRight') return lowerRight
}

function applyOp(fc: number, op: string, sc: number) {
  let res = -1
  if (op === 'plus') {
    res = fc + sc
  } else if (op == 'minus') {
    res = fc - sc
  } else if (op == 'times') {
    res = fc * sc
  } else if (op == 'divide') {
    res = fc / sc
  }
  if (res >= 0 && Number.isInteger(res)) {
    setTimeout(function () {
      mapCircleToValue(secondCircle.value).value = res
      checkWinner()
    }, 400)
    return true
  } else {
    return false
  }
}

function setMergeAnimation(c1: string, c2: string) {
  // Handle vertical rise and fall
  if (c1.includes('upper') && c2.includes('upper')) {
    // On upper row
    t2.value = '0%'
  }
  if (c1.includes('lower') && c2.includes('lower')) {
    // On lower row
    t2.value = '0%'
  }
  if (c1.includes('lower') && c2.includes('upper')) {
    // Move up
    t2.value = '-100%'
  }
  if (c1.includes('upper') && c2.includes('lower')) {
    // Move down
    t2.value = '100%'
  }

  // Handle horizontal
  // No movement
  if (c1.includes('Left') && c2.includes('Left')) {
    t1.value = '0%'
  }
  if (c1.includes('Center') && c2.includes('Center')) {
    t1.value = '0%'
  }
  if (c1.includes('Right') && c2.includes('Right')) {
    t1.value = '0%'
  }

  // Move one right
  if (
    (c1.includes('Left') && c2.includes('Center')) ||
    (c1.includes('Center') && c2.includes('Right'))
  ) {
    t1.value = '100%'
  }

  // Move one left
  if (
    (c1.includes('Right') && c2.includes('Center')) ||
    (c1.includes('Center') && c2.includes('Left'))
  ) {
    t1.value = '-100%'
  }

  // Move two right
  if (c1.includes('Left') && c2.includes('Right')) {
    t1.value = '200%'
  }

  // Move two left
  if (c1.includes('Right') && c2.includes('Left')) {
    t1.value = '-200%'
  }
}

function checkWinner() {
  if (mapCircleToValue(firstCircle.value).value === target.value) {
    confetti({
      particleCount: 100,
      spread: 70,
      origin: { y: 0.6 }
    })
    setTimeout(() => {
      if (round.value < 5) {
        let next_round = 'r' + (round.value + 1) + '-tab'
        document.getElementById(next_round)?.click()
      }
    }, 2200)
  }
}

function fullReset(this: any, cell: string) {
  if (isOp(cell) && cell === 'refresh') {
    while (history.length > 1) {
      history.pop()
    }
    if (history.length >= 1) {
      let h = history.pop()
      for (let k in numbers) {
        for (let j in numbers[k]) numbers[k][j] = h?.numbers[k][j]
      }
      for (let k in ops) {
        for (let j in ops[k]) ops[k][j] = h?.ops[k][j]
      }
      firstCircle.value = h?.firstCircle || ''
      secondCircle.value = h?.secondCircle || ''
      selectedOp.value = h?.selectedOp || ''
      upperLeft.value = h?.upperLeft || ''
      upperCenter.value = h?.upperCenter || ''
      upperRight.value = h?.upperRight || ''
      lowerLeft.value = h?.lowerLeft || ''
      lowerCenter.value = h?.lowerCenter || ''
      lowerRight.value = h?.lowerRight || ''
    }
  }
  return
}

function handleClick(cell: string) {
  if (isOp(cell) && cell === 'refresh') {
    // Empty history
    if (history.length >= 1) {
      let h = history.pop()
      for (let k in numbers) {
        for (let j in numbers[k]) numbers[k][j] = h?.numbers[k][j]
      }
      for (let k in ops) {
        for (let j in ops[k]) ops[k][j] = h?.ops[k][j]
      }
      firstCircle.value = h?.firstCircle || ''
      secondCircle.value = h?.secondCircle || ''
      selectedOp.value = h?.selectedOp || ''
      upperLeft.value = h?.upperLeft || ''
      upperCenter.value = h?.upperCenter || ''
      upperRight.value = h?.upperRight || ''
      lowerLeft.value = h?.lowerLeft || ''
      lowerCenter.value = h?.lowerCenter || ''
      lowerRight.value = h?.lowerRight || ''
    }
    return
  }
  // Store to history
  h0 = {
    numbers: JSON.parse(JSON.stringify(numbers)),
    ops: JSON.parse(JSON.stringify(ops)),
    firstCircle: firstCircle.value,
    secondCircle: secondCircle.value,
    selectedOp: selectedOp.value,
    upperLeft: upperLeft.value,
    upperCenter: upperCenter.value,
    upperRight: upperRight.value,
    lowerLeft: lowerLeft.value,
    lowerCenter: lowerCenter.value,
    lowerRight: lowerRight.value
  }
  history.push(h0)

  // TODO: Where does this belong?
  // Should do for ops too?
  // Set shake to false
  for (let circle in numbers) {
    numbers[circle].isShaked = false
  }

  if (firstCircle.value && !isOp(cell) && (selectedOp.value === '' || firstCircle.value == cell)) {
    // Unset first number cell
    if (firstCircle.value == cell) {
      // Case when you try and select secondCircle == firstCircle after op
      selectedOp.value = ''
      for (let op in ops) {
        ops[op].isClicked = false
      }
    }
    let og_value = firstCircle.value
    firstCircle.value = ''
    for (let circle in numbers) {
      numbers[circle].isClicked = false
    }
    if (cell != og_value) handleClick(cell)
    return
  }

  if (firstCircle.value === '' && !isOp(cell)) {
    // Click first number cell
    firstCircle.value = cell
    numbers[cell].isClicked = true
    return
  }
  if (firstCircle.value && selectedOp.value === '' && isOp(cell)) {
    // Selecting first op
    selectedOp.value = cell
    ops[cell].isClicked = true
    return
  }
  if (firstCircle.value && selectedOp.value && isOp(cell)) {
    // Unselecting an op or selecting a different op
    if (cell == selectedOp.value) {
      // Unselecting an op
      selectedOp.value = ''
      ops[cell].isClicked = false
    } else {
      // Selecting a different op
      for (let op in ops) {
        ops[op].isClicked = false
      }
      selectedOp.value = cell
      ops[cell].isClicked = true
    }

    return
  }
  if (firstCircle.value && selectedOp.value && !isOp(cell)) {
    secondCircle.value = cell
    numbers[cell].isClicked = true
    // Valid operation
    let fc: number = mapCircleToValue(firstCircle.value).value
    let op: string = selectedOp.value
    let sc: number = mapCircleToValue(secondCircle.value).value
    let t = applyOp(fc, op, sc)
    if (t) {
      // Merge animation
      setMergeAnimation(firstCircle.value, secondCircle.value)
      numbers[firstCircle.value].isVisible = false
      numbers[firstCircle.value].isClicked = false
      // Difference between the actual game
      numbers[secondCircle.value].isClicked = true
      firstCircle.value = secondCircle.value
      // secondCircle.value = ''

      ops[selectedOp.value].isClicked = false
      selectedOp.value = ''
    } else {
      // Invalid op
      // Shake animation
      // this[secondCircle.value] = ''
      numbers[secondCircle.value].isClicked = false
      numbers[secondCircle.value].isShaked = true
      setTimeout(() => {
        numbers[secondCircle.value].isShaked = false
      }, 820)
      numbers[firstCircle.value].isShaked = true
      setTimeout(() => {
        numbers[firstCircle.value].isShaked = false
      }, 820)
      ops[selectedOp.value].isShaked = true
      setTimeout(() => {
        ops[selectedOp.value].isShaked = false
      }, 820)
      if (history.length >= 1) {
        history.pop()
      }
    }
    return
  }
  if (firstCircle.value == '' && isOp(cell)) {
    ops[cell].isShaked = true
    setTimeout(() => {
      ops[cell].isShaked = false
    }, 820)
    if (history.length >= 1) {
      history.pop()
    }
    // Shake animation
    // Clicking operator first?
    return
  }
  console.log('unaccounted')
}
</script>

<template>
  <div class="container w-100">
    <div class="row justify-content-center mb-2">
        <div class="target mx-auto">{{ target }}</div>
    </div>
    <div class="row justify-content-center mb-2">
      <NumberCircle
        :v="upperLeft"
        :class="{
          green: numbers.upperLeft.isClicked,
          invisible: !numbers.upperLeft.isVisible,
          shaking: numbers.upperLeft.isShaked
        }"
        @click="handleClick('upperLeft')"
      ></NumberCircle>
      <NumberCircle
        :v="upperCenter"
        :class="{
          green: numbers.upperCenter.isClicked,
          invisible: !numbers.upperCenter.isVisible,
          shaking: numbers.upperCenter.isShaked
        }"
        @click="handleClick('upperCenter')"
      ></NumberCircle>
      <NumberCircle
        :v="upperRight"
        :class="{
          green: numbers.upperRight.isClicked,
          invisible: !numbers.upperRight.isVisible,
          shaking: numbers.upperRight.isShaked
        }"
        @click="handleClick('upperRight')"
      ></NumberCircle>
    </div>
    <div class="row justify-content-center mb-3">
      <NumberCircle
        :v="lowerLeft"
        :class="{
          green: numbers.lowerLeft.isClicked,
          invisible: !numbers.lowerLeft.isVisible,
          shaking: numbers.lowerLeft.isShaked
        }"
        @click="handleClick('lowerLeft')"
      ></NumberCircle>
      <NumberCircle
        :v="lowerCenter"
        :class="{
          green: numbers.lowerCenter.isClicked,
          invisible: !numbers.lowerCenter.isVisible,
          shaking: numbers.lowerCenter.isShaked
        }"
        @click="handleClick('lowerCenter')"
      ></NumberCircle>
      <NumberCircle
        :v="lowerRight"
        :class="{
          green: numbers.lowerRight.isClicked,
          invisible: !numbers.lowerRight.isVisible,
          shaking: numbers.lowerRight.isShaked
        }"
        @click="handleClick('lowerRight')"
      ></NumberCircle>
    </div>
    <div class="row justify-content-center mb-4">
      <OperatorCircle
        op="&#8635;"
        :class="{ green: ops.refresh.isClicked, shaking: ops.refresh.isShaked }"
        @click="handleClick('refresh')"
        @dblclick="fullReset('refresh')"
      ></OperatorCircle>
      <OperatorCircle
        op="&plus;"
        :class="{ green: ops.plus.isClicked, shaking: ops.plus.isShaked }"
        @click="handleClick('plus')"
      ></OperatorCircle>
      <OperatorCircle
        op="&minus;"
        :class="{ green: ops.minus.isClicked, shaking: ops.minus.isShaked }"
        @click="handleClick('minus')"
      ></OperatorCircle>
      <OperatorCircle
        op="&times;"
        :class="{ green: ops.times.isClicked, shaking: ops.times.isShaked }"
        @click="handleClick('times')"
      ></OperatorCircle>
      <OperatorCircle
        op="&divide;"
        :class="{ green: ops.divide.isClicked, shaking: ops.divide.isShaked }"
        @click="handleClick('divide')"
      ></OperatorCircle>
    </div>
    <div class="row justify-content-center">
      <button type="button" class="btn btn-outline-secondary w-25">Submit</button>
    </div>
  </div>
</template>

<style scoped>
.invisible {
  visibility: hidden;
  opacity: 0.5;
  transform: translate(v-bind('t1'), v-bind('t2'));
  transition: all 0.4s linear;
}

.shaking {
  animation: shake 0.82s cubic-bezier(0.36, 0.07, 0.19, 0.97) both;
  transform: translate3d(0, 0, 0);
  backface-visibility: hidden;
  perspective: 1000px;
}

@keyframes shake {
  10%,
  90% {
    transform: translate3d(-1px, 0, 0);
  }

  20%,
  80% {
    transform: translate3d(2px, 0, 0);
  }

  30%,
  50%,
  70% {
    transform: translate3d(-4px, 0, 0);
  }

  40%,
  60% {
    transform: translate3d(4px, 0, 0);
  }
}

.target {
  width: 300px;
  height: 150px;
  line-height: 150px;
  font-size: 58px;
  font-weight: bold;
  color: #000000;
  text-align: center;
  background: #ffffff;
}

@media (min-width: 400px) {
  .target {
    width: 300px;
    height: 150px;
    line-height: 150px;
    font-size: 72px;
    font-weight: bold;
    color: #000000;
    text-align: center;
    background: #ffffff;
  }
}

/* Small devices (landscape phones, 576px and up) */
@media (min-width: 576px) {
  .target {
    width: 300px;
    height: 150px;
    line-height: 150px;
    font-size: 80px;
    font-weight: bold;
    color: #000000;
    text-align: center;
    background: #ffffff;
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
