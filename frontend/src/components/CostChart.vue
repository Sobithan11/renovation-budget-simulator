<script setup lang="ts">
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Tooltip,
  Legend,
} from 'chart.js'

import { Bar } from 'vue-chartjs'

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Tooltip,
  Legend,
)

interface DistributionPoint {
  cost: number
  count: number
}

const props = defineProps<{
  distribution: DistributionPoint[]
}>()

const chartData = {
  labels: props.distribution.map(point =>
    `£${Math.round(point.cost / 1000)}k`
  ),

  datasets: [
    {
      label: 'Simulated scenarios',
      data: props.distribution.map(point => point.count),
      backgroundColor: '#3B82F6',
    },
  ],
}

const chartOptions = {
  responsive: true,

  plugins: {
    legend: {
      display: false,
    },

    tooltip: {
      callbacks: {
        label: (context: any) => {
          return `${context.raw} simulated scenarios`
        },
      },
    },
  },

  scales: {
    x: {
      title: {
        display: true,
        text: 'Estimated renovation cost',
      },
    },

    y: {
      beginAtZero: true,

      title: {
        display: true,
        text: 'Number of scenarios',
      },
    },
  },
}
</script>

<template>
  <div class="chart-container">
    <Bar
      :data="chartData"
      :options="chartOptions"
    />
  </div>
</template>

<style scoped>
.chart-container {
  position: relative;
  width: 100%;
  height: 400px;
}
</style>