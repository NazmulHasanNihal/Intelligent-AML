import React, { createContext, useContext, useState, useEffect } from 'react';

export const THEMES = {
  LIGHT: {
    id: 'light',
    name: 'Daylight',
    icon: '☀️',
    description: 'Clean, high-contrast light mode for daytime review and reports.'
  },
  DARK: {
    id: 'dark',
    name: 'Dark Slate',
    icon: '🌙',
    description: 'Minimalist dark mode for prolonged analytical focus.'
  },
  HIGH_CONTRAST: {
    id: 'high-contrast',
    name: 'High Contrast',
    icon: '👁️',
    description: 'Maximum contrast mode compliant with WCAG 2.1 AAA accessibility.'
  },
  AUTO: {
    id: 'auto',
    name: 'System Auto',
    icon: '💻',
    description: 'Automatically synchronizes with your operating system preference.'
  }
};

const ThemeContext = createContext({
  theme: 'dark',
  resolvedTheme: 'dark',
  setTheme: () => {},
  toggleTheme: () => {},
  density: 'comfortable',
  setDensity: () => {},
  toggleDensity: () => {},
  availableThemes: THEMES
});

export const ThemeProvider = ({ children }) => {
  const [theme, setThemeState] = useState(() => {
    return localStorage.getItem('iaml_theme') || 'dark';
  });

  const [density, setDensityState] = useState(() => {
    return localStorage.getItem('iaml_density') || 'comfortable';
  });

  // Calculate resolved theme (if 'auto', check system dark preference)
  const [systemIsDark, setSystemIsDark] = useState(() => {
    if (typeof window !== 'undefined' && window.matchMedia) {
      return window.matchMedia('(prefers-color-scheme: dark)').matches;
    }
    return true;
  });

  useEffect(() => {
    if (typeof window === 'undefined' || !window.matchMedia) return;
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    const handler = (e) => setSystemIsDark(e.matches);
    mediaQuery.addEventListener('change', handler);
    return () => mediaQuery.removeEventListener('change', handler);
  }, []);

  const resolvedTheme = theme === 'auto' 
    ? (systemIsDark ? 'dark' : 'light') 
    : theme;

  useEffect(() => {
    localStorage.setItem('iaml_theme', theme);
    const root = document.documentElement;

    root.setAttribute('data-theme', resolvedTheme);

    if (resolvedTheme === 'dark' || resolvedTheme === 'high-contrast') {
      root.classList.add('dark');
      root.classList.remove('light');
    } else {
      root.classList.add('light');
      root.classList.remove('dark');
    }
  }, [theme, resolvedTheme]);

  useEffect(() => {
    localStorage.setItem('iaml_density', density);
    document.documentElement.setAttribute('data-density', density);
  }, [density]);

  const setTheme = (newTheme) => {
    if (THEMES[newTheme?.toUpperCase()] || Object.values(THEMES).some(t => t.id === newTheme)) {
      setThemeState(newTheme);
    }
  };

  const toggleTheme = () => {
    setThemeState(prev => (prev === 'dark' ? 'light' : 'dark'));
  };

  const setDensity = (newDensity) => {
    setDensityState(newDensity);
  };

  const toggleDensity = () => {
    setDensityState(prev => (prev === 'comfortable' ? 'compact' : 'comfortable'));
  };

  return (
    <ThemeContext.Provider
      value={{
        theme,
        resolvedTheme,
        currentTheme: THEMES[resolvedTheme.toUpperCase()] || THEMES.DARK,
        themeId: resolvedTheme,
        setTheme,
        toggleTheme,
        density,
        setDensity,
        toggleDensity,
        availableThemes: THEMES
      }}
    >
      {children}
    </ThemeContext.Provider>
  );
};

export const useTheme = () => useContext(ThemeContext);
