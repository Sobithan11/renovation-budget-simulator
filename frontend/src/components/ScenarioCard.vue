<script setup lang="ts">
import MetricCard from './MetricCard.vue'
import type { Scenario } from '../types/simulation'
import { formatCurrency, formatPercentage } from '../utils/formatters'

defineProps<{
  scenario: Scenario
}>()

const emit = defineEmits<{
  remove: [scenarioId: number]
}>()
</script>

<template>
  <article class="scenario-card">
    <div class="scenario-card-header">
      <h4>{{ scenario.name }}</h4>

      <button
        class="remove-button"
        type="button"
        @click="emit('remove', scenario.id)"
      >
        Remove
      </button>
    </div>

    <div class="scenario-details">
      <span>
        Budget: {{ formatCurrency(scenario.budget) }}
      </span>

      <span>
        Extension: {{ scenario.extension_size }} m²
      </span>

      <span>
        Kitchen: {{ scenario.kitchen_spec }}
      </span>

      <span>
        Bathroom: {{ scenario.bathroom_spec }}
      </span>
    </div>

    <div class="scenario-metrics">
      <MetricCard
        title="Median"
        :value="formatCurrency(scenario.result.median_cost)"
        compact
      />

      <MetricCard
        title="P90"
        :value="formatCurrency(scenario.result.p90)"
        compact
      />

      <MetricCard
        title="Over-budget risk"
        :value="formatPercentage(scenario.result.over_budget_probability)"
        compact
      />
    </div>
  </article>
</template>

<style scoped>
.scenario-card {
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 10px;
  background: white;
}

.scenario-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.scenario-card-header h4 {
  margin: 0;
  font-size: 17px;
}

.remove-button {
  padding: 7px 12px;
  border: 1px solid #ccc;
  border-radius: 6px;
  background: white;
  color: #222;
  cursor: pointer;
}

.remove-button:hover {
  background: #f5f5f5;
}

.scenario-details {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  margin-top: 14px;
  color: #666;
  font-size: 14px;
}

.scenario-metrics {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  margin-top: 18px;
}

@media (max-width: 700px) {
  .scenario-metrics {
    grid-template-columns: 1fr;
  }
}
</style>