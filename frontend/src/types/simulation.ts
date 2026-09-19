export interface Project {
  id: number
  name: string
  budget: number
  extension_size: number
  kitchen_spec: string
  bathroom_spec: string
  flooring_area: number
  landscaping_area: number
  electrical_work: boolean
  plumbing_work: boolean
  plastering_work: boolean
  painting_area: number
  windows_doors: number
  structural_work: boolean
  roofing_work: boolean
}

export interface ProjectFormData {
  name: string
  budget: number
  extension_size: number
  kitchen_spec: string
  bathroom_spec: string
  flooring_area: number
  electrical_work: boolean
  plumbing_work: boolean
  plastering_work: boolean
  painting_area: number
  windows_doors: number
  structural_work: boolean
  roofing_work: boolean
  landscaping_area: number
}

export interface DistributionPoint {
  cost: number
  count: number
}

export interface BreakdownItem {
  category: string
  average_cost: number
}

export interface SimulationResult {
  project_id?: number
  project_name?: string
  budget: number
  mean_cost: number
  median_cost: number
  p10: number
  p90: number
  over_budget_probability: number
  under_budget_probability: number
  distribution?: DistributionPoint[]
  cost_breakdown?: BreakdownItem[]
}

export interface Scenario {
  id: number
  name: string
  budget: number
  extension_size: number
  kitchen_spec: string
  bathroom_spec: string
  flooring_area: number
  painting_area: number
  landscaping_area: number
  result: SimulationResult
}