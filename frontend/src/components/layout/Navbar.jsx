import React from 'react';
import { Code2, Play, Loader2, Sparkles, Award, ShieldCheck, CreditCard, Compass, BookOpen, Layers } from 'lucide-react';
import LanguageSelector from '../shared/LanguageSelector';
import StatusBadge from '../shared/StatusBadge';
import { useTheme, THEMES } from '../../context/ThemeContext';

export default function Navbar({
  activeTab,
  setActiveTab,
  selectedLanguage,
  setSelectedLanguage,
  llmStatus,
  isRunning,
  onRunCode,
  userRole,
  isAuthenticated,
  onOpenLogin,
  onOpenMonitor,
  onLogout
}) {
  const { theme, setTheme } = useTheme();

  const navItems = [
    { id: 'home', label: 'Home', icon: Compass },
    { id: 'journeys', label: 'Journeys', icon: Layers },
    { id: 'practice', label: 'Practice', icon: BookOpen },
    { id: 'pricing', label: 'Pricing', icon: CreditCard }
  ];

  return (
    <header className="h-16 bg-ide-panel/90 backdrop-blur-md border-b border-ide-border flex items-center justify-between px-6 select-none shrink-0 font-sans text-ide-text shadow-lg z-50">
      {/* Brand & Logo */}
      <div className="flex items-center gap-6">
        <div 
          onClick={() => setActiveTab('home')}
          className="flex items-center gap-3 cursor-pointer group"
        >
          <div className="w-9 h-9 rounded-2xl bg-gradient-to-tr from-emerald-500 via-teal-400 to-emerald-300 flex items-center justify-center shadow-md shadow-emerald-500/20 group-hover:scale-105 transition-transform duration-200">
            <Code2 className="w-5 h-5 text-slate-950 font-bold" />
          </div>
          <div className="flex flex-col">
            <span className="font-bold text-lg text-ide-text tracking-tight flex items-center gap-1.5">
              <span>Prasana</span> <span className="bg-gradient-to-r from-emerald-500 to-teal-500 bg-clip-text text-transparent">Code AI</span>
            </span>
            <span className="text-[10px] text-emerald-600 dark:text-emerald-400 font-semibold tracking-wider uppercase flex items-center gap-1">
              by @itsprasana
            </span>
          </div>
        </div>

        {/* Navigation Tabs - Executive Emerald Pill Bar */}
        <nav className="hidden md:flex items-center gap-1.5 bg-ide-panel/90 p-1.5 rounded-2xl border border-ide-border/80">
          {navItems.map((item) => {
            const isActive = activeTab === item.id;
            const IconComp = item.icon;
            return (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                className={`px-3.5 py-1.5 rounded-xl text-xs font-semibold transition-all duration-200 flex items-center gap-1.5 ${
                  isActive
                    ? 'bg-gradient-to-r from-emerald-400 via-teal-400 to-emerald-300 text-slate-950 shadow-md shadow-emerald-500/20'
                    : 'text-ide-muted hover:text-ide-text hover:bg-ide-sidebar/60'
                }`}
              >
                <IconComp className="w-3.5 h-3.5" />
                <span>{item.label}</span>
              </button>
            );
          })}
        </nav>
      </div>

      {/* Right Controls & Socials */}
      <div className="flex items-center gap-4">
        {/* Social Youtube Link */}
        <a
          href="https://www.youtube.com/@itsprasana"
          target="_blank"
          rel="noreferrer"
          className="hidden lg:flex items-center gap-1.5 bg-rose-500/10 hover:bg-rose-500/20 border border-rose-500/30 text-rose-300 px-3 py-1.5 rounded-xl text-xs font-medium transition-all duration-200"
        >
          <svg className="w-4 h-4 fill-rose-400 text-rose-400" viewBox="0 0 24 24">
            <path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/>
          </svg>
          <span>@itsprasana</span>
        </a>

        {/* IDE Controls if in IDE tab */}
        {activeTab === 'ide' && (
          <div className="flex items-center gap-3 border-l border-ide-border pl-4">
            <LanguageSelector selectedLanguage={selectedLanguage} onChange={setSelectedLanguage} />
            <button
              onClick={onRunCode}
              disabled={isRunning}
              className="flex items-center gap-2 bg-gradient-to-r from-emerald-400 to-teal-400 hover:from-emerald-300 hover:to-teal-300 disabled:opacity-50 text-slate-950 font-bold text-xs px-4 py-1.5 rounded-xl transition-all duration-200 shadow-md shadow-emerald-500/20 active:scale-95"
            >
              {isRunning ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" />
                  <span>Running...</span>
                </>
              ) : (
                <>
                  <Play className="w-4 h-4 fill-slate-950" />
                  <span>Run</span>
                </>
              )}
            </button>
          </div>
        )}

        <select
          value={theme}
          onChange={(e) => setTheme(e.target.value)}
          className="bg-ide-sidebar text-ide-text border border-ide-border text-[10px] rounded-lg px-2 py-1 outline-none"
        >
          <option value={THEMES.DARK}>Dark</option>
          <option value={THEMES.LIGHT}>Light</option>
          <option value={THEMES.HC_DARK}>HC Dark</option>
          <option value={THEMES.HC_LIGHT}>HC Light</option>
        </select>

        <StatusBadge status={llmStatus} />

        {isAuthenticated && userRole === 'admin' && (
          <button
            onClick={onOpenMonitor}
            className="bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 hover:bg-emerald-500/30 font-medium text-xs px-3.5 py-1.5 rounded-xl transition-all"
          >
            Admin
          </button>
        )}

        {isAuthenticated ? (
          <button
            onClick={onLogout}
            className="text-xs font-medium text-ide-muted hover:text-ide-text bg-ide-sidebar hover:bg-slate-700 px-3 py-1.5 rounded-xl transition-all"
          >
            Log Out
          </button>
        ) : (
          <button
            onClick={onOpenLogin}
            className="text-xs font-bold text-slate-950 bg-gradient-to-r from-emerald-400 via-teal-400 to-emerald-300 hover:from-emerald-300 hover:to-teal-300 px-4 py-1.5 rounded-xl transition-all shadow-md shadow-emerald-500/20 active:scale-95"
          >
            Log In / Sign Up
          </button>
        )}
      </div>
    </header>
  );
}

