import { describe, it, expect, beforeEach } from 'vitest';
import { useAppStore } from '../lib/store';

describe('Intelligent-AML Zustand Central Store', () => {
  beforeEach(() => {
    useAppStore.getState().resetWorkspaceData();
  });

  it('initializes with default jurisdiction as BD_BFIU', () => {
    const state = useAppStore.getState();
    expect(state.jurisdiction).toBe('BD_BFIU');
    expect(state.densityMode).toBe('compact');
  });

  it('switches jurisdiction cleanly and updates active profile', () => {
    const { setActiveJurisdiction } = useAppStore.getState();
    setActiveJurisdiction('US_FINCEN');
    const state = useAppStore.getState();
    expect(state.jurisdiction).toBe('US_FINCEN');
    expect(state.activeJurisdiction).toBe('US_FINCEN');
  });

  it('contains seeded commercial alerts and cases', () => {
    const state = useAppStore.getState();
    expect(state.alerts.length).toBeGreaterThan(0);
    expect(state.cases.length).toBeGreaterThan(0);
    expect(state.customers.length).toBeGreaterThan(0);
    expect(state.ctrRecords.length).toBeGreaterThan(0);
  });

  it('toggles stream execution state', () => {
    const { toggleLiveStream } = useAppStore.getState();
    const initialRunning = useAppStore.getState().isLiveStreamActive;
    toggleLiveStream();
    expect(useAppStore.getState().isLiveStreamActive).toBe(!initialRunning);
    toggleLiveStream();
    expect(useAppStore.getState().isLiveStreamActive).toBe(initialRunning);
  });

  it('allows setting stream speed multiplier', () => {
    const { setStreamSpeed } = useAppStore.getState();
    setStreamSpeed(5);
    expect(useAppStore.getState().streamSpeed).toBe(5);
    setStreamSpeed(1);
    expect(useAppStore.getState().streamSpeed).toBe(1);
  });

  it('handles audited PII unmasking', async () => {
    const { revealPii, isPiiRevealed } = useAppStore.getState();
    expect(isPiiRevealed()).toBe(false);
    await revealPii();
    expect(isPiiRevealed()).toBe(true);
  });
});
