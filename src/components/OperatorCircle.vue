<script setup lang="ts">
const props = defineProps<{
  path: String
}>()

function getImageUrl() {
  let s = new URL(`../assets/images/${props.path}`, import.meta.url)
  return s.href
}
</script>

<template>
  <button class="operator-circle">
    <img :src="getImageUrl()" />
  </button>
</template>

<style scoped>
.operator-circle.green {
  transition: all var(--color-change-time);
  background: var(--green);
  color: white;
  border: 3px solid transparent;
}

.operator-circle {
  transition: all var(--color-change-time);
  width: 48px;
  height: 48px;
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

.operator-circle > img {
  width: 32px;
  height: 32px;
}

@media (min-width: 400px) {
  .operator-circle {
    transition: all var(--color-change-time);
    width: 56px;
    height: 56px;
    border-radius: 50%;
    border: 3px dashed black;
    font-size: 48px;
    font-weight: bold;
    color: #ffffff;
    display: flex; /* or inline-flex */
    align-items: center;
    justify-content: center;
    background: #000000;
    margin-left: 4px;
    margin-right: 4px;
  }
  .operator-circle > img {
    width: 38px;
    height: 38px;
  }
}

/* Small devices (landscape phones, 576px and up) */
@media (min-width: 576px) {
  .operator-circle {
    transition: all var(--color-change-time);
    width: 72px;
    height: 72px;
    border-radius: 50%;
    border: 3px dashed black;
    font-size: 56px;
    font-weight: bold;
    color: #ffffff;
    background: #000000;
    margin-left: 4px;
    margin-right: 4px;
    padding: 0;
  }
  .operator-circle > img {
    width: 46px;
    height: 46px;
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
