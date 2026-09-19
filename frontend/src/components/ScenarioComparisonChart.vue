<script setup lang="ts">
import { computed } from 'vue'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Tooltip,
  Legend,
} from 'chart.js'
import { Bar } from 'vue-chartjs'
import type { Scenario } from '../types/simulation'

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Tooltip,
  Legend,
)

const props = defineProps<{
  scenarios: Scenario[]
}>()

const chartData = computed(() => {
  return {
    labels: props.scenarios.map(scenario => scenario.name),

    datasets: [
      {
        label: 'Budget',
        data: props.scenarios.map(scenario => scenario.budget),
        backgroundColor: '#6B7280',
      },
      {
        label: 'Median cost',
        data: props.scenarios.map(
          scenario => scenario.result.median_cost,
        ),
        backgroundColor: '#3B82F6',
      },
      {
        label: 'P90 cost',
        data: props.scenarios.map(
          scenario => scenario.result.p90,
        ),
        backgroundColor: '#F59E0B',
      },
    ],
  }
})

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,

  plugins: {
    legend: {
      position: 'top' as const,
    },

    tooltip: {
      callbacks: {
        label: (context: any) => {
          return ` £${Math.round(context.raw).toLocaleString('en-GB')}`
        },
      },
    },
  },

  scales: {
    y: {
      beginAtZero: true,

      ticks: {
        callback: (value: any) => {
          return `£${Math.round(value / 1000)}k`
        },
      },
    },
  },
}
</script>

<template>
  <div class="comparison-chart">
    <h3>Cost comparison</h3>

    <div class="chart-container">
      <Bar
        :data="chartData"
        :options="chartOptions"
      />
    </div>
  </div>
</template>

<style scoped>
.comparison-chart {
  margin-top: 32px;
  padding-top: 24px;
  border-top: 1px solid #eee;
}

.comparison-chart h3 {
  margin-bottom: 16px;
}

.chart-container {
  position: relative;
  height: 420px;
}
</style>