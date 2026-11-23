import { NextResponse } from 'next/server';
import { APP_MODE, IS_ONPREM_MODE } from '@/lib/config/env';

export async function GET() {
  return NextResponse.json({
    status: 'healthy',
    timestamp: new Date().toISOString(),
    service: 'intelligent-aml-frontend-bff',
    version: '3.0.0',
    mode: APP_MODE,
    airGapped: IS_ONPREM_MODE,
    uptimeSeconds: process.uptime ? Math.round(process.uptime()) : 0,
  });
}
