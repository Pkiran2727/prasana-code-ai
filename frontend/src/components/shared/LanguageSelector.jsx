import React from 'react';
import { ChevronDown } from 'lucide-react';

export const LANGUAGES = [
  { value: 'python', label: 'Python 🐍', extension: '.py' },
  { value: 'javascript', label: 'JavaScript ⚡', extension: '.js' },
  { value: 'cpp', label: 'C++ 🛠️', extension: '.cpp' },
  { value: 'c', label: 'C 🔩', extension: '.c' },
];

export default function LanguageSelector({ selectedLanguage, onChange }) {
  return (
    <div className="relative inline-block">
      <select
        value={selectedLanguage}
        onChange={(e) => onChange(e.target.value)}
        className="appearance-none bg-ide-sidebar hover:bg-ide-border text-ide-text px-4 pr-10 py-1.5 rounded-md border border-ide-border focus:outline-none focus:ring-1 focus:ring-accent-blue transition-colors cursor-pointer text-sm font-medium"
      >
        {LANGUAGES.map((lang) => (
          <option key={lang.value} value={lang.value} className="bg-ide-sidebar text-ide-text py-2">
            {lang.label}
          </option>
        ))}
      </select>
      <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center px-3 text-ide-muted">
        <ChevronDown className="w-4 h-4" />
      </div>
    </div>
  );
}
