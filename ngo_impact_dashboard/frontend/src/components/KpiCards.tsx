import type { Overview } from '../types'

interface Props {
  overview: Overview
}

function formatCurrency(n: number) {
  if (n >= 100000) return `₹${(n / 100000).toFixed(1)}L`
  if (n >= 1000) return `₹${(n / 1000).toFixed(0)}K`
  return `₹${n.toFixed(0)}`
}

const cards = (o: Overview) => [
  { label: 'Beneficiaries reached', value: o.total_beneficiaries.toLocaleString(), icon: '👥', color: '#2563eb' },
  { label: 'Sessions delivered', value: o.total_sessions.toLocaleString(), icon: '📚', color: '#7c3aed' },
  { label: 'Attendance rate', value: `${o.attendance_rate}%`, icon: '✓', color: '#059669' },
  { label: 'Learning gain', value: `+${o.avg_learning_gain} pts`, icon: '📈', color: '#d97706' },
  { label: 'Total spend', value: formatCurrency(o.total_spend), icon: '💰', color: '#dc2626' },
  { label: 'Cost per beneficiary', value: formatCurrency(o.cost_per_beneficiary), icon: '🎯', color: '#0891b2' },
]

export function KpiCards({ overview }: Props) {
  return (
    <div className="kpi-cards">
      {cards(overview).map((c) => (
        <div key={c.label} className="kpi-card" style={{ '--accent': c.color } as React.CSSProperties}>
          <span className="kpi-icon">{c.icon}</span>
          <div>
            <p className="kpi-label">{c.label}</p>
            <p className="kpi-value">{c.value}</p>
          </div>
        </div>
      ))}
    </div>
  )
}
