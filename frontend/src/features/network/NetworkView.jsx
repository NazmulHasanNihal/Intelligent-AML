import React, { useState, Suspense } from 'react';
import { Share2, Box, Eye, Info, Sparkles } from 'lucide-react';
import { Cytoscape2DGraph } from './Cytoscape2DGraph';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';

// Lazy-load the heavy 3D WebGL engine so it doesn't slow down first load
const Neo4j3DGraph = React.lazy(() => import('../../components/Neo4j3DGraph'));

export const NetworkView = () => {
  const [engineMode, setEngineMode] = useState('2D'); // '2D' (default Cytoscape) | '3D' (WebGL Force Graph)

  return (
    <div className="space-y-4">
      {/* Top Bar with Mode Switcher */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 p-4 rounded-lg bg-surface border border-border">
        <div className="min-w-0">
          <div className="flex items-center gap-2">
            <h2 className="text-sm font-semibold text-text">Forensic Network Topology</h2>
            <Badge variant="neutral" size="sm">Consolidated Dual-Engine</Badge>
          </div>
          <p className="text-xs text-text-2 mt-0.5">
            Interactive peeling chains, smurfing aggregations, and cycle-3 wash loops.
          </p>
        </div>

        {/* Engine Switcher */}
        <div className="flex items-center gap-1 p-0.5 bg-bg rounded border border-border font-mono text-xs">
          <button
            onClick={() => setEngineMode('2D')}
            className={`px-3 py-1 rounded transition-colors cursor-pointer ${
              engineMode === '2D' ? 'bg-surface font-semibold text-text shadow-sm' : 'text-text-muted hover:text-text'
            }`}
          >
            2D Cytoscape (Default)
          </button>

          <button
            onClick={() => setEngineMode('3D')}
            className={`px-3 py-1 rounded transition-colors cursor-pointer flex items-center gap-1 ${
              engineMode === '3D' ? 'bg-surface font-semibold text-text shadow-sm' : 'text-text-muted hover:text-text'
            }`}
          >
            <Box className="w-3.5 h-3.5" />
            <span>3D WebGL Engine</span>
          </button>
        </div>
      </div>

      {/* Main Graph Viewport */}
      {engineMode === '2D' ? (
        <Cytoscape2DGraph />
      ) : (
        <div className="w-full h-[540px] sm:h-[600px] rounded-lg border border-border overflow-hidden relative bg-surface">
          <Suspense fallback={
            <div className="w-full h-full flex flex-col items-center justify-center text-xs font-mono text-text-muted gap-2">
              <span className="w-3 h-3 rounded-full bg-accent animate-ping" />
              <span>Initializing WebGL 3D Force Graph Engine...</span>
            </div>
          }>
            <Neo4j3DGraph />
          </Suspense>
        </div>
      )}
    </div>
  );
};
