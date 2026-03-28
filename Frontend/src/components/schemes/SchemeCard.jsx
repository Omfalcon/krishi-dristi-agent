// src/components/schemes/SchemeCard.jsx
// Renders one scheme card in the list view.
// Props: scheme (object), onClick (fn)

export default function SchemeCard({ scheme, onClick }) {
  return (
    <button
      onClick={() => onClick(scheme)}
      style={{
        width: '100%',
        background: '#fff',
        border: `1.5px solid ${scheme.bgLight}`,
        borderRadius: 18,
        padding: '16px 18px',
        display: 'flex',
        alignItems: 'center',
        gap: 16,
        cursor: 'pointer',
        textAlign: 'left',
        boxShadow: '0 2px 14px rgba(0,0,0,0.06)',
        transition: 'transform 0.2s ease, box-shadow 0.2s ease',
        position: 'relative',
        overflow: 'hidden',
      }}
      onMouseEnter={e => {
        e.currentTarget.style.transform = 'translateY(-2px)'
        e.currentTarget.style.boxShadow = '0 8px 28px rgba(0,0,0,0.12)'
      }}
      onMouseLeave={e => {
        e.currentTarget.style.transform = 'translateY(0)'
        e.currentTarget.style.boxShadow = '0 2px 14px rgba(0,0,0,0.06)'
      }}
      aria-label={`View details for ${scheme.name}`}
    >
      {/* Left accent bar */}
      <div style={{
        position: 'absolute', left: 0, top: 0, bottom: 0, width: 4,
        background: scheme.color, borderRadius: '18px 0 0 18px',
      }} />

      {/* Emoji icon */}
      <div style={{
        width: 48, height: 48, borderRadius: 14, flexShrink: 0,
        background: scheme.bgLight,
        display: 'flex', alignItems: 'center', justifyContent: 'center',
        fontSize: '1.5rem',
        marginLeft: 8,
      }}>
        {scheme.emoji}
      </div>

      {/* Text */}
      <div style={{ flex: 1, minWidth: 0 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 4 }}>
          <span style={{
            fontSize: '0.68rem', fontWeight: 800,
            color: scheme.color,
            background: scheme.bgLight,
            padding: '2px 8px', borderRadius: 6,
            letterSpacing: '0.04em', textTransform: 'uppercase',
          }}>
            {scheme.tag}
          </span>
          {scheme.hasPdf && (
            <span style={{ fontSize: '0.68rem', color: '#9e9e9e' }}>📄 PDF</span>
          )}
        </div>
        <div style={{
          fontSize: '0.97rem', fontWeight: 700, color: '#1a1005',
          lineHeight: 1.2, marginBottom: 4,
        }}>
          {scheme.name}
        </div>
        <div style={{
          fontSize: '0.78rem', color: 'rgba(26,16,5,0.55)',
          lineHeight: 1.45,
          overflow: 'hidden', textOverflow: 'ellipsis',
          display: '-webkit-box', WebkitLineClamp: 2, WebkitBoxOrient: 'vertical',
        }}>
          {scheme.description}
        </div>
      </div>

      {/* Arrow */}
      <div style={{
        fontSize: '1rem', color: scheme.color,
        fontWeight: 700, flexShrink: 0, marginRight: 4,
        opacity: 0.7,
      }}>
        →
      </div>
    </button>
  )
}