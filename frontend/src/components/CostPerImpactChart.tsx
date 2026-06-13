import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend,
} from 'recharts'
import type { CostPerImpact } from '../types'

interface Props {
  data: CostPerImpact[]
}

export function CostPerImpactChart({ data }: Props) {
  const chartData = data.map((d) => ({
    name: d.program_name.replace(' ', '\n'),
    costPerBeneficiary: d.cost_per_beneficiary,
    costPerPoint: d.cost_per_learning_point,
    spend: d.total_spend,
  }))

  return (
    <div className="chart-wrap">
      <ResponsiveContainer width="100%" height={280}>
        <BarChart data={chartData} margin={{ top: 8, right: 8, left: 0, bottom: 40 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
          <XAxis dataKey="name" tick={{ fontSize: 11 }} interval={0} angle={-15} textAnchor="end" height={60} />
          <YAxis tick={{ fontSize: 11 }} tickFormatter={(v) => `₹${v}`} />
          <Tooltip
            formatter={(value: number, name: string) => [
              `₹${value.toLocaleString('en-IN')}`,
              name === 'costPerBeneficiary' ? 'Cost / beneficiary' : 'Cost / learning point',
            ]}
          />
          <Legend />
          <Bar dataKey="costPerBeneficiary" name="Cost per beneficiary" fill="#2563eb" radius={[4, 4, 0, 0]} />
          <Bar dataKey="costPerPoint" name="Cost per learning point" fill="#7c3aed" radius={[4, 4, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}
