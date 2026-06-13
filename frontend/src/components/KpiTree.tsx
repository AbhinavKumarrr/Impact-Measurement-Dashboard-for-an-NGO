import type { KpiNode } from '../types'

interface Props {
  nodes: KpiNode[]
}

const LEVELS = ['activity', 'output', 'outcome', 'impact'] as const
const LEVEL_LABELS: Record<string, string> = {
  activity: 'Activity',
  output: 'Output',
  outcome: 'Outcome',
  impact: 'Impact',
}
const LEVEL_COLORS: Record<string, string> = {
  activity: '#6366f1',
  output: '#8b5cf6',
  outcome: '#a855f7',
  impact: '#c026d3',
}

function formatValue(value: number | null, unit: string) {
  if (value === null) return '—'
  if (unit === 'INR' || unit.startsWith('INR/')) {
    return `₹${Number(value).toLocaleString('en-IN', { maximumFractionDigits: 2 })}`
  }
  if (unit === '%') return `${value}%`
  return `${Number(value).toLocaleString('en-IN', { maximumFractionDigits: 2 })} ${unit}`
}

export function KpiTree({ nodes }: Props) {
  return (
    <div className="kpi-tree">
      {LEVELS.map((level) => {
        const levelNodes = nodes.filter((n) => n.level === level)
        if (!levelNodes.length) return null
        return (
          <div key={level} className="kpi-level" style={{ '--level-color': LEVEL_COLORS[level] } as React.CSSProperties}>
            <div className="level-header">
              <span className="level-dot" />
              <h3>{LEVEL_LABELS[level]}</h3>
            </div>
            <div className="level-cards">
              {levelNodes.map((node) => (
                <div key={node.kpi_code} className="tree-card">
                  <div className="tree-card-top">
                    <span className="tree-name">{node.kpi_name}</span>
                    {node.iris_indicator && (
                      <span className="iris-tag" title="IRIS+ indicator">IRIS {node.iris_indicator}</span>
                    )}
                  </div>
                  <div className="tree-values">
                    <span className="actual">{formatValue(node.actual_value, node.unit)}</span>
                    {node.target_value != null && (
                      <span className="target">Target: {formatValue(node.target_value, node.unit)}</span>
                    )}
                  </div>
                  {node.progress_pct != null && (
                    <div className="progress-bar">
                      <div
                        className="progress-fill"
                        style={{ width: `${Math.min(node.progress_pct, 100)}%` }}
                      />
                      <span className="progress-label">{node.progress_pct}% of target</span>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        )
      })}
    </div>
  )
}
