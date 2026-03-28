export default function SchemeDetailPage({ scheme, onBack }) {
  if (!scheme) return null

  return (
    <div style={{ minHeight: '100vh', background: '#f5f5f5', fontFamily: "'Outfit', system-ui, sans-serif" }}>

      {/* HEADER */}
      <div style={{ background: scheme.color, padding: '20px 16px 24px' }}>
        <button onClick={onBack} style={{
          background: 'none', border: 'none', color: 'rgba(255,255,255,0.85)',
          fontSize: '0.85rem', fontWeight: 600, cursor: 'pointer',
          fontFamily: 'inherit', padding: 0, marginBottom: 16,
          display: 'flex', alignItems: 'center', gap: 4
        }}>← Back</button>

        <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
          <span style={{ fontSize: '2rem' }}>{scheme.emoji}</span>
          <div>
            <div style={{ fontSize: '0.65rem', fontWeight: 800, color: 'rgba(255,255,255,0.6)', textTransform: 'uppercase', letterSpacing: '0.1em' }}>{scheme.tag}</div>
            <h1 style={{ fontSize: '1.3rem', fontWeight: 900, color: '#fff', margin: '2px 0 0' }}>{scheme.name}</h1>
          </div>
        </div>
      </div>

      <div style={{ padding: '16px', display: 'flex', flexDirection: 'column', gap: 10 }}>

        {/* ABOUT — compact */}
        <p style={{ fontSize: '0.85rem', color: '#444', lineHeight: 1.6, margin: 0, background: '#fff', padding: '12px 14px', borderRadius: 10 }}>
          {scheme.detailDesc}
        </p>

        {/* ELIGIBILITY + BENEFIT — single row */}
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 8 }}>
          <div style={{ background: '#fff', borderRadius: 10, padding: '10px 12px', borderLeft: `3px solid ${scheme.color}` }}>
            <div style={{ fontSize: '0.6rem', fontWeight: 800, color: scheme.color, textTransform: 'uppercase', letterSpacing: '0.07em', marginBottom: 3 }}>Who can apply</div>
            <div style={{ fontSize: '0.75rem', color: '#333', lineHeight: 1.4 }}>{scheme.eligibility}</div>
          </div>
          <div style={{ background: '#fff', borderRadius: 10, padding: '10px 12px', borderLeft: `3px solid ${scheme.color}` }}>
            <div style={{ fontSize: '0.6rem', fontWeight: 800, color: scheme.color, textTransform: 'uppercase', letterSpacing: '0.07em', marginBottom: 3 }}>Benefit</div>
            <div style={{ fontSize: '0.75rem', color: '#333', lineHeight: 1.4 }}>{scheme.benefit}</div>
          </div>
        </div>

        {/* PDFs — PROMINENT */}
        {scheme.hasPdf && (
          <div style={{ background: '#fff', borderRadius: 10, overflow: 'hidden' }}>
            <div style={{ padding: '10px 14px', background: scheme.color }}>
              <span style={{ fontSize: '0.75rem', fontWeight: 800, color: '#fff' }}>📄 Application Forms</span>
            </div>
            {[
              { lang: 'English', flag: '🇬🇧', pdf: scheme.pdfEn, label: 'Download Form (English)' },
              { lang: 'Hindi',   flag: '🇮🇳', pdf: scheme.pdfHi, label: 'आवेदन फॉर्म (हिंदी)' },
            ].map((btn, i) => (
              <a key={btn.lang} href={btn.pdf} download style={{
                display: 'flex', alignItems: 'center', justifyContent: 'space-between',
                padding: '14px 16px',
                borderTop: i > 0 ? '1px solid #f0f0f0' : 'none',
                textDecoration: 'none',
              }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                  <span style={{ fontSize: '1.4rem' }}>📄</span>
                  <div>
                    <div style={{ fontSize: '0.9rem', fontWeight: 700, color: '#111' }}>{btn.label}</div>
                    <div style={{ fontSize: '0.7rem', color: '#888' }}>{btn.flag} {btn.lang} · PDF</div>
                  </div>
                </div>
                <div style={{
                  background: scheme.color, color: '#fff',
                  borderRadius: 8, padding: '6px 14px',
                  fontSize: '0.8rem', fontWeight: 700
                }}>↓ Download</div>
              </a>
            ))}
          </div>
        )}

        {/* STEPS for no-PDF schemes */}
        {!scheme.hasPdf && scheme.steps && (
          <div style={{ background: '#fff', borderRadius: 10, overflow: 'hidden' }}>
            <div style={{ padding: '10px 14px', background: scheme.color }}>
              <span style={{ fontSize: '0.75rem', fontWeight: 800, color: '#fff' }}>🚀 How to Apply</span>
            </div>
            {scheme.steps.map((step, i) => (
              <div key={i} style={{
                display: 'flex', gap: 12, padding: '12px 16px',
                borderTop: i > 0 ? '1px solid #f0f0f0' : 'none',
                alignItems: 'flex-start'
              }}>
                <div style={{
                  width: 24, height: 24, borderRadius: '50%', flexShrink: 0,
                  background: scheme.bgLight, color: scheme.color,
                  fontSize: '0.7rem', fontWeight: 900,
                  display: 'flex', alignItems: 'center', justifyContent: 'center'
                }}>{i + 1}</div>
                <div style={{ fontSize: '0.85rem', color: '#333', lineHeight: 1.5, paddingTop: 2 }}>
                  {step.icon} {step.text}
                </div>
              </div>
            ))}
          </div>
        )}

        {/* PORTAL + HELPLINE — minimal */}
        <div style={{ display: 'flex', gap: 8 }}>
          {scheme.portal && (
            <a href={scheme.portal} target="_blank" rel="noopener noreferrer" style={{
              flex: 1, padding: '12px', background: '#fff',
              border: `1.5px solid ${scheme.color}`, borderRadius: 10,
              color: scheme.color, fontSize: '0.82rem', fontWeight: 700,
              textDecoration: 'none', textAlign: 'center'
            }}>🌐 Official Portal</a>
          )}
          <a href="tel:18001801551" style={{
            flex: 1, padding: '12px', background: '#fff',
            border: '1.5px solid #388e3c', borderRadius: 10,
            color: '#2e7d32', fontSize: '0.82rem', fontWeight: 700,
            textDecoration: 'none', textAlign: 'center'
          }}>📞 1800-180-1551</a>
        </div>

      </div>
    </div>
  )
}