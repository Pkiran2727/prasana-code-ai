import React, { useEffect, useRef } from 'react';
import { Terminal as TerminalIcon, Trash2, Loader2 } from 'lucide-react';

export default function Terminal({
  lines = [], // list of { type: 'stdout' | 'stderr' | 'system', text: string }
  onClearTerminal,
  isRunning = false
}) {
  const terminalEndRef = useRef(null);

  // Auto-scroll to bottom of output
  useEffect(() => {
    terminalEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [lines, isRunning]);

  return (
    <div className="flex-1 flex flex-col h-full overflow-hidden bg-ide-terminal font-mono text-xs select-none">
      {/* Terminal Title Header */}
      <div className="h-8 px-3 bg-ide-navbar border-b border-ide-border flex items-center justify-between text-ide-muted font-sans font-bold tracking-wider uppercase shrink-0">
        <span className="flex items-center gap-1.5 select-none">
          <TerminalIcon className="w-4 h-4 text-emerald-400" />
          Terminal Output
        </span>
        {lines.length > 0 && (
          <button
            onClick={onClearTerminal}
            title="Clear Output"
            className="p-1 rounded hover:bg-ide-border text-ide-muted hover:text-ide-text transition-colors"
          >
            <Trash2 className="w-3.5 h-3.5" />
          </button>
        )}
      </div>

      {/* Output Console Box */}
      <div className="flex-1 overflow-y-auto p-3.5 space-y-1 select-text">
        {lines.length === 0 && !isRunning ? (
          <div className="h-full flex items-center justify-center text-ide-muted font-sans select-none text-[11px]">
            No execution logs yet. Click 'Run' to compile and execute your code.
          </div>
        ) : (
          lines.map((line, idx) => {
            let textColor = 'text-ide-text';
            if (line.type === 'stderr') {
              textColor = 'text-rose-400 font-medium';
            } else if (line.type === 'stdout') {
              textColor = 'text-emerald-400';
            } else if (line.type === 'system') {
              textColor = 'text-ide-muted font-semibold';
            }

            return (
              <div key={idx} className={`leading-normal whitespace-pre-wrap select-text ${textColor}`}>
                {line.text}
              </div>
            );
          })
        )}

        {/* Live Running Indicator inside Terminal */}
        {isRunning && (
          <div className="flex items-center gap-2 text-accent-blue font-sans font-bold select-none pt-1">
            <Loader2 className="w-3.5 h-3.5 animate-spin" />
            <span>Running program execution sandboxed container...</span>
          </div>
        )}
        <div ref={terminalEndRef} />
      </div>
    </div>
  );
}
