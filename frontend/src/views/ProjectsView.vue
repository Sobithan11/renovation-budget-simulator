```vue
<script setup lang="ts">
import { API_BASE_URL } from '../config'
import { nextTick, onMounted, reactive, ref } from 'vue'
import ProjectCard from '../components/ProjectCard.vue'
import type {
  Project,
  ProjectFormData,
  SimulationResult,
} from '../types/simulation'

const project = reactive<ProjectFormData>({
  name: '',
  budget: 0,
  extension_size: 0,
  kitchen_spec: 'standard',
  bathroom_spec: 'standard',
  flooring_area: 0,
  electrical_work: false,
  plumbing_work: false,
  plastering_work: false,
  painting_area: 0,
  windows_doors: 0,
  structural_work: false,
  roofing_work: false,
  landscaping_area: 0,
})

const projects = ref<Project[]>([])
const simulationResults = ref<
  Record<number, SimulationResult>
>({})
const simulationLoading = ref<number | null>(null)

const message = ref('')
const error = ref('')

const fieldErrors = reactive({
  name: '',
  budget: '',
  extension_size: '',
  flooring_area: '',
  painting_area: '',
  landscaping_area: '',
  windows_doors: '',
})

const formRef = ref<HTMLFormElement | null>(null)

async function scrollToFirstError() {
  await nextTick()

  const firstError = formRef.value?.querySelector(
    '.field-error'
  )

  if (firstError) {
    firstError.scrollIntoView({
      behavior: 'smooth',
      block: 'center',
    })
  }
}

function preventNumberInputScroll(event: WheelEvent) {
  const target = event.target as HTMLInputElement

  target.blur()
}

function validateProject() {
  fieldErrors.name = ''
  fieldErrors.budget = ''
  fieldErrors.extension_size = ''
  fieldErrors.flooring_area = ''
  fieldErrors.painting_area = ''
  fieldErrors.landscaping_area = ''
  fieldErrors.windows_doors = ''

  let valid = true

  if (!project.name.trim()) {
    fieldErrors.name = 'Project name is required.'
    valid = false
  }

  if (!Number.isFinite(project.budget) || project.budget <= 0) {
    fieldErrors.budget =
      'Budget is required and must be greater than £0.'
    valid = false
  }

  if (
    !Number.isFinite(project.extension_size) ||
    project.extension_size < 0
  ) {
    fieldErrors.extension_size =
      'Extension size is required and must be 0 or greater.'
    valid = false
  }

  if (
    !Number.isFinite(project.flooring_area) ||
    project.flooring_area < 0
  ) {
    fieldErrors.flooring_area =
      'Flooring area is required and must be 0 or greater.'
    valid = false
  }

  if (
    !Number.isFinite(project.painting_area) ||
    project.painting_area < 0
  ) {
    fieldErrors.painting_area =
      'Painting area is required and must be 0 or greater.'
    valid = false
  }

  if (
    !Number.isFinite(project.landscaping_area) ||
    project.landscaping_area < 0
  ) {
    fieldErrors.landscaping_area =
      'Landscaping area is required and must be 0 or greater.'
    valid = false
  }

  if (
    !Number.isInteger(project.windows_doors) ||
    project.windows_doors < 0
  ) {
    fieldErrors.windows_doors =
      'Number of windows/doors is required and must be a whole number of 0 or greater.'
    valid = false
  }

  return valid
}

async function createProject() {
  message.value = ''
  error.value = ''

  if (!validateProject()) {
    await scrollToFirstError()
    return
  }

  try {
    const response = await fetch(
      `${API_BASE_URL}/projects`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(project),
      },
    )

    const data = await response.json()

    if (!response.ok) {
      error.value =
        data.error || 'Failed to create project.'
      return
    }

    message.value = 'Project created successfully.'

    project.name = ''
    project.budget = 0
    project.extension_size = 0
    project.kitchen_spec = 'standard'
    project.bathroom_spec = 'standard'
    project.flooring_area = 0
    project.electrical_work = false
    project.plumbing_work = false
    project.plastering_work = false
    project.painting_area = 0
    project.windows_doors = 0
    project.structural_work = false
    project.roofing_work = false
    project.landscaping_area = 0

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
      `${API_BASE_URL}/projects/${projectId}/simulate`,
      {
        method: 'POST',
      },
    )

    const data = await response.json()

    if (!response.ok) {
      error.value =
        data.error || 'Failed to run simulation.'
      return
    }

    simulationResults.value[projectId] = data
  } catch (err) {
    error.value = 'Could not connect to the backend.'
  } finally {
    simulationLoading.value = null
  }
}

async function deleteProject(projectId: number) {
  error.value = ''
  message.value = ''

  try {
    const response = await fetch(
      `${API_BASE_URL}/projects/${projectId}`,
      {
        method: 'DELETE',
      },
    )

    const data = await response.json()

    if (!response.ok) {
      error.value =
        data.error || 'Failed to delete project.'
      return
    }

    delete simulationResults.value[projectId]

    message.value = 'Project deleted successfully.'

    await loadProjects()
  } catch (err) {
    error.value = 'Could not connect to the backend.'
  }
}

async function loadProjects() {
  try {
    const response = await fetch(
      `${API_BASE_URL}/projects`,
    )

    if (!response.ok) {
      error.value = 'Failed to load projects.'
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
  <main class="projects">
    <section class="page-header">
      <p class="eyebrow">Project management</p>

      <h1>Projects</h1>

      <p class="subtitle">
        Create and manage renovation projects and run
        budget simulations.
      </p>
    </section>

    <form
      ref="formRef"
      class="project-form"
      @submit.prevent="createProject"
    >
      <section>
        <h2>Project details</h2>

        <label>
          Project name

          <input
            v-model="project.name"
            type="text"
            placeholder="e.g. House Renovation"
          />

          <span
            v-if="fieldErrors.name"
            class="field-error"
          >
            {{ fieldErrors.name }}
          </span>
        </label>

        <label>
          Budget (£)

          <input
            v-model.number="project.budget"
            type="number"
            min="1"
            step="1"
            @wheel="preventNumberInputScroll"
          />

          <span
            v-if="fieldErrors.budget"
            class="field-error"
          >
            {{ fieldErrors.budget }}
          </span>
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
            step="0.1"
            @wheel="preventNumberInputScroll"
          />

          <span
            v-if="fieldErrors.extension_size"
            class="field-error"
          >
            {{ fieldErrors.extension_size }}
          </span>
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
            step="0.1"
            @wheel="preventNumberInputScroll"
          />

          <span
            v-if="fieldErrors.flooring_area"
            class="field-error"
          >
            {{ fieldErrors.flooring_area }}
          </span>
        </label>

        <label>
          Painting area (m²)

          <input
            v-model.number="project.painting_area"
            type="number"
            min="0"
            step="0.1"
            @wheel="preventNumberInputScroll"
          />

          <span
            v-if="fieldErrors.painting_area"
            class="field-error"
          >
            {{ fieldErrors.painting_area }}
          </span>
        </label>

        <label>
          Landscaping area (m²)

          <input
            v-model.number="project.landscaping_area"
            type="number"
            min="0"
            step="0.1"
            @wheel="preventNumberInputScroll"
          />

          <span
            v-if="fieldErrors.landscaping_area"
            class="field-error"
          >
            {{ fieldErrors.landscaping_area }}
          </span>
        </label>
      </section>

      <section>
        <h2>Additional work</h2>

        <label class="checkbox-label">
          <input
            v-model="project.electrical_work"
            type="checkbox"
          />
          Electrical work
        </label>

        <label class="checkbox-label">
          <input
            v-model="project.plumbing_work"
            type="checkbox"
          />
          Plumbing work
        </label>

        <label class="checkbox-label">
          <input
            v-model="project.plastering_work"
            type="checkbox"
          />
          Plastering
        </label>

        <label class="checkbox-label">
          <input
            v-model="project.structural_work"
            type="checkbox"
          />
          Structural work
        </label>

        <label class="checkbox-label">
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
            step="1"
            @wheel="preventNumberInputScroll"
          />

          <span
            v-if="fieldErrors.windows_doors"
            class="field-error"
          >
            {{ fieldErrors.windows_doors }}
          </span>
        </label>
      </section>

      <button
        class="create-button"
        type="submit"
      >
        Create Project
      </button>

      <p
        v-if="message"
        class="success"
      >
        {{ message }}
      </p>

      <p
        v-if="error"
        class="error"
      >
        {{ error }}
      </p>
    </form>

    <section class="saved-projects">
      <div class="section-header">
        <div>
          <p class="eyebrow">Saved projects</p>
          <h2>Your renovation projects</h2>
        </div>
      </div>

      <p
        v-if="projects.length === 0"
        class="empty"
      >
        No projects saved yet.
      </p>

      <ProjectCard
        v-for="savedProject in projects"
        :key="savedProject.id"
        :project="savedProject"
        :simulation-result="simulationResults[savedProject.id]"
        :simulation-loading="
          simulationLoading === savedProject.id
        "
        @simulate="runProjectSimulation"
        @delete="deleteProject"
      />
    </section>
  </main>
</template>

<style scoped>
.projects {
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
  margin-top: 10px;
  color: #666;
  line-height: 1.5;
}

.project-form {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.project-form section {
  padding: 28px;
  border: 1px solid #ddd;
  border-radius: 12px;
  background: white;
}

.project-form h2 {
  margin-top: 0;
}

.project-form label {
  display: block;
  margin-top: 18px;
  font-weight: 600;
}

.project-form input[type='text'],
.project-form input[type='number'],
.project-form select {
  display: block;
  width: 100%;
  box-sizing: border-box;
  margin-top: 7px;
  padding: 11px;
  border: 1px solid #ccc;
  border-radius: 7px;
  background: white;
  font-size: 15px;
}

.checkbox-label {
  font-weight: 500 !important;
}

.checkbox-label input {
  margin-right: 8px;
}

.field-error {
  display: block;
  margin-top: 5px;
  color: #c0392b;
  font-size: 13px;
  font-weight: 400;
}

.create-button {
  align-self: flex-start;
  padding: 12px 20px;
  border: none;
  border-radius: 8px;
  background: #222;
  color: white;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
}

.success {
  margin: 0;
  color: #0f5132;
}

.error {
  margin: 0;
  color: #c0392b;
}

.saved-projects {
  margin-top: 40px;
}

.section-header {
  margin-bottom: 16px;
}

.section-header h2 {
  margin: 0;
}

.empty {
  color: #666;
}

@media (max-width: 800px) {
  .projects {
    padding: 24px;
  }
}
</style>