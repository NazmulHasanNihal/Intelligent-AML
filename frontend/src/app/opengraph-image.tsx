import { ImageResponse } from 'next/og';

export const runtime = 'nodejs';
export const alt = 'Intelligent-AML Enterprise Compliance Platform';
export const size = {
  width: 1200,
  height: 630,
};
export const contentType = 'image/png';

export default async function Image() {
  return new ImageResponse(
    (
      <div
        style={{
          background: '#070B12',
          width: '100%',
          height: '100%',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'flex-start',
          justifyContent: 'center',
          padding: '60px 80px',
          fontFamily: 'sans-serif',
          color: '#F8FAFC',
        }}
      >
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            marginBottom: '24px',
            gap: '12px',
          }}
        >
          <div
            style={{
              width: '24px',
              height: '24px',
              borderRadius: '50%',
              background: '#10B981',
            }}
          />
          <span
            style={{
              fontSize: '28px',
              fontWeight: 'bold',
              letterSpacing: '2px',
              color: '#F8FAFC',
              textTransform: 'uppercase',
            }}
          >
            INTELLIGENT-AML
          </span>
          <span
            style={{
              fontSize: '18px',
              fontWeight: 'bold',
              background: '#1E293B',
              color: '#34D399',
              padding: '4px 12px',
              borderRadius: '6px',
              border: '1px solid #059669',
              marginLeft: '12px',
            }}
          >
            V3.0
          </span>
        </div>

        <h1
          style={{
            fontSize: '50px',
            fontWeight: '900',
            lineHeight: 1.15,
            color: '#FFFFFF',
            maxWidth: '1000px',
            margin: '0 0 24px 0',
          }}
        >
          Eliminate 84% of False Positives with Provable Conformal Risk Guarantees
        </h1>

        <p
          style={{
            fontSize: '22px',
            color: '#94A3B8',
            maxWidth: '900px',
            margin: '0 0 40px 0',
          }}
        >
          Tier-1 Air-Gap-Ready Anti-Money Laundering &amp; Conformal Risk Control OS for Central Banks &amp; Enterprise Financial Institutions.
        </p>

        <div
          style={{
            display: 'flex',
            gap: '32px',
            fontSize: '18px',
            fontFamily: 'monospace',
            color: '#34D399',
          }}
        >
          <span>94.5% Macro F1</span>
          <span>•</span>
          <span>&lt; 200 µs Micro-Clearing</span>
          <span>•</span>
          <span>BFIU MLPA 2012 Ready</span>
          <span>•</span>
          <span>Ed25519 WORM Ledger</span>
        </div>
      </div>
    ),
    {
      ...size,
    }
  );
}
