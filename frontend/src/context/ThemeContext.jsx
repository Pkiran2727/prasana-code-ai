import React, { createContext, useContext, useEffect, useState } from 'react';

const ThemeContext = createContext();

export const THEMES = {
  DARK: 'dark',
  LIGHT: 'light',
  HC_DARK: 'hc-dark',
  HC_LIGHT: 'hc-light'
};

export function ThemeProvider({ children }) {
  const [theme, setTheme] = useState(() => {
    if (typeof window !== 'undefined') {
      const stored = localStorage.getItem('pca_theme');
      if (stored && Object.values(THEMES).includes(stored)) return stored;
    }
    return THEMES.DARK; // default
  });

  useEffect(() => {
    const root = window.document.documentElement;
    // Remove all theme classes and data attributes
    Object.values(THEMES).forEach(t => root.classList.remove(t));
    root.setAttribute('data-theme', theme);
    root.classList.add(theme); // Keep class for standard tailwind dark mode if needed
    localStorage.setItem('pca_theme', theme);
  }, [theme]);

  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  const context = useContext(ThemeContext);
  if (context === undefined) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
}
