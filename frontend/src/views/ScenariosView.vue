<script setup lang="ts">
import { onMounted, ref, computed } from 'vue'
import ScenarioCard from '../components/ScenarioCard.vue'
import ScenarioComparisonChart from '../components/ScenarioComparisonChart.vue'
import RiskComparisonChart from '../components/RiskComparisonChart.vue'
import SimulationResults from '../components/SimulationResults.vue'
import { API_BASE_URL } from '../config'
import type {
  Project,
  Scenario,
  SimulationResult,
} from '../types/simulation'
import { formatCurrency } from '../utils/formatters'

const projects = ref<Project[]>([])
const selectedProjectId = ref<number | null>(null)

const loading = ref(true)
const error = ref('')

const scenarioBudget = ref(0)
const scenarioExtensionSize = ref(0)
const scenarioKitchenSpec = ref('standard')
const scenarioBathroomSpec = ref('standard')
const scenarioFlooringArea = ref(0)
const scenarioPaintingArea = ref(0)
const scenarioLandscapingArea = ref(0)

const scenarioResult = ref<SimulationResult | null>(null)
const scenarios = ref<Scenario[]>([])

const simulating = ref(false)

let nextScenarioId = 1

const selectedProject = computed(() => {
  return projects.value.find(
    project => project.id === selectedProjectId.value,
  )
})

function loadScenarioFromProject() {
  if (!selectedProject.value) {
    return
  }

  scenarioBudget.value = selectedProject.value.budget

  scenarioExtensionSize.value =
    selectedProject.value.extension_size

  scenarioKitchenSpec.value =
    selectedProject.value.kitchen_spec

  scenarioBathroomSpec.value =
    selectedProject.value.bathroom_spec

  scenarioFlooringArea.value =
    selectedProject.value.flooring_area

  scenarioPaintingArea.value =
    selectedProject.value.painting_area

  scenarioLandscapingArea.value =
    selectedProject.value.landscaping_area

  scenarioResult.value = null
}

async function runScenario() {
  if (!selectedProject.value) {
    return
  }

  if (
    !Number.isFinite(scenarioBudget.value) ||
    scenarioBudget.value <= 0
  ) {
    error.value = 'Budget must be greater than £0.'
    return
  }

  if (
    !Number.isFinite(scenarioExtensionSize.value) ||
    scenarioExtensionSize.value < 0
  ) {
    error.value = 'Extension size cannot be negative.'
    return
  }

  if (
    !Number.isFinite(scenarioFlooringArea.value) ||
    scenarioFlooringArea.value < 0
  ) {
    error.value = 'Flooring area cannot be negative.'
    return
  }

  if (
    !Number.isFinite(scenarioPaintingArea.value) ||
    scenarioPaintingArea.value < 0
  ) {
    error.value = 'Painting area cannot be negative.'
    return
  }

  if (
    !Number.isFinite(scenarioLandscapingArea.value) ||
    scenarioLandscapingArea.value < 0
  ) {
    error.value = 'Landscaping area cannot be negative.'
    return
  }

  simulating.value = true
  error.value = ''
  scenarioResult.value = null

  const scenario = {
    name: `${selectedProject.value.name} - Scenario`,
    budget: scenarioBudget.value,
    extension_size: scenarioExtensionSize.value,
    kitchen_spec: scenarioKitchenSpec.value,
    bathroom_spec: scenarioBathroomSpec.value,
    flooring_area: scenarioFlooringArea.value,
    painting_area: scenarioPaintingArea.value,
    landscaping_area: scenarioLandscapingArea.value,

    electrical_work:
      selectedProject.value.electrical_work,

    plumbing_work:
      selectedProject.value.plumbing_work,

    plastering_work:
      selectedProject.value.plastering_work,

    windows_doors:
      selectedProject.value.windows_doors,

    structural_work:
      selectedProject.value.structural_work,

    roofing_work:
      selectedProject.value.roofing_work,
  }

  try {
    const response = await fetch(
      `${API_BASE_URL}/simulate`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(scenario),
      },
    )

    const data = await response.json()

    if (!response.ok) {
      error.value =
        data.error || 'Failed to run scenario.'
      return
    }

    scenarioResult.value = data

    const scenarioId = nextScenarioId++

    scenarios.value.push({
      id: scenarioId,
      name: `${selectedProject.value.name} - Scenario ${scenarioId}`,
      budget: scenarioBudget.value,
      extension_size: scenarioExtensionSize.value,
      kitchen_spec: scenarioKitchenSpec.value,
      bathroom_spec: scenarioBathroomSpec.value,
      flooring_area: scenarioFlooringArea.value,
      painting_area: scenarioPaintingArea.value,
      landscaping_area: scenarioLandscapingArea.value,
      result: data,
    })
  } catch (err) {
    error.value = 'Could not connect to the backend.'
  } finally {
    simulating.value = false
  }
}

