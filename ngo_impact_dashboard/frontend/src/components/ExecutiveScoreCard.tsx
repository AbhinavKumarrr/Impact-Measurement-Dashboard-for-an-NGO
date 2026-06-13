interface ExecutiveScoreCardProps {
  score: number
  title?: string
  subtitle?: string
  target?: number
}

function getStatus(score: number, target: number) {
  if (score >= target) return 'excellent'
  if (score >= target * 0.8) return 'good'
  return 'attention'
}

export function ExecutiveScoreCard({
  score,
  title = 'Executive Monday Score',
  subtitle = 'The one number the ED checks every Monday',
  target = 1,
}: ExecutiveScoreCardProps) {
  const status = getStatus(score, target)

  return (
    <section className={`quality-banner ${status}`} style={{ marginBottom: '1.25rem' }}>
      <div className="quality-icon">★</div>
      <div>
        <strong>{title}</strong>
        <span>{subtitle}</span>
      </div>
      <div style={{ marginLeft: 'auto', textAlign: 'right' }}>
        <strong style={{ fontSize: '1.2rem' }}>{score.toFixed(2)}</strong>
        <span>Target: {target.toFixed(2)}</span>
      </div>
    </section>
  )
}