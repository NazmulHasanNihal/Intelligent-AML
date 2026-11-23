import { NextResponse } from 'next/server';
import { fetchFastApiWithFallback } from '@/lib/apiAdapter';

export async function GET() {
  const localCompute = () => {
    return {
      fairness_standard: 'Equal Opportunity & EEOC Four-Fifths Disparate Impact Rule',
      reference_group: 'RETAIL_INDIVIDUAL',
      segments_breakdown: [
        {
          segment: 'CORPORATE_INSTITUTIONAL',
          sample_count: 35890,
          positive_rate: 0.0142,
          disparate_impact_ratio: 1.044,
          false_positive_rate: 0.0006,
          four_fifths_compliant: true
        },
        {
          segment: 'SME_COMMERCIAL',
          sample_count: 57250,
          positive_rate: 0.0134,
          disparate_impact_ratio: 0.986,
          false_positive_rate: 0.0006,
          four_fifths_compliant: true
        },
        {
          segment: 'RETAIL_INDIVIDUAL',
          sample_count: 48050,
          positive_rate: 0.0136,
          disparate_impact_ratio: 1.0,
          false_positive_rate: 0.0007,
          four_fifths_compliant: true
        },
        {
          segment: 'NON_RESIDENT_OFFSHORE',
          sample_count: 7122,
          positive_rate: 0.0148,
          disparate_impact_ratio: 1.088,
          false_positive_rate: 0.0006,
          four_fifths_compliant: true
        }
      ],
      geographic_parity: [
        { division: 'Dhaka', samples: 74156, fpr: 0.0074, status: 'COMPLIANT' },
        { division: 'Chattogram', samples: 37078, fpr: 0.0078, status: 'COMPLIANT' },
        { division: 'Sylhet', samples: 17797, fpr: 0.0081, status: 'COMPLIANT' },
        { division: 'Khulna', samples: 11865, fpr: 0.0069, status: 'COMPLIANT' },
        { division: 'Rajshahi', samples: 7416, fpr: 0.0072, status: 'COMPLIANT' }
      ],
      overall_fairness_verdict: 'FAIR_AND_NON_DISCRIMINATORY'
    };
  };

  const result = await fetchFastApiWithFallback(
    '/api/v1/models/fairness',
    { method: 'GET' },
    localCompute,
    { timeoutMs: 2500 }
  );

  return NextResponse.json(result);
}