function removeScenario(scenarioId: number) {
  scenarios.value = scenarios.value.filter(
    scenario => scenario.id !== scenarioId,
  )
}

async function loadProjects() {
  loading.value = true
  error.value = ''

  try {
    const response = await fetch(
      `${API_BASE_URL}/projects`,
    )

    if (!response.ok) {
      error.value = 'Failed to load projects.'
      return
    }

    projects.value = await response.json()

    if (projects.value.length > 0) {
      selectedProjectId.value =
        projects.value[0]?.id ?? null

      loadScenarioFromProject()
    }
  } catch (err) {
    error.value = 'Could not connect to the backend.'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadProjects()
})
</script>

<template>
  <main class="scenarios">
    <section class="page-header">
      <p class="eyebrow">What-if analysis</p>

      <h1>Scenarios</h1>

      <p class="subtitle">
        Explore how changes to your renovation plans could
        affect cost and budget risk.
      </p>
    </section>

    <section class="project-selector">
      <label for="project">Select a project</label>

      <select
        id="project"
        v-model="selectedProjectId"
        @change="loadScenarioFromProject"
      >
        <option
          v-for="project in projects"
          :key="project.id"
          :value="project.id"
        >
          {{ project.name }}
        </option>
      </select>
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
      v-else-if="selectedProject"
      class="scenario-builder"
    >
      <div class="section-heading">
        <div>
          <p class="eyebrow">Current project</p>

          <h2>{{ selectedProject.name }}</h2>
        </div>

        <div class="budget">
          <span>Budget</span>

          <strong>
            {{ formatCurrency(selectedProject.budget) }}
          </strong>
        </div>
      </div>

      <div class="settings-grid">
        <div class="setting">
          <span>Extension size</span>
          <strong>
            {{ selectedProject.extension_size }} m²
          </strong>
        </div>

        <div class="setting">
          <span>Kitchen</span>
          <strong>
            {{ selectedProject.kitchen_spec }}
          </strong>
        </div>

        <div class="setting">
          <span>Bathroom</span>
          <strong>
            {{ selectedProject.bathroom_spec }}
          </strong>
        </div>

        <div class="setting">
          <span>Flooring</span>
          <strong>
            {{ selectedProject.flooring_area }} m²
          </strong>
        </div>

        <div class="setting">
          <span>Painting</span>
          <strong>
            {{ selectedProject.painting_area }} m²
          </strong>
        </div>

        <div class="setting">
          <span>Landscaping</span>
          <strong>
            {{ selectedProject.landscaping_area }} m²
          </strong>
        </div>
      </div>

      <div class="scenario-form">
        <h3>Build a scenario</h3>

        <p class="form-description">
          Adjust the project assumptions below to explore a
          different renovation scenario.
        </p>

        <div class="form-grid">
          <div class="form-group">
            <label for="scenario-budget">
              Budget (£)
            </label>

            <input
              id="scenario-budget"
              v-model.number="scenarioBudget"
              type="number"
              min="1"
              step="1"
            />
          </div>

          <div class="form-group">
            <label for="scenario-extension">
              Extension size (m²)
            </label>

            <input
              id="scenario-extension"
              v-model.number="scenarioExtensionSize"
              type="number"
              min="0"
              step="0.1"
            />
          </div>

          <div class="form-group">
            <label for="scenario-kitchen">
              Kitchen
            </label>

            <select
              id="scenario-kitchen"
              v-model="scenarioKitchenSpec"
            >
              <option value="none">None</option>
              <option value="budget">Budget</option>
              <option value="standard">Standard</option>
              <option value="high">High-end</option>
            </select>
          </div>

          <div class="form-group">
            <label for="scenario-bathroom">
              Bathroom
            </label>

            <select
              id="scenario-bathroom"
              v-model="scenarioBathroomSpec"
            >
              <option value="none">None</option>
              <option value="budget">Budget</option>
              <option value="standard">Standard</option>
              <option value="high">High-end</option>
            </select>
          </div>

          <div class="form-group">
            <label for="scenario-flooring">
              Flooring area (m²)
            </label>

            <input
              id="scenario-flooring"
              v-model.number="scenarioFlooringArea"
              type="number"
              min="0"
              step="0.1"
            />
          </div>

          <div class="form-group">
            <label for="scenario-painting">
              Painting area (m²)
            </label>

            <input
              id="scenario-painting"
              v-model.number="scenarioPaintingArea"
              type="number"
              min="0"
              step="0.1"
            />
          </div>

          <div class="form-group">
            <label for="scenario-landscaping">
              Landscaping area (m²)
            </label>

            <input
              id="scenario-landscaping"
              v-model.number="scenarioLandscapingArea"
              type="number"
              min="0"
              step="0.1"
            />
          </div>
        </div>

        <button
          class="simulate-button"
          :disabled="simulating"
          @click="runScenario"
        >
          {{
            simulating
              ? 'Running simulation...'
              : 'Run Scenario'
          }}
        </button>

        <SimulationResults
          v-if="scenarioResult"
          :results="{
            ...scenarioResult,
            budget: scenarioBudget,
          }"
          :show-header="false"
          :show-charts="false"
          compact
        />

        <div
          v-if="scenarios.length > 0"
          class="saved-scenarios"
        >
          <h3>Scenario comparison</h3>

          <div class="scenario-list">
            <ScenarioCard
              v-for="scenario in scenarios"
              :key="scenario.id"
              :scenario="scenario"
              @remove="removeScenario"
            />
          </div>

          <ScenarioComparisonChart
            :scenarios="scenarios"
          />

          <RiskComparisonChart
            :scenarios="scenarios"
          />
        </div>
      </div>
    </section>
  </main>
