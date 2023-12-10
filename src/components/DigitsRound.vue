<script setup lang="ts">
import NumberCircle from './NumberCircle.vue'
import OperatorCircle from './OperatorCircle.vue'
import { ref, reactive, onMounted } from 'vue'
import { confetti } from 'tsparticles-confetti'
// @ts-ignore
import $ from 'jquery'

const props = defineProps({
  data: Object
})

const round = ref(props?.data?.round)

// The circles that the user picks and in what order
const firstCircle = ref('')
const secondCircle = ref('')
const selectedOp = ref('')
// const solutionRevealed = ref(localStorage.getItem('r' + round.value + 'Failed') === 'true' || false)
const solutionRevealed = ref(false)

const opMap = {
  times: '*',
  divide: '÷',
  minus: '-',
  plus: '+'
}

// https://devblogs.microsoft.com/typescript/announcing-typescript-3-7-beta/#optional-chaining
// Receive the actual values for each circle from the AllRounds.vue parent
const target = ref(props?.data?.target)
const upperLeft = ref(localStorage.getItem('r' + round.value + 'upperLeft') || props?.data?.n[0])
const upperCenter = ref(
  localStorage.getItem('r' + round.value + 'upperCenter') || props?.data?.n[1]
)
const upperRight = ref(localStorage.getItem('r' + round.value + 'upperRight') || props?.data?.n[2])
const lowerLeft = ref(localStorage.getItem('r' + round.value + 'lowerLeft') || props?.data?.n[3])
const lowerCenter = ref(
  localStorage.getItem('r' + round.value + 'lowerCenter') || props?.data?.n[4]
)
const lowerRight = ref(localStorage.getItem('r' + round.value + 'lowerRight') || props?.data?.n[5])
const expressions = reactive(
  JSON.parse(localStorage.getItem('r' + round.value + 'Expressions') || '[]')
)
const solutions: Array<string> = reactive(Object.values(props?.data?.how[target.value] || {}))
solutions.sort(function (a: string, b: string) {
  return a.length - b.length
})

upperLeft.value = parseInt(upperLeft.value)
upperCenter.value = parseInt(upperCenter.value)
upperRight.value = parseInt(upperRight.value)
lowerLeft.value = parseInt(lowerLeft.value)
lowerCenter.value = parseInt(lowerCenter.value)
lowerRight.value = parseInt(lowerRight.value)

// Used in merge animation
const t1 = ref('0%')
const t2 = ref('0%')

// State data
let cachedNumbers = JSON.parse(localStorage.getItem('r' + round.value + 'Numbers') || '{}')
const numbers: any = reactive({
  upperLeft: { v: upperLeft, isClicked: false, isVisible: true, isShaked: false },
  upperCenter: { v: upperCenter, isClicked: false, isVisible: true, isShaked: false },
  upperRight: { v: upperRight, isClicked: false, isVisible: true, isShaked: false },
  lowerLeft: { v: lowerLeft, isClicked: false, isVisible: true, isShaked: false },
  lowerCenter: { v: lowerCenter, isClicked: false, isVisible: true, isShaked: false },
  lowerRight: { v: lowerRight, isClicked: false, isVisible: true, isShaked: false }
})
if (!$.isEmptyObject(cachedNumbers)) {
  numbers['upperLeft']['v'] = upperLeft
  numbers['upperCenter']['v'] = upperCenter
  numbers['upperRight']['v'] = upperRight
  numbers['lowerLeft']['v'] = lowerLeft
  numbers['lowerCenter']['v'] = lowerCenter
  numbers['lowerRight']['v'] = lowerRight

  numbers['upperLeft']['isClicked'] = cachedNumbers['upperLeft']['isClicked']
  numbers['upperCenter']['isClicked'] = cachedNumbers['upperCenter']['isClicked']
  numbers['upperRight']['isClicked'] = cachedNumbers['upperRight']['isClicked']
  numbers['lowerLeft']['isClicked'] = cachedNumbers['lowerLeft']['isClicked']
  numbers['lowerCenter']['isClicked'] = cachedNumbers['lowerCenter']['isClicked']
  numbers['lowerRight']['isClicked'] = cachedNumbers['lowerRight']['isClicked']

  numbers['upperLeft']['isVisible'] = cachedNumbers['upperLeft']['isVisible']
  numbers['upperCenter']['isVisible'] = cachedNumbers['upperCenter']['isVisible']
  numbers['upperRight']['isVisible'] = cachedNumbers['upperRight']['isVisible']
  numbers['lowerLeft']['isVisible'] = cachedNumbers['lowerLeft']['isVisible']
  numbers['lowerCenter']['isVisible'] = cachedNumbers['lowerCenter']['isVisible']
  numbers['lowerRight']['isVisible'] = cachedNumbers['lowerRight']['isVisible']

  numbers['upperLeft']['isShaked'] = cachedNumbers['upperLeft']['isShaked']
  numbers['upperCenter']['isShaked'] = cachedNumbers['upperCenter']['isShaked']
  numbers['upperRight']['isShaked'] = cachedNumbers['upperRight']['isShaked']
  numbers['lowerLeft']['isShaked'] = cachedNumbers['lowerLeft']['isShaked']
  numbers['lowerCenter']['isShaked'] = cachedNumbers['lowerCenter']['isShaked']
  numbers['lowerRight']['isShaked'] = cachedNumbers['lowerRight']['isShaked']
}
let cachedOps = JSON.parse(localStorage.getItem('r' + round.value + 'Ops') || '{}')
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
  lowerRight: lowerRight.value,
  expressions: JSON.parse(JSON.stringify(expressions))
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
      // @ts-ignore
      expressions.push(fc + ' ' + opMap[op] + ' ' + sc + ' = ' + res)
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

