<script setup lang="ts">
defineProps<{
  title: string
  value: string
  compact?: boolean
}>()
</script>

<template>
  <article
    class="metric-card"
    :class="{ compact }"
  >
    <p>{{ title }}</p>
    <strong>{{ value }}</strong>
  </article>
</template>

<style scoped>
.metric-card {
  padding: 24px;
  border: 1px solid #ddd;
  border-radius: 12px;
  background: white;
}

.metric-card p {
  margin: 0 0 10px;
  color: #666;
  font-size: 14px;
}

.metric-card strong {
  font-size: 24px;
}

.metric-card.compact {
  padding: 18px;
  border-color: #eee;
  background: #fafafa;
}

.metric-card.compact strong {
  font-size: 20px;
}
</style>