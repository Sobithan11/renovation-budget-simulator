<script setup lang="ts">
import MetricCard from './MetricCard.vue'
import type {
  Project,
  SimulationResult,
} from '../types/simulation'
import { formatCurrency } from '../utils/formatters'

defineProps<{
  project: Project
  simulationResult?: SimulationResult
  simulationLoading?: boolean
}>()

const emit = defineEmits<{
  simulate: [projectId: number]
  delete: [projectId: number]
}>()
</script>

<template>
  <article class="project-card">
    <div class="project-header">
      <div>
        <h3>{{ project.name }}</h3>
        <p>
          Budget:
          <strong>{{ formatCurrency(project.budget) }}</strong>
        </p>
      </div>

      <button
        class="delete-button"
        type="button"
        @click="emit('delete', project.id)"
      >
        Delete
      </button>
    </div>

    <div class="project-details">
      <div>
        <span>Extension</span>
        <strong>{{ project.extension_size }} m²</strong>
      </div>

      <div>
        <span>Kitchen</span>
        <strong>{{ project.kitchen_spec }}</strong>
      </div>

      <div>
        <span>Bathroom</span>
        <strong>{{ project.bathroom_spec }}</strong>
      </div>

      <div>
        <span>Flooring</span>
        <strong>{{ project.flooring_area }} m²</strong>
      </div>

      <div>
        <span>Landscaping</span>
        <strong>{{ project.landscaping_area }} m²</strong>
      </div>
    </div>

    <button
      class="simulate-button"
      type="button"
      :disabled="simulationLoading"
      @click="emit('simulate', project.id)"
    >
      {{
        simulationLoading
          ? 'Running simulation...'
          : 'Run Simulation'
      }}
    </button>

    <div
      v-if="simulationResult"
      class="simulation-section"
    >
      <div class="simulation-heading">
        <h4>Simulation results</h4>

        <div
          class="budget-status"
          :class="{
            'over-budget':
              simulationResult.median_cost > simulationResult.budget,
            'within-budget':
              simulationResult.median_cost <= simulationResult.budget,
          }"
        >
          {{
            simulationResult.median_cost > simulationResult.budget
              ? 'Over budget'
              : 'Within budget'
          }}
        </div>
      </div>

      <div class="results-grid">
        <MetricCard
          title="Expected cost"
          :value="formatCurrency(simulationResult.mean_cost)"
          compact
        />

        <MetricCard
          title="Median cost"
          :value="formatCurrency(simulationResult.median_cost)"
          compact
        />

        <MetricCard
          title="P10"
          :value="formatCurrency(simulationResult.p10)"
          compact
        />

        <MetricCard
          title="P90"
          :value="formatCurrency(simulationResult.p90)"
          compact
        />

        <MetricCard
          title="Over-budget risk"
          :value="`${(simulationResult.over_budget_probability * 100).toFixed(1)}%`"
          compact
        />

        <MetricCard
          title="Within-budget probability"
          :value="`${(simulationResult.under_budget_probability * 100).toFixed(1)}%`"
          compact
        />
      </div>
    </div>
  </article>
</template>

<style scoped>
.project-card {
  margin-top: 16px;
  padding: 24px;
  border: 1px solid #ddd;
  border-radius: 12px;
  background: white;
}

.project-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.project-header h3 {
  margin: 0 0 8px;
}

.project-header p {
  margin: 0;
  color: #666;
}

.project-details {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  margin-top: 20px;
}

.project-details div {
  padding: 14px;
  border-radius: 8px;
  background: #fafafa;
}

.project-details span {
  display: block;
  margin-bottom: 5px;
  color: #666;
  font-size: 13px;
}

.project-details strong {
  text-transform: capitalize;
}

.simulate-button {
  margin-top: 20px;
  padding: 12px 20px;
  border: none;
  border-radius: 7px;
  background: #222;
  color: white;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
}

.simulate-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.delete-button {
  padding: 7px 12px;
  border: 1px solid #ccc;
  border-radius: 6px;
  background: white;
  color: #222;
  cursor: pointer;
}

.delete-button:hover {
  background: #f5f5f5;
}

.simulation-section {
  margin-top: 28px;
  padding-top: 24px;
  border-top: 1px solid #eee;
}

.simulation-heading {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.simulation-heading h4 {
  margin: 0;
  font-size: 18px;
}

.budget-status {
  padding: 7px 12px;
  border-radius: 20px;
  font-size: 13px;
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
  gap: 12px;
}

@media (max-width: 800px) {
  .project-details,
  .results-grid {
    grid-template-columns: 1fr 1fr;
  }
}

@media (max-width: 550px) {
  .project-header,
  .simulation-heading {
    flex-direction: column;
    gap: 12px;
  }

  .project-details,
  .results-grid {
    grid-template-columns: 1fr;
  }
}
</style>