function surrendered() {
  solutionRevealed.value = true
  if ((localStorage.getItem('r' + round.value + 'Complete') || 'false') === 'false') {
    localStorage.setItem('r' + round.value + 'Failed', 'true')
    $('#r' + round.value + '-failed').removeClass('d-none')
    // disableButtons()
  }
}

function endingConfetti() {
  // do this for 30 seconds
  var duration = 3 * 1000
  var end = Date.now() + duration

  ;(function frame() {
    // launch a few confetti from the left edge
    confetti({
      particleCount: 7,
      angle: 60,
      spread: 55,
      origin: { x: 0 }
    })
    // and launch a few from the right edge
    confetti({
      particleCount: 7,
      angle: 120,
      spread: 55,
      origin: { x: 1 }
    })

    // keep going until we are out of time
    if (Date.now() < end) {
      requestAnimationFrame(frame)
    }
  })()
}

function checkWinner() {
  if (mapCircleToValue(firstCircle.value).value === target.value) {
    if (!solutionRevealed.value && localStorage.getItem('r' + round.value + 'Failed') === 'false') {
      localStorage.setItem('r' + round.value + 'Complete', 'true')
      // Disable the buttons immediately after winning for completed rounds
      disableButtons()
      if (
        localStorage.getItem('r1Complete') === 'true' &&
        localStorage.getItem('r2Complete') === 'true' &&
        localStorage.getItem('r3Complete') === 'true' &&
        localStorage.getItem('r4Complete') === 'true' &&
        localStorage.getItem('r5Complete') === 'true'
      ) {
        endingConfetti()
      } else {
        // Baby confetti
        confetti({
          particleCount: 100,
          spread: 70,
          origin: { y: 0.6 }
        })
      }
    }

    localStorage.setItem('r' + round.value + 'Expressions', JSON.stringify(expressions))
    localStorage.setItem('r' + round.value + 'Numbers', JSON.stringify(numbers))
    localStorage.setItem('r' + round.value + 'Ops', JSON.stringify(ops))
    localStorage.setItem('r' + round.value + 'upperLeft', upperLeft.value)
    localStorage.setItem('r' + round.value + 'upperCenter', upperCenter.value)
    localStorage.setItem('r' + round.value + 'upperRight', upperRight.value)
    localStorage.setItem('r' + round.value + 'lowerLeft', lowerLeft.value)
    localStorage.setItem('r' + round.value + 'lowerCenter', lowerCenter.value)
    localStorage.setItem('r' + round.value + 'lowerRight', lowerRight.value)

    setTimeout(() => {
      // If the solution hasn't been revealed and the round hasn't been failed (survived refresh)
      if (
        !solutionRevealed.value &&
        localStorage.getItem('r' + round.value + 'Failed') === 'false'
      ) {
        $('#r' + round.value + '-complete').removeClass('d-none')
      }
      if (
        ((localStorage.getItem('r1Complete') || 'false') === 'true' ||
          (localStorage.getItem('r1Failed') || 'false') === 'true') &&
        ((localStorage.getItem('r2Complete') || 'false') === 'true' ||
          (localStorage.getItem('r2Failed') || 'false') === 'true') &&
        ((localStorage.getItem('r3Complete') || 'false') === 'true' ||
          (localStorage.getItem('r3Failed') || 'false') === 'true') &&
        ((localStorage.getItem('r4Complete') || 'false') === 'true' ||
          (localStorage.getItem('r4Failed') || 'false') === 'true') &&
        ((localStorage.getItem('r5Complete') || 'false') === 'true' ||
          (localStorage.getItem('r5Failed') || 'false') === 'true')
      ) {
        // If all rounds complete (or failed) go to round 5
        document.getElementById('r5-tab')?.click()
      } else {
        let nextRound = (round.value % 5) + 1
        for (let j = 0; j <= 5; j++) {
          if (
            (localStorage.getItem('r' + nextRound + 'Complete') || 'false') === 'true' ||
            (localStorage.getItem('r' + nextRound + 'Failed') || 'false') === 'true'
          ) {
            // If nextRound is completed:
            nextRound = (nextRound % 5) + 1
          } else {
            break
          }
        }
        nextRound = Math.min(nextRound, 5)
        document.getElementById('r' + nextRound + '-tab')?.click()
      }
    }, 2200)
  }
}

