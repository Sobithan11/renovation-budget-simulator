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

interface BreakdownItem {
  category: string
  average_cost: number
}

const props = defineProps<{
  breakdown: BreakdownItem[]
}>()

const categoryLabels: Record<string, string> = {
  extension: 'Extension',
  kitchen: 'Kitchen',
  bathroom: 'Bathroom',
  flooring: 'Flooring',
  landscaping: 'Landscaping',
  electrical: 'Electrical',
  plumbing: 'Plumbing',
  plastering: 'Plastering',
  painting: 'Painting',
  windows_doors: 'Windows & doors',
}

const chartData = {
  labels: props.breakdown.map(
    item => categoryLabels[item.category] || item.category
  ),

  datasets: [
    {
    label: 'Average cost',
    data: props.breakdown.map(item => item.average_cost),
    backgroundColor: [
    '#3B82F6',
    '#10B981',
    '#F59E0B',
    '#8B5CF6',
    '#EC4899',
    '#06B6D4',
    '#F97316',
    '#14B8A6',
    '#6366F1',
    '#84CC16',
    ],
  },
],
}

const chartOptions = {
  indexAxis: 'y' as const,

  responsive: true,

  plugins: {
    legend: {
      display: false,
    },

    tooltip: {
      callbacks: {
        label: (context: any) => {
          return `£${Math.round(context.raw).toLocaleString('en-GB')}`
        },
      },
    },
  },

  scales: {
    x: {
      beginAtZero: true,

      title: {
        display: true,
        text: 'Average cost',
      },

      ticks: {
        callback: (value: string | number) => {
          return `£${Number(value) / 1000}k`
        },
      },
    },

    y: {
      title: {
        display: true,
        text: 'Category',
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
  height: 420px;
}
</style>