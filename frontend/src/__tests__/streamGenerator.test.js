import { describe, it, expect } from 'vitest';
import { streamService } from '../lib/streamGenerator';

describe('Real-World Transaction Stream Service', () => {
  it('instantiates stream service with default speed', () => {
    expect(streamService).toBeDefined();
    expect(streamService.speed).toBe(1);
    expect(streamService.isRunning).toBe(false);
  });

  it('generates synthetic transaction conforming to real-world rails', () => {
    const tx = streamService.generateSyntheticTransaction();
    expect(tx).toBeDefined();
    expect(tx.id).toMatch(/^TX-\d+/);
    expect(tx.amount).toBeGreaterThan(0);
    expect(tx.sourceAccount).toBeDefined();
    expect(tx.targetAccount).toBeDefined();
    expect(typeof tx.riskScore).toBe('number');
    expect([1, 2, 3]).toContain(tx.tierCode);
  });

  it('adjusts stream speed factor properly', () => {
    streamService.setSpeed(5);
    expect(streamService.speed).toBe(5);
    streamService.setSpeed(1);
    expect(streamService.speed).toBe(1);
  });

  it('injects predefined scenarios successfully', () => {
    const scenarioTxs = streamService.injectLocalScenario('structuring');
    expect(Array.isArray(scenarioTxs)).toBe(true);
    expect(scenarioTxs.length).toBeGreaterThan(0);
    const firstTx = scenarioTxs[0];
    expect(firstTx.rail).toContain('SWIFT MT700');
    expect(firstTx.tierCode).toBe(1);
    expect(firstTx.riskScore).toBeGreaterThan(0.70);
  });
});