function fullReset(this: any, cell: string) {
  if (
    isOp(cell) &&
    cell === 'refresh' &&
    localStorage.getItem('r' + round.value + 'Complete') === 'false'
  ) {
    let maybeRefresh = false
    if (localStorage.getItem('r' + round.value + 'Complete') === 'false') {
      // Remove the local storage
      localStorage.removeItem('r' + round.value + 'Expressions')
      localStorage.removeItem('r' + round.value + 'Numbers')
      localStorage.removeItem('r' + round.value + 'Ops')
      localStorage.removeItem('r' + round.value + 'upperLeft')
      localStorage.removeItem('r' + round.value + 'upperCenter')
      localStorage.removeItem('r' + round.value + 'upperRight')
      localStorage.removeItem('r' + round.value + 'lowerLeft')
      localStorage.removeItem('r' + round.value + 'lowerCenter')
      localStorage.removeItem('r' + round.value + 'lowerRight')
      // localStorage.setItem('r' + round.value + 'Complete', 'false')
      maybeRefresh = true
    }

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
      for (let k in expressions) {
        expressions[k] = h?.expressions[k]
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
    if (maybeRefresh) {
      location.reload()
      localStorage.setItem('roundFromRefreshedTab', round.value)
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
      for (let k in expressions) {
        expressions[k] = h?.expressions[k]
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
    lowerRight: lowerRight.value,
    expressions: JSON.parse(JSON.stringify(expressions))
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

function disableButtons() {
  if (localStorage.getItem('r' + round.value + 'Complete') === 'true') {
    ;(document.getElementById('r' + round.value + '-upperRight') as HTMLButtonElement).setAttribute(
      'disabled',
      'disabled'
    )
    ;(
      document.getElementById('r' + round.value + '-upperCenter') as HTMLButtonElement
    ).setAttribute('disabled', 'disabled')
    ;(document.getElementById('r' + round.value + '-upperLeft') as HTMLButtonElement).setAttribute(
      'disabled',
      'disabled'
    )
    ;(document.getElementById('r' + round.value + '-lowerLeft') as HTMLButtonElement).setAttribute(
      'disabled',
      'disabled'
    )
    ;(
      document.getElementById('r' + round.value + '-lowerCenter') as HTMLButtonElement
    ).setAttribute('disabled', 'disabled')
    ;(document.getElementById('r' + round.value + '-lowerRight') as HTMLButtonElement).setAttribute(
      'disabled',
      'disabled'
    )
    ;(document.getElementById('r' + round.value + '-plus') as HTMLButtonElement).setAttribute(
      'disabled',
      'disabled'
    )
    ;(document.getElementById('r' + round.value + '-minus') as HTMLButtonElement).setAttribute(
      'disabled',
      'disabled'
    )
    ;(document.getElementById('r' + round.value + '-times') as HTMLButtonElement).setAttribute(
      'disabled',
      'disabled'
    )
    ;(document.getElementById('r' + round.value + '-divide') as HTMLButtonElement).setAttribute(
      'disabled',
      'disabled'
    )
    ;(document.getElementById('r' + round.value + '-refresh') as HTMLButtonElement).setAttribute(
      'disabled',
      'disabled'
    )
  }
}

// After mounted get the right round
onMounted(() => {
  disableButtons()
})
</script>

<template>
  <div class="container w-100">
    <div class="row justify-content-center mb-2">
      <div class="target mx-auto">{{ target }}</div>
    </div>
    <div class="row justify-content-center mb-2">
      <NumberCircle
        :id="'r' + round + '-upperLeft'"
        :v="upperLeft"
        :class="{
          green: numbers.upperLeft.isClicked,
          invisible: !numbers.upperLeft.isVisible,
          shaking: numbers.upperLeft.isShaked
        }"
        @click="handleClick('upperLeft')"
      ></NumberCircle>
      <NumberCircle
        :id="'r' + round + '-upperCenter'"
        :v="upperCenter"
        :class="{
          green: numbers.upperCenter.isClicked,
          invisible: !numbers.upperCenter.isVisible,
          shaking: numbers.upperCenter.isShaked
        }"
        @click="handleClick('upperCenter')"
      ></NumberCircle>
      <NumberCircle
        :id="'r' + round + '-upperRight'"
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
        :id="'r' + round + '-lowerLeft'"
        :v="lowerLeft"
        :class="{
          green: numbers.lowerLeft.isClicked,
          invisible: !numbers.lowerLeft.isVisible,
          shaking: numbers.lowerLeft.isShaked
        }"
        @click="handleClick('lowerLeft')"
      ></NumberCircle>
      <NumberCircle
        :id="'r' + round + '-lowerCenter'"
        :v="lowerCenter"
        :class="{
          green: numbers.lowerCenter.isClicked,
          invisible: !numbers.lowerCenter.isVisible,
          shaking: numbers.lowerCenter.isShaked
        }"
        @click="handleClick('lowerCenter')"
      ></NumberCircle>
      <NumberCircle
        :id="'r' + round + '-lowerRight'"
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
        :id="'r' + round + '-refresh'"
        op="&#8635;"
        :class="{ green: ops.refresh.isClicked, shaking: ops.refresh.isShaked }"
        @click="handleClick('refresh')"
        @dblclick="fullReset('refresh')"
      ></OperatorCircle>
      <OperatorCircle
        :id="'r' + round + '-plus'"
        op="&plus;"
        :class="{ green: ops.plus.isClicked, shaking: ops.plus.isShaked }"
        @click="handleClick('plus')"
      ></OperatorCircle>
      <OperatorCircle
        :id="'r' + round + '-minus'"
        op="&minus;"
        :class="{ green: ops.minus.isClicked, shaking: ops.minus.isShaked }"
        @click="handleClick('minus')"
      ></OperatorCircle>
      <OperatorCircle
        :id="'r' + round + '-times'"
        op="&times;"
        :class="{ green: ops.times.isClicked, shaking: ops.times.isShaked }"
        @click="handleClick('times')"
      ></OperatorCircle>
      <OperatorCircle
        :id="'r' + round + '-divide'"
        op="&divide;"
        :class="{ green: ops.divide.isClicked, shaking: ops.divide.isShaked }"
        @click="handleClick('divide')"
      ></OperatorCircle>
    </div>
    <!-- <div class="row justify-content-center">
      <button type="button" class="btn btn-outline-secondary w-25">Submit</button>
    </div> -->
    <div class="mx-auto text-center">
      <div class="mx-auto text-center" v-for="expression in expressions" :key="expression">
        {{ expression }}
      </div>
    </div>
    <div class="mx-auto text-center" v-if="solutionRevealed">
      <div class="mx-auto text-center" style="font-weight: bold">Solutions:</div>
      <div class="mx-auto text-center" v-for="n in 5">
        {{ solutions[n] }}
      </div>
    </div>
    <div class="mb-5 mx-auto text-center" v-else>
      <button
        type="button"
        class="mx-auto text-center btn border"
        style="color: var(--round-green)"
        @click="surrendered"
      >
        Reveal Solution
      </button>
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
  font-size: 72px;
  font-weight: bold;
  color: #000000;
  text-align: center;
  background: #ffffff;
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
