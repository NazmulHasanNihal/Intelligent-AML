/**
 * env.ts — Centralized Application Mode Configuration
 * 
 * Supports:
 * - APP_MODE = 'demo': Public demonstration environment.
 *   - Persistent disclaimer: "Synthetic demo data, not connected to any institution".
 *   - In-memory seeded state.
 *   - Transparent illustrative metrics labeling.
 * 
 * - APP_MODE = 'onprem': Isolated institutional deployment.
 *   - Connects to private bank gateway.
 *   - Strict air-gap Content Security Policy (connect-src 'self').
 */

export type AppMode = 'demo' | 'onprem';

export const APP_MODE: AppMode = 
  (process.env.NEXT_PUBLIC_APP_MODE as AppMode) || 
  (process.env.APP_MODE as AppMode) || 
  'demo';

export const IS_DEMO_MODE = APP_MODE === 'demo';
export const IS_ONPREM_MODE = APP_MODE === 'onprem';
