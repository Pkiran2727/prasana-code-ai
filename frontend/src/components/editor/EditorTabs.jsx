import React from 'react';
import { X, FileCode } from 'lucide-react';

export default function EditorTabs({
  openFiles,
  activeFile,
  setActiveFile,
  onCloseFile,
  fileStates = {} // map of filepath -> { isDirty: boolean }
}) {
  if (!openFiles || openFiles.length === 0) {
    return (
      <div className="h-9 bg-ide-sidebar border-b border-ide-border flex items-center px-4 text-xs text-ide-muted font-sans select-none">
        No open files
      </div>
    );
  }

  // Helper to extract basename of a file path
  const getBasename = (path) => {
    return path.split('/').pop();
  };

  return (
    <div className="h-9 bg-ide-sidebar border-b border-ide-border flex items-center overflow-x-auto overflow-y-hidden select-none shrink-0 scrollbar-thin">
      <div className="flex h-full">
        {openFiles.map((file) => {
          const isActive = file === activeFile;
          const isDirty = fileStates[file]?.isDirty;

          return (
            <div
              key={file}
              onClick={() => setActiveFile(file)}
              className={`h-full flex items-center gap-2 px-3 border-r border-ide-border cursor-pointer transition-colors text-xs font-sans font-medium relative group select-none ${
                isActive
                  ? 'bg-ide-panel text-ide-text border-t-2 border-t-accent-blue'
                  : 'bg-ide-sidebar text-ide-muted hover:bg-ide-panel/50 hover:text-ide-text'
              }`}
            >
              <FileCode className="w-3.5 h-3.5 text-accent-blue" />
              <span className="truncate max-w-[100px]">{getBasename(file)}</span>
              
              {/* Status Indicator (dirty/close) */}
              <div className="flex items-center justify-center w-4 h-4 ml-1">
                {isDirty && !isActive ? (
                  <span className="w-2.5 h-2.5 rounded-full bg-accent-yellow animate-pulse" />
                ) : (
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      onCloseFile(file);
                    }}
                    className="opacity-0 group-hover:opacity-100 hover:bg-ide-border rounded p-0.5 text-ide-muted hover:text-ide-text transition-opacity duration-150"
                  >
                    <X className="w-3 h-3" />
                  </button>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
