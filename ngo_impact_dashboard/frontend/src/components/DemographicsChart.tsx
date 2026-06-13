import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell,
} from 'recharts'
import type { Demographic } from '../types'

interface Props {
  data: Demographic[]
}

const COLORS = ['#2563eb', '#7c3aed', '#059669', '#d97706', '#dc2626', '#0891b2']

export function DemographicsChart({ data }: Props) {
  const byDistrict = data.reduce<Record<string, number>>((acc, d) => {
    acc[d.district] = (acc[d.district] || 0) + d.beneficiaries_reached
    return acc
  }, {})

  const districtData = Object.entries(byDistrict)
    .map(([district, count]) => ({ district, count }))
    .sort((a, b) => b.count - a.count)

  const genderData = data.reduce<Record<string, number>>((acc, d) => {
    acc[d.gender] = (acc[d.gender] || 0) + d.beneficiaries_reached
    return acc
  }, {})

  return (
    <div className="demographics-grid">
      <div className="chart-wrap">
        <h4>By district</h4>
        <ResponsiveContainer width="100%" height={240}>
          <BarChart data={districtData} layout="vertical" margin={{ left: 80, right: 16 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" horizontal={false} />
            <XAxis type="number" tick={{ fontSize: 11 }} />
            <YAxis type="category" dataKey="district" tick={{ fontSize: 11 }} width={75} />
            <Tooltip />
            <Bar dataKey="count" name="Beneficiaries" radius={[0, 4, 4, 0]}>
              {districtData.map((_, i) => (
                <Cell key={i} fill={COLORS[i % COLORS.length]} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="gender-breakdown">
        <h4>By gender</h4>
        <div className="gender-bars">
          {Object.entries(genderData).map(([gender, count], i) => {
            const total = Object.values(genderData).reduce((a, b) => a + b, 0)
            const pct = Math.round((count / total) * 100)
            return (
              <div key={gender} className="gender-row">
                <span className="gender-label">{gender}</span>
                <div className="gender-bar-track">
                  <div
                    className="gender-bar-fill"
                    style={{ width: `${pct}%`, background: COLORS[i % COLORS.length] }}
                  />
                </div>
                <span className="gender-pct">{count} ({pct}%)</span>
              </div>
            )
          })}
        </div>
      </div>
    </div>
  )
}
