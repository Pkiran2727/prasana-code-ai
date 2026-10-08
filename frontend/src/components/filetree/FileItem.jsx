import React, { useState } from 'react';
import {
  Folder,
  FolderOpen,
  File,
  FileCode,
  ChevronRight,
  ChevronDown,
  Trash2,
  Edit,
  FilePlus,
  FolderPlus
} from 'lucide-react';

export default function FileItem({
  node,
  activeFile,
  onFileClick,
  onDelete,
  onRename,
  onCreateFile,
  onCreateFolder,
  level = 0
}) {
  const [isExpanded, setIsExpanded] = useState(true);
  const [isHovered, setIsHovered] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [editName, setEditName] = useState(node.name);

  const paddingLeft = `${level * 12 + 8}px`;
  const isFolder = node.type === 'directory';
  const isActive = activeFile === node.path;

  const handleToggle = (e) => {
    e.stopPropagation();
    if (isFolder) {
      setIsExpanded(!isExpanded);
    } else {
      onFileClick(node.path);
    }
  };

  const handleRenameSubmit = (e) => {
    e.preventDefault();
    if (editName.trim() && editName !== node.name) {
      onRename(node.path, editName.trim());
    }
    setIsEditing(false);
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Escape') {
      setEditName(node.name);
      setIsEditing(false);
    }
  };

  // Get file icon based on extension
  const getFileIcon = (fileName) => {
    const ext = fileName.split('.').pop().toLowerCase();
    switch (ext) {
      case 'py':
        return <FileCode className="w-4 h-4 text-emerald-400 shrink-0" />;
      case 'js':
      case 'jsx':
        return <FileCode className="w-4 h-4 text-amber-400 shrink-0" />;
      case 'ts':
      case 'tsx':
        return <FileCode className="w-4 h-4 text-accent-blue shrink-0" />;
      case 'java':
        return <FileCode className="w-4 h-4 text-orange-500 shrink-0" />;
      case 'cpp':
      case 'h':
      case 'c':
        return <FileCode className="w-4 h-4 text-blue-400 shrink-0" />;
      case 'rs':
        return <FileCode className="w-4 h-4 text-amber-600 shrink-0" />;
      case 'go':
        return <FileCode className="w-4 h-4 text-cyan-400 shrink-0" />;
      case 'sh':
        return <FileCode className="w-4 h-4 text-indigo-400 shrink-0" />;
      default:
        return <File className="w-4 h-4 text-ide-muted shrink-0" />;
    }
  };

  return (
    <div className="flex flex-col select-none font-sans">
      <div
        onClick={handleToggle}
        onMouseEnter={() => setIsHovered(true)}
        onMouseLeave={() => setIsHovered(false)}
        style={{ paddingLeft }}
        className={`h-7 flex items-center justify-between pr-2 cursor-pointer transition-colors text-xs select-none ${
          isActive
            ? 'bg-accent-blue/15 text-ide-text border-l-2 border-l-accent-blue font-medium'
            : 'text-ide-text hover:bg-ide-panel/40'
        }`}
      >
        <div className="flex items-center gap-1.5 min-w-0 flex-1 h-full">
          {/* Chevron for folder expansion */}
          {isFolder ? (
            <span className="text-ide-muted">
              {isExpanded ? (
                <ChevronDown className="w-3.5 h-3.5 shrink-0" />
              ) : (
                <ChevronRight className="w-3.5 h-3.5 shrink-0" />
              )}
            </span>
          ) : (
            <span className="w-3.5" /> // spacer
          )}

          {/* Type icon */}
          {isFolder ? (
            isExpanded ? (
              <FolderOpen className="w-4 h-4 text-amber-500 shrink-0" />
            ) : (
              <Folder className="w-4 h-4 text-amber-500 shrink-0" />
            )
          ) : (
            getFileIcon(node.name)
          )}

          {/* Name label */}
          {isEditing ? (
            <form onSubmit={handleRenameSubmit} className="flex-1" onClick={(e) => e.stopPropagation()}>
              <input
                type="text"
                autoFocus
                value={editName}
                onChange={(e) => setEditName(e.target.value)}
                onBlur={handleRenameSubmit}
                onKeyDown={handleKeyDown}
                className="w-full bg-ide-bg text-ide-text border border-accent-blue px-1.5 py-0.5 rounded text-[11px] focus:outline-none"
              />
            </form>
          ) : (
            <span className="truncate text-ide-text hover:text-ide-text transition-colors">{node.name}</span>
          )}
        </div>

        {/* Hover Controls */}
        {isHovered && !isEditing && (
          <div className="flex items-center gap-1 select-none shrink-0" onClick={(e) => e.stopPropagation()}>
            {isFolder && (
              <>
                <button
                  onClick={() => onCreateFile(node.path)}
                  title="New File"
                  className="p-0.5 rounded hover:bg-ide-border text-ide-muted hover:text-ide-text transition-colors"
                >
                  <FilePlus className="w-3 h-3" />
                </button>
                <button
                  onClick={() => onCreateFolder(node.path)}
                  title="New Folder"
                  className="p-0.5 rounded hover:bg-ide-border text-ide-muted hover:text-ide-text transition-colors"
                >
                  <FolderPlus className="w-3 h-3" />
                </button>
              </>
            )}
            <button
              onClick={() => setIsEditing(true)}
              title="Rename"
              className="p-0.5 rounded hover:bg-ide-border text-ide-muted hover:text-ide-text transition-colors"
            >
              <Edit className="w-3.5 h-3.5" />
            </button>
            <button
              onClick={() => onDelete(node.path)}
              title="Delete"
              className="p-0.5 rounded hover:bg-ide-border text-ide-muted hover:text-rose-400 transition-colors"
            >
              <Trash2 className="w-3.5 h-3.5" />
            </button>
          </div>
        )}
      </div>

      {/* Children list */}
      {isFolder && isExpanded && node.children && (
        <div className="flex flex-col">
          {node.children.map((child) => (
            <FileItem
              key={child.path}
              node={child}
              activeFile={activeFile}
              onFileClick={onFileClick}
              onDelete={onDelete}
              onRename={onRename}
              onCreateFile={onCreateFile}
              onCreateFolder={onCreateFolder}
              level={level + 1}
            />
          ))}
        </div>
      )}
    </div>
  );
}
