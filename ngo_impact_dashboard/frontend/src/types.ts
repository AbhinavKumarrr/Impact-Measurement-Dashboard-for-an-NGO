export interface Overview {
  ngo_name: string
  data_source: string

  beneficiaries_reached: number
  sessions_delivered: number
  attendance_rate: number
  learning_gain: number
  total_spend: number
  cost_per_beneficiary: number

  impact_efficiency_score?: number
  executive_score?: number
}

export interface KpiNode {
  level: 'activity' | 'output' | 'outcome' | 'impact'
  kpi_code: string
  kpi_name: string
  description?: string
  iris_indicator?: string
  parent_kpi_code?: string
  unit: string
  target_value: number | null
  actual_value: number | null
  progress_pct: number | null
}

export interface Demographic {
  district: string
  gender: string
  beneficiaries_reached: number
  avg_age: number
}

export interface ProgramProgress {
  program_name: string
  enrolled: number
  attended_sessions: number
  assessed_students: number
  attendance_rate: number
  avg_test_score_gain: number
  budget_allocated?: number
  total_spend?: number
}

export interface CostPerImpact {
  program_name: string
  total_spend: number
  beneficiaries: number
  cost_per_beneficiary: number
  cost_per_learning_point: number
}

export interface TrendPoint {
  month: string
  [key: string]: string | number
}

export interface DataQuality {
  total_submissions?: number
  total_records: number
  invalid_records: number
  duplicate_records: number
  data_quality_score: number
}

export interface DashboardData {
  overview: Overview
  kpi_tree: KpiNode[]
  demographics: Demographic[]
  program_progress: ProgramProgress[]
  cost_per_impact: CostPerImpact[]
  monthly_trends: TrendPoint[]
  learning_trends: TrendPoint[]
  spend_trends: TrendPoint[]
  data_quality: DataQuality
  data_source?: string
}
