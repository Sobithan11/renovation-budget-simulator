<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'

interface Project {
  id: number
  name: string
  budget: number
  extension_size: number
  kitchen_spec: string
  bathroom_spec: string
  flooring_area: number
  landscaping_area: number
}

const project = reactive({
  name: '',
  budget: 0,
  extension_size: 0,
  kitchen_spec: 'standard',
  bathroom_spec: 'standard',
  flooring_area: 0,
  electrical_work: false,
  plumbing_work: false,
  plastering_work: false,
  painting_work: false,
  windows_doors: 0,
  structural_work: false,
  roofing_work: false,
  landscaping_area: 0,
})

const projects = ref<Project[]>([])
const simulationResults = ref<Record<number, any>>({})
const simulationLoading = ref<number | null>(null)

const message = ref('')
const error = ref('')

async function createProject() {
  message.value = ''
  error.value = ''

  try {
    const response = await fetch('http://127.0.0.1:5000/projects', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(project),
    })

    const data = await response.json()

    if (!response.ok) {
      error.value = data.error || 'Failed to create project'
      return
    }

    message.value = `Project created successfully. ID: ${data.project_id}`

    await loadProjects()
  } catch (err) {
    error.value = 'Could not connect to the backend.'
  }
}

async function runProjectSimulation(projectId: number) {
  error.value = ''
  simulationLoading.value = projectId

  try {
    const response = await fetch(
      `http://127.0.0.1:5000/projects/${projectId}/simulate`,
      {
        method: 'POST',
      },
    )

    const data = await response.json()

    if (!response.ok) {
      error.value = data.error || 'Failed to run simulation'
      return
    }

    simulationResults.value[projectId] = data
  } catch (err) {
    error.value = 'Could not connect to the backend.'
  } finally {
    simulationLoading.value = null
  }
}

function getBudgetStatus(projectId: number) {
  const result = simulationResults.value[projectId]

  if (!result) {
    return ''
  }

  if (result.median_cost <= result.budget) {
    return 'Within budget'
  }

  return 'Over budget'
}

async function loadProjects() {
  try {
    const response = await fetch('http://127.0.0.1:5000/projects')

    if (!response.ok) {
      error.value = 'Failed to load projects'
      return
    }

    projects.value = await response.json()
  } catch (err) {
    error.value = 'Could not connect to the backend.'
  }
}

onMounted(() => {
  loadProjects()
})
</script>

