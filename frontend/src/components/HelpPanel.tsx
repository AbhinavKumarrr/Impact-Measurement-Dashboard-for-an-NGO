import { useState } from 'react'

const SECTIONS = [
  {
    title: 'At a glance',
    text: 'Six cards show your most important numbers: children reached, sessions held, attendance rate, learning improvement, total spend, and cost per child.',
  },
  {
    title: 'KPI ladder',
    text: 'A story from what you DO (Activity) → what you DELIVER (Output) → short-term CHANGES (Outcome) → long-term VALUE (Impact). Green progress bars show how close you are to annual targets.',
  },
  {
    title: 'Programme progress',
    text: 'Compare your three programmes side by side. Look for attendance below 70% — that needs a field visit.',
  },
  {
    title: 'Cost per impact',
    text: 'Shows which programme gives the best value for money. Use this in budget meetings with finance staff.',
  },
  {
    title: 'Demographic reach',
    text: 'Are you reaching all districts and both genders fairly? Gaps here mean you may need more outreach.',
  },
  {
    title: 'Trends',
    text: 'Switch between Attendance, Learning scores, and Spending tabs. Watch for downward trends early.',
  },
]

export function HelpPanel() {
  const [open, setOpen] = useState(false)

  return (
    <div className="help-panel">
      <button className="help-toggle" onClick={() => setOpen(!open)}>
        {open ? '✕ Close guide' : '? Help — how to read this dashboard'}
      </button>
      {open && (
        <div className="help-content">
          <p className="help-intro">
            No technical skills needed. This guide explains each section in plain language.
            Full manual: <code>docs/USER_GUIDE.md</code>
          </p>
          <div className="help-grid">
            {SECTIONS.map((s) => (
              <div key={s.title} className="help-card">
                <h4>{s.title}</h4>
                <p>{s.text}</p>
              </div>
            ))}
          </div>
          <p className="help-footer">
            Data updates every 30 seconds. Click <strong>↻ Refresh</strong> for immediate update.
            Questions? Ask your M&E officer.
          </p>
        </div>
      )}
    </div>
  )
}
