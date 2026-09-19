<script setup lang="ts">
import { onMounted, ref, computed } from 'vue'
import SimulationResults from '../components/SimulationResults.vue'
import type {
  Project,
  SimulationResult,
} from '../types/simulation'
import { formatCurrency } from '../utils/formatters'

const projects = ref<Project[]>([])
const selectedProjectId = ref<number | null>(null)
const results = ref<SimulationResult | null>(null)

const loading = ref(true)
const simulating = ref(false)
const error = ref('')

const selectedProject = computed(() => {
  return projects.value.find(
    project => project.id === selectedProjectId.value,
  )
})

async function loadProjects() {
  loading.value = true
  error.value = ''

  try {
    const response = await fetch(
      'http://127.0.0.1:5000/projects',
    )

    if (!response.ok) {
      error.value = 'Failed to load projects.'
      return
    }

    projects.value = await response.json()

    if (projects.value.length > 0) {
      selectedProjectId.value = projects.value[0]?.id ?? null
    }
  } catch (err) {
    error.value = 'Could not connect to the backend.'
  } finally {
    loading.value = false
  }
}

async function runSimulation() {
  if (selectedProjectId.value === null) {
    return
  }

  simulating.value = true
  error.value = ''
  results.value = null

  try {
    const response = await fetch(
      `http://127.0.0.1:5000/projects/${selectedProjectId.value}/simulate`,
      {
        method: 'POST',
      },
    )

    const data = await response.json()

    if (!response.ok) {
      error.value = data.error || 'Failed to run simulation.'
      return
    }

    results.value = data
  } catch (err) {
    error.value = 'Could not connect to the backend.'
  } finally {
    simulating.value = false
  }
}

onMounted(() => {
  loadProjects()
})
</script>

<template>
  <main class="dashboard">
    <section class="dashboard-header">
      <div>
        <p class="eyebrow">Renovation analysis</p>

        <h1>Dashboard</h1>

        <p class="subtitle">
          View your renovation budget and simulation results.
        </p>
      </div>
    </section>

    <section class="project-selector">
      <label for="project">Select a project</label>

      <select
        id="project"
        v-model="selectedProjectId"
      >
        <option
          v-for="project in projects"
          :key="project.id"
          :value="project.id"
        >
          {{ project.name }}
        </option>
      </select>

      <button
        :disabled="selectedProjectId === null || simulating"
        @click="runSimulation"
      >
        {{
          simulating
            ? 'Running simulation...'
            : 'Run Simulation'
        }}
      </button>
    </section>

    <p
      v-if="loading"
      class="status"
    >
      Loading projects...
    </p>

    <p
      v-else-if="error"
      class="error"
    >
      {{ error }}
    </p>

    <p
      v-else-if="projects.length === 0"
      class="empty"
    >
      No renovation projects found. Create a project first.
    </p>

    <section
      v-if="selectedProject && !results && !simulating"
      class="project-summary"
    >
      <h2>{{ selectedProject.name }}</h2>

      <p>
        Budget:
        <strong>
          {{ formatCurrency(selectedProject.budget) }}
        </strong>
      </p>

      <p>
        Run a simulation to see the estimated renovation cost
        and financial risk.
      </p>
    </section>

    <section
      v-if="simulating"
      class="project-summary"
    >
      <h2>Running simulation</h2>

      <p>
        Generating thousands of possible renovation cost
        scenarios...
      </p>
    </section>

    <SimulationResults
      v-if="results"
      :results="results"
    />
  </main>
</template>

<style scoped>
.dashboard {
  max-width: 1100px;
  margin: 0 auto;
  padding: 40px;
}

.dashboard-header {
  margin-bottom: 32px;
}

.eyebrow {
  margin: 0 0 8px;
  font-size: 13px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #666;
}

h1 {
  margin: 0;
  font-size: 36px;
}

.subtitle {
  margin-top: 10px;
  color: #666;
  font-size: 16px;
}

.project-selector {
  display: flex;
  flex-direction: column;
  gap: 8px;
  max-width: 450px;
  margin-bottom: 32px;
}

.project-selector label {
  font-weight: 600;
}

.project-selector select {
  padding: 12px;
  border: 1px solid #ccc;
  border-radius: 8px;
  background: white;
  font-size: 15px;
}

.project-selector button {
  margin-top: 8px;
  padding: 12px 18px;
  border: none;
  border-radius: 8px;
  background: #222;
  color: white;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
}

.project-selector button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.project-summary {
  padding: 28px;
  border: 1px solid #ddd;
  border-radius: 12px;
  background: white;
  margin-bottom: 24px;
}

.project-summary h2 {
  margin-top: 0;
}

.status,
.empty {
  color: #666;
}

.error {
  color: #c0392b;
}

@media (max-width: 800px) {
  .dashboard {
    padding: 24px;
  }
}
</style>