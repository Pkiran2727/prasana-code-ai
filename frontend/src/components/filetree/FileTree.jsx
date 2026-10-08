import React, { useState } from 'react';
import { Plus, FolderPlus, FilePlus, ChevronDown } from 'lucide-react';
import FileItem from './FileItem';

export default function FileTree({
  files, // array of top-level nodes: { name, path, type: 'file' | 'directory', children: [] }
  activeFile,
  onFileClick,
  onDeleteFile,
  onRenameFile,
  onCreateFile,
  onCreateFolder,
}) {
  const [showRootInput, setShowRootInput] = useState(null); // 'file' | 'folder' | null
  const [rootInputName, setRootInputName] = useState('');

  const handleRootSubmit = (e) => {
    e.preventDefault();
    if (rootInputName.trim()) {
      if (showRootInput === 'file') {
        onCreateFile('', rootInputName.trim());
      } else if (showRootInput === 'folder') {
        onCreateFolder('', rootInputName.trim());
      }
    }
    setRootInputName('');
    setShowRootInput(null);
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Escape') {
      setRootInputName('');
      setShowRootInput(null);
    }
  };

  return (
    <div className="flex-grow flex flex-col overflow-hidden select-none h-full bg-ide-sidebar font-sans">
      {/* Title Header */}
      <div className="h-9 px-3 border-b border-ide-border flex items-center justify-between text-xs font-bold text-ide-muted tracking-wider uppercase select-none shrink-0">
        <span className="flex items-center gap-1">
          <ChevronDown className="w-3.5 h-3.5" />
          Explorer: Project
        </span>
        <div className="flex items-center gap-1 select-none">
          <button
            onClick={() => setShowRootInput('file')}
            title="New File at Root"
            className="p-0.5 rounded hover:bg-ide-border text-ide-muted hover:text-ide-text transition-colors"
          >
            <FilePlus className="w-3.5 h-3.5" />
          </button>
          <button
            onClick={() => setShowRootInput('folder')}
            title="New Folder at Root"
            className="p-0.5 rounded hover:bg-ide-border text-ide-muted hover:text-ide-text transition-colors"
          >
            <FolderPlus className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>

      {/* Nodes list */}
      <div className="flex-grow overflow-y-auto py-2 select-none">
        {/* Root Inline Input Form */}
        {showRootInput && (
          <div className="px-3 mb-2">
            <form onSubmit={handleRootSubmit} className="flex gap-1.5 items-center">
              <span className="text-[10px] text-accent-blue font-bold uppercase shrink-0">
                {showRootInput === 'file' ? 'New File' : 'New Dir'}
              </span>
              <input
                type="text"
                autoFocus
                value={rootInputName}
                onChange={(e) => setRootInputName(e.target.value)}
                onBlur={() => setShowRootInput(null)}
                onKeyDown={handleKeyDown}
                placeholder={showRootInput === 'file' ? 'main.py' : 'src'}
                className="flex-grow bg-ide-bg text-ide-text border border-accent-blue px-2 py-0.5 rounded text-xs focus:outline-none"
              />
            </form>
          </div>
        )}

        {/* Existing file tree */}
        {files.length === 0 ? (
          <div className="px-4 py-8 text-center text-xs text-ide-muted font-sans">
            Workspace is empty
          </div>
        ) : (
          files.map((node) => (
            <FileItem
              key={node.path}
              node={node}
              activeFile={activeFile}
              onFileClick={onFileClick}
              onDelete={onDeleteFile}
              onRename={onRenameFile}
              onCreateFile={(parentPath) => onCreateFile(parentPath)}
              onCreateFolder={(parentPath) => onCreateFolder(parentPath)}
            />
          ))
        )}
      </div>

      {/* Quick Root Control Buttons at the Bottom */}
      <div className="p-3 border-t border-ide-border flex gap-2 select-none shrink-0 bg-ide-sidebar/55">
        <button
          onClick={() => setShowRootInput('file')}
          className="flex-1 flex items-center justify-center gap-1.5 bg-ide-panel hover:bg-ide-border border border-ide-border text-ide-text hover:text-ide-text py-1.5 rounded text-xs font-semibold transition-all"
        >
          <Plus className="w-3.5 h-3.5" />
          File
        </button>
        <button
          onClick={() => setShowRootInput('folder')}
          className="flex-1 flex items-center justify-center gap-1.5 bg-ide-panel hover:bg-ide-border border border-ide-border text-ide-text hover:text-ide-text py-1.5 rounded text-xs font-semibold transition-all"
        >
          <FolderPlus className="w-3.5 h-3.5 animate-pulse-slow" />
          Folder
        </button>
      </div>
    </div>
  );
}
