import React from 'react';

export default function StatusBadge({ status = 'online' }) {
  const statusConfig = {
    online: {
      color: 'bg-emerald-500',
      glow: 'shadow-[0_0_10px_rgba(16,185,129,0.3)]',
      text: 'LLM Online',
      textColor: 'text-emerald-400',
      bgColor: 'bg-emerald-500/10',
      borderColor: 'border-emerald-500/20'
    },
    slow: {
      color: 'bg-amber-500',
      glow: 'shadow-[0_0_10px_rgba(245,158,11,0.3)]',
      text: 'LLM Slow',
      textColor: 'text-amber-400',
      bgColor: 'bg-amber-500/10',
      borderColor: 'border-amber-500/20'
    },
    offline: {
      color: 'bg-rose-500',
      glow: 'shadow-[0_0_10px_rgba(239,68,68,0.3)]',
      text: 'LLM Offline',
      textColor: 'text-rose-400',
      bgColor: 'bg-rose-500/10',
      borderColor: 'border-rose-500/20'
    }
  };

  const current = statusConfig[status] || statusConfig.online;

  return (
    <div className={`flex items-center gap-2 px-3 py-1.5 rounded-full border ${current.bgColor} ${current.borderColor} ${current.textColor} transition-all duration-300 text-xs font-semibold select-none`}>
      <span className={`w-2 h-2 rounded-full ${current.color} ${current.glow} animate-pulse-slow`} />
      <span>{current.text}</span>
    </div>
  );
}
