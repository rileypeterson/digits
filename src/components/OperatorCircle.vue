<script setup lang="ts">
defineProps<{
  op: string
}>()
</script>

<template>
  <button class="operator-circle">
    <span>{{ op }}</span>
  </button>
</template>

<style scoped>
.operator-circle > span {
  position: relative;
  top: calc(50% - 25px);
}

.operator-circle.green {
  transition: all var(--color-change-time);
  background: var(--green);
  color: white;
  border: 3px solid transparent;
}

.operator-circle {
  transition: all var(--color-change-time);
  width: 50px;
  height: 50px;
  border-radius: 50%;
  border: 3px dashed black;
  font-size: 40px;
  font-weight: bold;
  color: #ffffff;
  display: flex; /* or inline-flex */
  align-items: center;
  justify-content: center;
  background: #000000;
  margin-left: 4px;
  margin-right: 4px;
}

@media (min-width: 400px) {
  .operator-circle {
    transition: all var(--color-change-time);
    width: 60px;
    height: 60px;
    border-radius: 50%;
    border: 3px dashed black;
    font-size: 50px;
    font-weight: bold;
    color: #ffffff;
    display: flex; /* or inline-flex */
    align-items: center;
    justify-content: center;
    background: #000000;
    margin-left: 4px;
    margin-right: 4px;
  }
  .operator-circle > span {
    position: relative;
    top: calc(50% - 30px);
  }
}

/* Small devices (landscape phones, 576px and up) */
@media (min-width: 576px) {
  .operator-circle {
    transition: all var(--color-change-time);
    width: 80px;
    height: 80px;
    border-radius: 50%;
    border: 3px dashed black;
    font-size: 60px;
    font-weight: bold;
    color: #ffffff;
    background: #000000;
    margin-left: 4px;
    margin-right: 4px;
    padding: 0;
  }
  .operator-circle > span {
    position: relative;
    top: calc(50% - 40px);
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
