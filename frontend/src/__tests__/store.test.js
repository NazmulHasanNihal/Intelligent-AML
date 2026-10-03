import { describe, it, expect, beforeEach } from 'vitest';
import { useAppStore } from '../lib/store';

describe('Intelligent-AML Zustand Central Store', () => {
  beforeEach(() => {
    // Reset route before each test
    useAppStore.setState({ activeRoute: 'overview', activeRouteParams: {} });
  });

  it('initializes with default active route as overview', () => {
    const state = useAppStore.getState();
    expect(state.activeRoute).toBe('overview');
  });

  it('updates route and params on navigate', () => {
    const { navigate } = useAppStore.getState();
    navigate('alerts', { priority: 'TIER_1' });
    const state = useAppStore.getState();
    expect(state.activeRoute).toBe('alerts');
    expect(state.activeRouteParams).toEqual({ priority: 'TIER_1' });
  });

  it('contains seeded alerts and cases', () => {
    const state = useAppStore.getState();
    expect(state.alerts.length).toBeGreaterThan(0);
    expect(state.cases.length).toBeGreaterThan(0);
  });

  it('toggles stream execution state', () => {
    const { toggleStreamRunning } = useAppStore.getState();
    const initialRunning = useAppStore.getState().isStreamRunning;
    toggleStreamRunning();
    expect(useAppStore.getState().isStreamRunning).toBe(!initialRunning);
    toggleStreamRunning();
    expect(useAppStore.getState().isStreamRunning).toBe(initialRunning);
  });

  it('allows setting stream speed multiplier', () => {
    const { setStreamSpeed } = useAppStore.getState();
    setStreamSpeed(5);
    expect(useAppStore.getState().streamSpeed).toBe(5);
    setStreamSpeed(1);
    expect(useAppStore.getState().streamSpeed).toBe(1);
  });
});
