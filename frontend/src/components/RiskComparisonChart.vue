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
        label: 'Over-budget risk',
        data: props.scenarios.map(
          scenario =>
            scenario.result.over_budget_probability * 100,
        ),
        backgroundColor: '#EF4444',
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
          return ` ${Number(context.raw).toFixed(1)}%`
        },
      },
    },
  },

  scales: {
    y: {
      beginAtZero: true,
      max: 100,

      ticks: {
        callback: (value: any) => {
          return `${value}%`
        },
      },
    },
  },
}
</script>

<template>
  <div class="comparison-chart">
    <h3>Budget risk comparison</h3>

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