</template>

<style scoped>
.scenarios {
  max-width: 1100px;
  margin: 0 auto;
  padding: 40px;
}

.page-header {
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
  max-width: 650px;
  margin-top: 10px;
  color: #666;
  line-height: 1.5;
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

.status,
.empty {
  color: #666;
}

.error {
  color: #c0392b;
}

.scenario-builder {
  padding: 28px;
  border: 1px solid #ddd;
  border-radius: 12px;
  background: white;
}

.section-heading {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 24px;
}

.section-heading h2 {
  margin: 0;
}

.budget {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 4px;
}

.budget span {
  color: #666;
  font-size: 14px;
}

.budget strong {
  font-size: 20px;
}

.settings-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
}

.setting {
  padding: 18px;
  border: 1px solid #eee;
  border-radius: 8px;
  background: #fafafa;
}

.setting span {
  display: block;
  margin-bottom: 6px;
  color: #666;
  font-size: 13px;
}

.setting strong {
  text-transform: capitalize;
}

.scenario-form {
  margin-top: 28px;
  padding-top: 24px;
  border-top: 1px solid #eee;
}

.scenario-form h3 {
  margin-top: 0;
  margin-bottom: 8px;
}

.form-description {
  margin-bottom: 24px;
  color: #666;
  line-height: 1.5;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 18px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 7px;
}

.form-group label {
  font-weight: 600;
  font-size: 14px;
}

.form-group input,
.form-group select {
  box-sizing: border-box;
  width: 100%;
  padding: 11px;
  border: 1px solid #ccc;
  border-radius: 7px;
  background: white;
  font-size: 15px;
}

.simulate-button {
  margin-top: 24px;
  padding: 12px 20px;
  border: none;
  border-radius: 7px;
  background: #222;
  color: white;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
}

.simulate-button:hover {
  opacity: 0.85;
}

.simulate-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.saved-scenarios {
  margin-top: 32px;
}

.saved-scenarios h3 {
  margin-bottom: 16px;
}

.scenario-list {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

@media (max-width: 700px) {
  .scenarios {
    padding: 24px;
  }

  .form-grid {
    grid-template-columns: 1fr;
  }

  .settings-grid {
    grid-template-columns: 1fr 1fr;
  }

  .section-heading {
    flex-direction: column;
    gap: 16px;
  }

  .budget {
    align-items: flex-start;
  }
}

@media (max-width: 500px) {
  .settings-grid {
    grid-template-columns: 1fr;
  }
}
</style>