// src/pages/schemes/SchemesListPage.jsx
// Full list/grid of all schemes. Clicking a card opens SchemeDetailPage.

import { useState } from 'react'
import { SCHEMES } from '../data/schemes'
import SchemeCard from '../components/schemes/SchemeCard'
import SchemeDetailPage from './SchemeDetailPage'

export default function SchemesListPage({ onBack }) {
  const [selectedScheme, setSelectedScheme] = useState(null)

  // If a scheme is selected → show its detail page
  if (selectedScheme) {
    return (
      <SchemeDetailPage
        scheme={selectedScheme}
        onBack={() => setSelectedScheme(null)}
      />
    )
  }

  return (
    <div style={{
      minHeight: '100vh',
      background: 'linear-gradient(180deg, #f1f8e9 0%, #fafafa 100%)',
      fontFamily: "'Outfit', system-ui, sans-serif",
    }}>

      {/* ── Header ── */}
      <div style={{
        background: 'linear-gradient(135deg, #2e7d32, #1b5e20)',
        padding: '48px 20px 36px',
        position: 'relative',
        overflow: 'hidden',
      }}>
        {/* Back button */}
        {onBack && (
          <button onClick={onBack} style={{
            position: 'absolute', top: 16, left: 16,
            background: 'rgba(255,255,255,0.15)',
            border: '1px solid rgba(255,255,255,0.25)',
            borderRadius: 12, padding: '7px 14px',
            color: '#fff', fontSize: '0.82rem', fontWeight: 600,
            cursor: 'pointer', display: 'flex', alignItems: 'center', gap: 6,
            fontFamily: 'inherit',
          }}>
            ← Back
          </button>
        )}

        {/* Decorative circles */}
        <div style={{
          position: 'absolute', top: -40, right: -40,
          width: 200, height: 200, borderRadius: '50%',
          background: 'rgba(255,255,255,0.06)', pointerEvents: 'none',
        }} />
        <div style={{
          position: 'absolute', bottom: -60, left: -30,
          width: 160, height: 160, borderRadius: '50%',
          background: 'rgba(255,255,255,0.04)', pointerEvents: 'none',
        }} />

        <div style={{ textAlign: 'center', position: 'relative' }}>
          <div style={{ fontSize: '2.2rem', marginBottom: 8 }}>🏛️</div>
          <h1 style={{
            fontSize: '1.55rem', fontWeight: 800, color: '#fff',
            letterSpacing: '-0.02em', marginBottom: 8, margin: '0 0 8px',
          }}>
            Government Schemes
          </h1>
          <p style={{
            fontSize: '0.85rem', color: 'rgba(255,255,255,0.72)',
            margin: 0, lineHeight: 1.5,
          }}>
            सरकारी योजनाएं · Tap any scheme to apply
          </p>
        </div>
      </div>

      {/* ── Search bar ── */}
      <div style={{ padding: '16px 20px 4px' }}>
        <div style={{ position: 'relative' }}>
          <span style={{
            position: 'absolute', left: 14, top: '50%', transform: 'translateY(-50%)',
            fontSize: '1rem', opacity: 0.45, pointerEvents: 'none',
          }}>🔍</span>
          <input
            placeholder="Search schemes…"
            style={{
              width: '100%', padding: '11px 14px 11px 40px',
              borderRadius: 14, border: '1.5px solid rgba(0,0,0,0.1)',
              background: '#fff', fontSize: '0.9rem', fontFamily: 'inherit',
              color: '#1a1005', outline: 'none',
            }}
            onFocus={e => { e.target.style.borderColor = '#2e7d32'; e.target.style.boxShadow = '0 0 0 3px rgba(46,125,50,0.12)' }}
            onBlur={e => { e.target.style.borderColor = 'rgba(0,0,0,0.1)'; e.target.style.boxShadow = 'none' }}
          />
        </div>
      </div>

      {/* ── Stats strip ── */}
      <div style={{
        display: 'flex', gap: 12, padding: '12px 20px',
        overflowX: 'auto', scrollbarWidth: 'none',
      }}>
        {[
          { label: 'Total Schemes', value: SCHEMES.length, emoji: '📋' },
          { label: 'With PDF', value: SCHEMES.filter(s => s.hasPdf).length, emoji: '📄' },
          { label: 'Online Apply', value: SCHEMES.filter(s => !s.hasPdf).length, emoji: '🌐' },
        ].map(stat => (
          <div key={stat.label} style={{
            flexShrink: 0,
            background: '#fff', borderRadius: 14,
            padding: '10px 16px', boxShadow: '0 2px 8px rgba(0,0,0,0.06)',
            border: '1px solid rgba(0,0,0,0.06)',
            display: 'flex', alignItems: 'center', gap: 8,
          }}>
            <span style={{ fontSize: '1.1rem' }}>{stat.emoji}</span>
            <div>
              <div style={{ fontSize: '1.1rem', fontWeight: 800, color: '#2e7d32', lineHeight: 1 }}>
                {stat.value}
              </div>
              <div style={{ fontSize: '0.65rem', color: 'rgba(26,16,5,0.5)', fontWeight: 600, marginTop: 2 }}>
                {stat.label}
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* ── Cards list ── */}
      <div style={{ padding: '4px 20px 80px', display: 'flex', flexDirection: 'column', gap: 12 }}>
        {SCHEMES.map((scheme, i) => (
          <div key={scheme.id} style={{ animation: `fadeSlideUp 0.35s ease both ${i * 0.06}s` }}>
            <SchemeCard scheme={scheme} onClick={setSelectedScheme} />
          </div>
        ))}
      </div>

      <style>{`
        @keyframes fadeSlideUp {
          from { opacity: 0; transform: translateY(16px); }
          to   { opacity: 1; transform: translateY(0); }
        }
      `}</style>
    </div>
  )
}