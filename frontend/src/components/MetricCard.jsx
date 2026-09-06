import React from 'react';

export const MetricCard = ({ title, value, subtitle, icon: Icon, color = 'cyan' }) => {
  const colorMap = {
    cyan: {
      border: 'border-cyan-500/20',
      iconBg: 'bg-cyan-500/10 text-cyan-400',
      badge: 'text-cyan-400',
    },
    green: {
      border: 'border-emerald-500/20',
      iconBg: 'bg-emerald-500/10 text-emerald-400',
      badge: 'text-emerald-400',
    },
    amber: {
      border: 'border-amber-500/20',
      iconBg: 'bg-amber-500/10 text-amber-400',
      badge: 'text-amber-400',
    },
    indigo: {
      border: 'border-indigo-500/20',
      iconBg: 'bg-indigo-500/10 text-indigo-400',
      badge: 'text-indigo-400',
    },
  };

  const theme = colorMap[color] || colorMap.cyan;

  return (
    <div className={`card-panel p-3.5 flex items-center justify-between ${theme.border}`}>
      <div>
        <p className="text-[11px] font-semibold text-slate-400 tracking-wide">{title}</p>
        <h3 className="text-xl font-bold text-white font-mono mt-0.5">{value}</h3>
        <p className={`text-[10px] font-medium font-mono mt-0.5 ${theme.badge}`}>{subtitle}</p>
      </div>
      {Icon && (
        <div className={`w-9 h-9 rounded-lg ${theme.iconBg} flex items-center justify-center`}>
          <Icon className="w-4 h-4" />
        </div>
      )}
    </div>
  );
};
