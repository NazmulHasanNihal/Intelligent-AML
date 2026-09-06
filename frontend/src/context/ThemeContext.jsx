import React, { createContext, useContext, useState, useEffect } from 'react';

export const THEMES = {
  MONEY_GREEN_SKEUO: {
    id: 'money-green-skeuo',
    name: 'Federal Money Green & White',
    tagline: 'Tactile Currency Banknote Skeuomorphism with Crisp Specular Highlights & Bevels',
    accentColor: '#1B5E34',
    accentSecondary: '#12381E',
    accentName: 'Federal Money Green',
    badgeClass: 'bg-[#E8F5E9] text-[#1B5E34] border-[#81C784]/60 shadow-sm font-semibold',
    icon: '💵',
    description: 'Physical tactile skeuomorphism inspired by crisp bank reserves, intaglio engraving, brushed steel bevels, and lustrous white currency paper.'
  },
  VAULT_MIDNIGHT_SKEUO: {
    id: 'vault-midnight-skeuo',
    name: 'Vault Midnight & Steel',
    tagline: 'Dark Executive Bank Vault with Brushed Steel & Illuminated Mint Phosphor',
    accentColor: '#4EAB68',
    accentSecondary: '#1F5C34',
    accentName: 'Vault Phosphor Mint',
    badgeClass: 'bg-[#1B3624]/70 text-[#85E0A3] border-[#4EAB68]/50 shadow-sm font-semibold',
    icon: '🏛️',
    description: 'Deep ballistic steel panels, dark executive physical dials, and luminescent green terminal readouts.'
  },
  BOTANICAL_CLAY: {
    id: 'botanical-clay',
    name: 'Botanical Emerald Clay',
    tagline: 'Deep Forest #2A7C13 & Radiant Leaf #76C457 on Custard #FFF8CF',
    accentColor: '#76C457',
    accentSecondary: '#2A7C13',
    accentName: 'Botanical Leaf',
    badgeClass: 'bg-[#76C457]/20 text-[#FFF8CF] border-[#76C457]/40 shadow-sm',
    icon: '🌿',
    description: 'Tactile 3D Claymorphic theme with deep sculpted forest obsidian, radiant spring leaf glow, and warm cream custard highlights.'
  },
  QUANTUM: {
    id: 'quantum',
    name: 'Quantum Cyber Clay',
    tagline: 'Deep Carbon & Electric Cyan Glow',
    accentColor: '#06B6D4',
    accentName: 'Electric Cyan',
    badgeClass: 'bg-cyan-500/20 text-cyan-300 border-cyan-500/40 shadow-sm',
    icon: '🌌',
    description: 'Tactile deep carbon clay theme with radiant cyan luminescence and sculpted glass surfaces.'
  },
  SWISS_GOLD: {
    id: 'swiss-gold',
    name: 'Swiss Private Gold Clay',
    tagline: 'Midnight Navy & Refined Champagne Gold',
    accentColor: '#F59E0B',
    accentName: 'Champagne Gold',
    badgeClass: 'bg-amber-500/20 text-amber-300 border-amber-500/40 shadow-sm',
    icon: '🪙',
    description: 'Tactile luxury institutional palette tailored for sovereign asset managers and private banking desks.'
  }
};

const ThemeContext = createContext({
  currentTheme: THEMES.MONEY_GREEN_SKEUO,
  themeId: 'money-green-skeuo',
  setTheme: () => {},
  availableThemes: THEMES
});

export const ThemeProvider = ({ children }) => {
  const [themeId, setThemeId] = useState(() => {
    return localStorage.getItem('intelligent_aml_theme') || 'money-green-skeuo';
  });

  const currentTheme = Object.values(THEMES).find(t => t.id === themeId) || THEMES.MONEY_GREEN_SKEUO;

  useEffect(() => {
    localStorage.setItem('intelligent_aml_theme', themeId);
    document.documentElement.setAttribute('data-theme', themeId);
    if (themeId === 'money-green-skeuo' || themeId === 'organic-cream-clay' || themeId === 'daylight') {
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
