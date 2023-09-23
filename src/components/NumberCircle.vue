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
  width: 80px;
  height: 80px;
  border-radius: 50%;
  border: 3px dashed black;
  font-size: 32px;
  font-weight: bold;
  color: #000000;
  display: flex; /* or inline-flex */
  align-items: center;
  justify-content: center;
  background: #ffffff;
  margin-left: 10px;
}

@media (min-width: 400px) {
  .number-circle {
    transition: all var(--color-change-time);
    width: 125px;
    height: 125px;
    border-radius: 50%;
    border: 3px dashed black;
    font-size: 50px;
    font-weight: bold;
    color: #000000;
    display: flex; /* or inline-flex */
    align-items: center;
    justify-content: center;
    background: #ffffff;
    margin-left: 10px;
  }
}

/* Small devices (landscape phones, 576px and up) */
@media (min-width: 576px) {
  .number-circle {
    transition: all var(--color-change-time);
    width: 150px;
    height: 150px;
    border-radius: 50%;
    border: 3px dashed black;
    font-size: 60px;
    font-weight: bold;
    color: #000000;
    display: flex; /* or inline-flex */
    align-items: center;
    justify-content: center;
    background: #ffffff;
    margin-left: 10px;
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
