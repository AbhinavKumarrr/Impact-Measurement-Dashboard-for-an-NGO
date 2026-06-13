import { useEffect, useState, useCallback } from 'react'
import type { DashboardData } from './types'
import { Header } from './components/Header'
import { KpiCards } from './components/KpiCards'
import { KpiTree } from './components/KpiTree'
import { ProgramProgress } from './components/ProgramProgress'
import { DemographicsChart } from './components/DemographicsChart'
import { CostPerImpactChart } from './components/CostPerImpactChart'
import { TrendsSection } from './components/TrendsSection'
import { DataQualityBanner } from './components/DataQualityBanner'
import { HelpPanel } from './components/HelpPanel'
import { ExecutiveScoreCard } from './components/ExecutiveScoreCard'

const API_BASE = import.meta.env.VITE_API_URL || ''

export default function App() {
  const [data, setData] = useState<DashboardData | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [lastUpdated, setLastUpdated] = useState<Date>(new Date())
  const [loadTimeMs, setLoadTimeMs] = useState<number | null>(null)

  const fetchData = useCallback(async () => {
    const t0 = performance.now()
    try {
      const res = await fetch(`${API_BASE}/api/dashboard`)
      if (!res.ok) throw new Error('Failed to load dashboard data')
      const json = await res.json()
      setData(json)
      setLastUpdated(new Date())
      setLoadTimeMs(Math.round(performance.now() - t0))
      setError(null)
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Unknown error')
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    fetchData()
    const interval = setInterval(fetchData, 30000)
    return () => clearInterval(interval)
  }, [fetchData])

  if (loading) {
    return (
      <div className="app loading-screen">
        <div className="loader" />
        <p>Loading impact data…</p>
      </div>
    )
  }

  if (error || !data) {
    return (
      <div className="app error-screen">
        <h2>Unable to load dashboard</h2>
        <p>{error}</p>
        <button onClick={fetchData}>Try again</button>
      </div>
    )
  }

  const executiveScore = data.overview.executive_score || 0

  return (
    <div className="app">
      <Header
        ngoName={data.overview.ngo_name}
        dataSource={data.data_source || data.overview.data_source}
        lastUpdated={lastUpdated}
        loadTimeMs={loadTimeMs}
        onRefresh={fetchData}
      />

      <HelpPanel />

      <ExecutiveScoreCard
        score={executiveScore}
        title="Executive Monday Score"
        subtitle="The one number the ED checks every Monday"
        target={1}
      />

      <DataQualityBanner quality={data.data_quality} />

      <section className="section">
        <h2>At a glance</h2>
        <KpiCards overview={data.overview} />
      </section>

      <section className="section">
        <h2>KPI ladder — Activity → Output → Outcome → Impact</h2>
        <p className="section-desc">
          Based on Logical Framework, Theory of Change, and IRIS+ indicators
        </p>
        <KpiTree nodes={data.kpi_tree} />
      </section>

      <div className="grid-2">
        <section className="section">
          <h2>Programme progress</h2>
          <ProgramProgress programs={data.program_progress} />
        </section>

        <section className="section">
          <h2>Cost per impact</h2>
          <CostPerImpactChart data={data.cost_per_impact} />
        </section>
      </div>

      <section className="section">
        <h2>Demographic reach</h2>
        <DemographicsChart data={data.demographics} />
      </section>

      <section className="section">
        <h2>Trends over time</h2>
        <TrendsSection
          attendance={data.monthly_trends}
          learning={data.learning_trends}
          spend={data.spend_trends}
        />
      </section>
    </div>
  )
}