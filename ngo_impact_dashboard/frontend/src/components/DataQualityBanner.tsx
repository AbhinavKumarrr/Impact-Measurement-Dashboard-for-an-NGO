import type { DataQuality } from '../types'

interface Props {
  quality: DataQuality
}

export function DataQualityBanner({ quality }: Props) {
  const score = quality.data_quality_score
  const status = score >= 95 ? 'excellent' : score >= 80 ? 'good' : 'attention'

  return (
    <div className={`quality-banner ${status}`}>
      <span className="quality-icon">{status === 'excellent' ? '✓' : status === 'good' ? '◉' : '!'}</span>
      <div>
        <strong>Data quality: {score}%</strong>
        <span>
          {quality.total_records.toLocaleString()} records from field submissions
          {quality.invalid_records > 0 && ` · ${quality.invalid_records} invalid`}
          {quality.duplicate_records > 0 && ` · ${quality.duplicate_records} duplicates`}
        </span>
      </div>
    </div>
  )
}
