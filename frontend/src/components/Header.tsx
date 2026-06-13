interface Props {
  ngoName: string
  dataSource?: string
  lastUpdated: Date
  loadTimeMs?: number | null
  onRefresh: () => void
}

export function Header({ ngoName, dataSource, lastUpdated, loadTimeMs, onRefresh }: Props) {
  const sourceLabel =
    dataSource === 'postgresql' ? 'Live — PostgreSQL' : 'Sample data — CSV fallback'

  return (
    <header className="header">
      <div className="header-brand">
        <div className="logo">U</div>
        <div>
          <h1>{ngoName}</h1>
          <p className="subtitle">Impact Dashboard — Education programmes in Delhi NCR</p>
        </div>
      </div>
      <div className="header-actions">
        <span className={`badge ${dataSource === 'postgresql' ? 'live' : 'fallback'}`}>
          {sourceLabel}
        </span>
        <span className="updated">
          Updated {lastUpdated.toLocaleTimeString()}
          {loadTimeMs != null && (
            <span className={`load-time ${loadTimeMs < 3000 ? 'fast' : 'slow'}`}>
              {' '}· Loaded in {(loadTimeMs / 1000).toFixed(1)}s
            </span>
          )}
        </span>
        <button className="btn-refresh" onClick={onRefresh} title="Refresh data">
          ↻ Refresh
        </button>
      </div>
    </header>
  )
}
