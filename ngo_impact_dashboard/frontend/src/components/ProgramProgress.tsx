import type { ProgramProgress as Program } from '../types'

interface Props {
  programs: Program[]
}

export function ProgramProgress({ programs }: Props) {
  return (
    <div className="program-list">
      {programs.map((p) => {
        const budgetUsed = p.total_spend && p.budget_allocated
          ? Math.round((p.total_spend / p.budget_allocated) * 100)
          : null
        return (
          <div key={p.program_name} className="program-card">
            <h4>{p.program_name}</h4>
            <div className="program-stats">
              <div>
                <span className="stat-num">{p.enrolled}</span>
                <span className="stat-lbl">Enrolled</span>
              </div>
              <div>
                <span className="stat-num">{p.attendance_rate}%</span>
                <span className="stat-lbl">Attendance</span>
              </div>
              <div>
                <span className="stat-num">+{p.avg_test_score_gain}</span>
                <span className="stat-lbl">Score gain</span>
              </div>
              <div>
                <span className="stat-num">{p.assessed_students}</span>
                <span className="stat-lbl">Assessed</span>
              </div>
            </div>
            {budgetUsed !== null && (
              <div className="budget-bar">
                <div className="budget-fill" style={{ width: `${Math.min(budgetUsed, 100)}%` }} />
                <span>{budgetUsed}% budget used</span>
              </div>
            )}
          </div>
        )
      })}
    </div>
  )
}
