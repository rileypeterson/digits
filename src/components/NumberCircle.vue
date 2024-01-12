<script setup lang="ts">
defineProps<{
  v: number
}>()
</script>

<template>
  <button class="number-circle">{{ v }}</button>
</template>

<style scoped>
.number-circle.green {
  transition: all var(--color-change-time);
  background: var(--green);
  color: white;
  border: none;
}

.number-circle {
  transition: all var(--color-change-time);
  width: 88px;
  height: 88px;
  border-radius: 50%;
  border: 3px dashed black;
  font-size: 36px;
  font-weight: bold;
  color: #000000;
  display: flex; /* or inline-flex */
  align-items: center;
  justify-content: center;
  background: #ffffff;
  margin-left: 5px;
  margin-right: 5px;
}

@media (min-width: 400px) {
  .number-circle {
    transition: all var(--color-change-time);
    width: 105px;
    height: 105px;
    border-radius: 50%;
    border: 3px dashed black;
    font-size: 45px;
    font-weight: bold;
    color: #000000;
    display: flex; /* or inline-flex */
    align-items: center;
    justify-content: center;
    background: #ffffff;
    margin-left: 5px;
    margin-right: 5px;
  }
}

/* Small devices (landscape phones, 576px and up) */
@media (min-width: 576px) {
  .number-circle {
    transition: all var(--color-change-time);
    width: 136px;
    height: 136px;
    border-radius: 50%;
    border: 3px dashed black;
    font-size: 56px;
    font-weight: bold;
    color: #000000;
    display: flex; /* or inline-flex */
    align-items: center;
    justify-content: center;
    background: #ffffff;
    margin-left: 5px;
    margin-right: 5px;
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
