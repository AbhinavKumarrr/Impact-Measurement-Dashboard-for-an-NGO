import { useState } from 'react'
import {
  LineChart, Line, AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend,
} from 'recharts'
import type { TrendPoint } from '../types'

interface Props {
  attendance: TrendPoint[]
  learning: TrendPoint[]
  spend: TrendPoint[]
}

type Tab = 'attendance' | 'learning' | 'spend'

export function TrendsSection({ attendance, learning, spend }: Props) {
  const [tab, setTab] = useState<Tab>('attendance')

  const formatMonth = (m: string) => {
    const d = new Date(m)
    return d.toLocaleDateString('en-IN', { month: 'short', year: '2-digit' })
  }

  const attData = attendance.map((r) => ({
    month: formatMonth(String(r.month)),
    rate: Number(r.attendance_rate),
    sessions: Number(r.sessions_held),
  }))

  const learnData = learning.map((r) => ({
    month: formatMonth(String(r.month)),
    pre: Number(r.avg_pre_score),
    post: Number(r.avg_post_score),
    gain: Number(r.avg_gain),
  }))

  const spendData = spend.map((r) => ({
    month: formatMonth(String(r.month)),
    spend: Number(r.total_spend),
  }))

  return (
    <div className="trends-section">
      <div className="tab-bar">
        {(['attendance', 'learning', 'spend'] as Tab[]).map((t) => (
          <button
            key={t}
            className={`tab ${tab === t ? 'active' : ''}`}
            onClick={() => setTab(t)}
          >
            {t === 'attendance' ? 'Attendance' : t === 'learning' ? 'Learning scores' : 'Spending'}
          </button>
        ))}
      </div>

      <div className="chart-wrap tall">
        {tab === 'attendance' && (
          <ResponsiveContainer width="100%" height={300}>
            <AreaChart data={attData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
              <XAxis dataKey="month" tick={{ fontSize: 11 }} />
              <YAxis yAxisId="left" tick={{ fontSize: 11 }} domain={[0, 100]} />
              <YAxis yAxisId="right" orientation="right" tick={{ fontSize: 11 }} />
              <Tooltip />
              <Legend />
              <Area yAxisId="left" type="monotone" dataKey="rate" name="Attendance %" stroke="#059669" fill="#d1fae5" />
              <Line yAxisId="right" type="monotone" dataKey="sessions" name="Sessions" stroke="#2563eb" strokeWidth={2} dot={false} />
            </AreaChart>
          </ResponsiveContainer>
        )}

        {tab === 'learning' && (
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={learnData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
              <XAxis dataKey="month" tick={{ fontSize: 11 }} />
              <YAxis tick={{ fontSize: 11 }} domain={[0, 100]} />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="pre" name="Pre-score" stroke="#94a3b8" strokeWidth={2} dot={false} />
              <Line type="monotone" dataKey="post" name="Post-score" stroke="#2563eb" strokeWidth={2} dot={false} />
              <Line type="monotone" dataKey="gain" name="Gain" stroke="#059669" strokeWidth={2} strokeDasharray="5 5" dot={false} />
            </LineChart>
          </ResponsiveContainer>
        )}

        {tab === 'spend' && (
          <ResponsiveContainer width="100%" height={300}>
            <AreaChart data={spendData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
              <XAxis dataKey="month" tick={{ fontSize: 11 }} />
              <YAxis tick={{ fontSize: 11 }} tickFormatter={(v) => `₹${(v / 1000).toFixed(0)}K`} />
              <Tooltip formatter={(v: number) => [`₹${v.toLocaleString('en-IN')}`, 'Spend']} />
              <Area type="monotone" dataKey="spend" name="Monthly spend" stroke="#dc2626" fill="#fee2e2" />
            </AreaChart>
          </ResponsiveContainer>
        )}
      </div>
    </div>
  )
}
