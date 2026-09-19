<script setup lang="ts">
import CostChart from './CostChart.vue'
import CostBreakdown from './CostBreakdown.vue'
import MetricCard from './MetricCard.vue'
import type { SimulationResult } from '../types/simulation'
import { formatCurrency, formatPercentage } from '../utils/formatters'

withDefaults(
  defineProps<{
    results: SimulationResult
    showHeader?: boolean
    showCharts?: boolean
    compact?: boolean
  }>(),
  {
    showHeader: true,
    showCharts: true,
    compact: false,
  },
)
</script>

<template>
  <section class="simulation-results">
    <div
      v-if="showHeader"
      class="results-header"
    >
      <div>
        <p class="eyebrow">Simulation results</p>
        <h2>{{ results.project_name || 'Simulation' }}</h2>
      </div>

      <div
        class="budget-status"
        :class="{
          'over-budget': results.median_cost > results.budget,
          'within-budget': results.median_cost <= results.budget,
        }"
      >
        {{
          results.median_cost > results.budget
            ? 'Over budget'
            : 'Within budget'
        }}
      </div>
    </div>

    <div class="results-grid">
      <MetricCard
        title="Budget"
        :value="formatCurrency(results.budget)"
        :compact="compact"
      />

      <MetricCard
        title="Mean estimated cost"
        :value="formatCurrency(results.mean_cost)"
        :compact="compact"
      />

      <MetricCard
        title="Median estimated cost"
        :value="formatCurrency(results.median_cost)"
        :compact="compact"
      />

      <MetricCard
        title="P10 estimate"
        :value="formatCurrency(results.p10)"
        :compact="compact"
      />

      <MetricCard
        title="P90 estimate"
        :value="formatCurrency(results.p90)"
        :compact="compact"
      />

      <MetricCard
        title="Over-budget probability"
        :value="formatPercentage(results.over_budget_probability)"
        :compact="compact"
      />

      <MetricCard
        title="Within-budget probability"
        :value="formatPercentage(results.under_budget_probability)"
        :compact="compact"
      />
    </div>

    <template v-if="showCharts">
      <div
        v-if="results.distribution"
        class="chart-card"
      >
        <div class="chart-header">
          <p class="eyebrow">Cost distribution</p>
          <h3>Possible renovation costs</h3>
          <p>
            The chart shows how frequently each cost range appeared
            across the simulated scenarios.
          </p>
        </div>

        <CostChart :distribution="results.distribution" />
      </div>

      <div
        v-if="results.cost_breakdown"
        class="chart-card"
      >
        <div class="chart-header">
          <p class="eyebrow">Cost breakdown</p>
          <h3>Where the estimated cost comes from</h3>
          <p>
            Average simulated cost for each renovation category.
          </p>
        </div>

        <CostBreakdown :breakdown="results.cost_breakdown" />
      </div>
    </template>
  </section>
</template>

<style scoped>
.simulation-results {
  margin-top: 32px;
}

.results-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.results-header h2 {
  margin: 0;
}

.eyebrow {
  margin: 0 0 8px;
  font-size: 13px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #666;
}

.budget-status {
  padding: 8px 14px;
  border-radius: 20px;
  font-weight: 600;
}

.over-budget {
  background: #f8d7da;
  color: #842029;
}

.within-budget {
  background: #d1e7dd;
  color: #0f5132;
}

.results-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

.chart-card {
  margin-top: 24px;
  padding: 28px;
  border: 1px solid #ddd;
  border-radius: 12px;
  background: white;
}

.chart-header {
  margin-bottom: 24px;
}

.chart-header h3 {
  margin: 0 0 8px;
  font-size: 22px;
}

.chart-header p:last-child {
  margin: 0;
  color: #666;
  line-height: 1.5;
}

@media (max-width: 800px) {
  .results-grid {
    grid-template-columns: 1fr 1fr;
  }
}

@media (max-width: 550px) {
  .results-grid {
    grid-template-columns: 1fr;
  }

  .results-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
}
</style>