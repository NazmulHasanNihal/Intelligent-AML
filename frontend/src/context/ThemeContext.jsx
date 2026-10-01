import React, { createContext, useContext, useState, useEffect } from 'react';

export const THEMES = {
  MINIMAL_DARK: {
    id: 'minimal-dark',
    name: 'Obsidian Minimalist (Dark)',
    tagline: 'High-Precision Slate Obsidian with Emerald Accents',
    accentColor: '#10B981',
    accentSecondary: '#059669',
    accentName: 'Emerald Precision',
    badgeClass: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30',
    icon: '⚡',
    description: 'Clean, minimalist enterprise theme with hairline borders, generous spacing, and zero clutter.'
  },
  MINIMAL_LIGHT: {
    id: 'minimal-light',
    name: 'Daylight Clean (Light)',
    tagline: 'Pure Banknote White with Forest Emerald Accents',
    accentColor: '#059669',
    accentSecondary: '#047857',
    accentName: 'Daylight Emerald',
    badgeClass: 'bg-emerald-50 text-emerald-800 border-emerald-200',
    icon: '☀️',
    description: 'Crisp, high-contrast light theme engineered for executive presentations and compliance reviews.'
  },
  QUANTUM_PRISM: {
    id: 'quantum',
    name: 'Quantum Prism (Dark)',
    tagline: 'Deep Cosmic Abyss, Prismatic Dispersion & Laser Topology',
    accentColor: '#06B6D4',
    accentSecondary: '#8B5CF6',
    accentName: 'Quantum Prism',
    badgeClass: 'bg-cyan-500/15 text-cyan-300 border-cyan-500/40 shadow-[0_0_12px_rgba(6,182,212,0.3)]',
    icon: '🔮',
    description: 'High-energy forensic visualization with chromatic refraction, glowing neon lasers, and quantum node topology.'
  }
};

const ThemeContext = createContext({
  currentTheme: THEMES.MINIMAL_DARK,
  themeId: 'minimal-dark',
  setTheme: () => {},
  availableThemes: THEMES
});

export const ThemeProvider = ({ children }) => {
  const [themeId, setThemeId] = useState(() => {
    return localStorage.getItem('intelligent_aml_theme') || 'minimal-dark';
  });

  const currentTheme = Object.values(THEMES).find(t => t.id === themeId) || THEMES.MINIMAL_DARK;

  useEffect(() => {
    localStorage.setItem('intelligent_aml_theme', themeId);
    document.documentElement.setAttribute('data-theme', themeId);
    if (themeId === 'minimal-light' || themeId === 'daylight' || themeId === 'money-green-skeuo') {
      document.documentElement.classList.remove('dark');
      document.documentElement.classList.add('light');
    } else {
      document.documentElement.classList.remove('light');
      document.documentElement.classList.add('dark');
    }
  }, [themeId]);

  const setTheme = (id) => {
    if (Object.values(THEMES).some(t => t.id === id)) {
      setThemeId(id);
    }
  };

  return (
    <ThemeContext.Provider value={{ currentTheme, themeId, setTheme, availableThemes: THEMES }}>
      {children}
    </ThemeContext.Provider>
  );
};

export const useTheme = () => useContext(ThemeContext);