<template>
  <main>
    <h1>Renovation Budget Simulator</h1>
    <p>Plan your renovation and understand your budget risk.</p>

    <form>
      <section>
        <h2>Project details</h2>

        <label>
          Project name
          <input
            v-model="project.name"
            type="text"
            placeholder="e.g. House Renovation"
          />
        </label>

        <label>
          Budget (£)
          <input
            v-model.number="project.budget"
            type="number"
            min="0"
          />
        </label>
      </section>

      <section>
        <h2>Renovation details</h2>

        <label>
          Extension size (m²)
          <input
            v-model.number="project.extension_size"
            type="number"
            min="0"
          />
        </label>

        <label>
          Kitchen specification
          <select v-model="project.kitchen_spec">
            <option value="none">None</option>
            <option value="budget">Budget</option>
            <option value="standard">Standard</option>
            <option value="high">High-end</option>
          </select>
        </label>

        <label>
          Bathroom specification
          <select v-model="project.bathroom_spec">
            <option value="none">None</option>
            <option value="budget">Budget</option>
            <option value="standard">Standard</option>
            <option value="high">High-end</option>
          </select>
        </label>

        <label>
          Flooring area (m²)
          <input
            v-model.number="project.flooring_area"
            type="number"
            min="0"
          />
        </label>

        <label>
          Landscaping area (m²)
          <input
            v-model.number="project.landscaping_area"
            type="number"
            min="0"
          />
        </label>
      </section>

      <section>
        <h2>Additional work</h2>

        <label>
          <input
            v-model="project.electrical_work"
            type="checkbox"
          />
          Electrical work
        </label>

        <label>
          <input
            v-model="project.plumbing_work"
            type="checkbox"
          />
          Plumbing work
        </label>

        <label>
          <input
            v-model="project.plastering_work"
            type="checkbox"
          />
          Plastering
        </label>

        <label>
          <input
            v-model="project.painting_work"
            type="checkbox"
          />
          Painting
        </label>

        <label>
          <input
            v-model="project.structural_work"
            type="checkbox"
          />
          Structural work
        </label>

        <label>
          <input
            v-model="project.roofing_work"
            type="checkbox"
          />
          Roofing work
        </label>

        <label>
          Number of windows/doors
          <input
            v-model.number="project.windows_doors"
            type="number"
            min="0"
          />
        </label>
      </section>

      <button
        type="button"
        @click="createProject"
      >
        Create Project
      </button>

      <p v-if="message">{{ message }}</p>
      <p v-if="error">{{ error }}</p>
    </form>

    <section>
      <h2>Saved Projects</h2>

      <p v-if="projects.length === 0">
        No projects saved yet.
      </p>

      <div
        v-for="savedProject in projects"
        :key="savedProject.id"
      >
        <h3>{{ savedProject.name }}</h3>

        <p>
          Budget: £{{ savedProject.budget.toLocaleString() }}
        </p>

        <p>
          Extension:
          {{ savedProject.extension_size }} m²
        </p>

        <p>
          Kitchen:
          {{ savedProject.kitchen_spec }}
        </p>

        <p>
          Bathroom:
          {{ savedProject.bathroom_spec }}
        </p>

        <button
          type="button"
          @click="runProjectSimulation(savedProject.id)"
        >
          {{
            simulationLoading === savedProject.id
              ? 'Running simulation...'
              : 'Run Simulation'
          }}
        </button>

        <div v-if="simulationResults[savedProject.id]">
          <h3>
            {{ getBudgetStatus(savedProject.id) }}
          </h3>

          <p>
            Budget:
            £{{ simulationResults[savedProject.id].budget.toLocaleString() }}
          </p>

          <h4>Simulation Results</h4>

          <p>
            Mean cost:
            £{{ simulationResults[savedProject.id].mean_cost.toLocaleString(undefined, {
              maximumFractionDigits: 0
            }) }}
          </p>

          <p>
            Median cost:
            £{{ simulationResults[savedProject.id].median_cost.toLocaleString(undefined, {
              maximumFractionDigits: 0
            }) }}
          </p>

          <p>
            P10:
            £{{ simulationResults[savedProject.id].p10.toLocaleString(undefined, {
              maximumFractionDigits: 0
            }) }}
          </p>

          <p>
            P90:
            £{{ simulationResults[savedProject.id].p90.toLocaleString(undefined, {
              maximumFractionDigits: 0
            }) }}
          </p>

          <p>
            Probability of exceeding budget:
            {{ (simulationResults[savedProject.id].over_budget_probability * 100).toFixed(1) }}%
          </p>

          <p>
            Probability of staying within budget:
            {{ (simulationResults[savedProject.id].under_budget_probability * 100).toFixed(1) }}%
          </p>
        </div>
      </div>
    </section>
  </main>
</template>

<style>
body {
  margin: 0;
  font-family: Arial, sans-serif;
  background: #f5f5f5;
}

main {
  max-width: 800px;
  margin: 0 auto;
  padding: 40px 20px;
}

h1 {
  margin-bottom: 8px;
}

section {
  background: white;
  padding: 24px;
  margin-top: 24px;
  border-radius: 8px;
}

label {
  display: block;
  margin-top: 16px;
  font-weight: 600;
}

input[type='text'],
input[type='number'],
select {
  display: block;
  width: 100%;
  box-sizing: border-box;
  margin-top: 6px;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

input[type='checkbox'] {
  margin-right: 8px;
}

button {
  margin-top: 24px;
  padding: 12px 20px;
  border: none;
  border-radius: 6px;
  background: #222;
  color: white;
  font-size: 16px;
  cursor: pointer;
}
</style>