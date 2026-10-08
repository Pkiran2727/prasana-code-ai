import React, { useEffect } from 'react';
import Editor from '@monaco-editor/react';
import { Loader2 } from 'lucide-react';
import { saveFileContent } from '../../api/agentApi';

export default function MonacoEditor({
  sessionId,
  filePath,
  content,
  language,
  isDirty,
  onChange,
  onSaved,
  readOnly = false
}) {
  // Map our app's language code to Monaco language ids
  const getMonacoLanguage = (lang) => {
    const mapping = {
      python: 'python',
      javascript: 'javascript',
      typescript: 'typescript',
      java: 'java',
      cpp: 'cpp',
      c: 'c',
      go: 'go',
      rust: 'rust',
      bash: 'shell',
    };
    return mapping[lang] || 'plaintext';
  };

  // Debounced auto-save effect
  useEffect(() => {
    if (!sessionId || !filePath || !isDirty || readOnly) return;

    const saveTimer = setTimeout(async () => {
      try {
        await saveFileContent(sessionId, filePath, content);
        if (onSaved) onSaved();
      } catch (err) {
        console.error(`Auto-save error for ${filePath}:`, err);
      }
    }, 500);

    return () => clearTimeout(saveTimer);
  }, [content, filePath, sessionId, isDirty, readOnly, onSaved]);

  const handleEditorChange = (value) => {
    if (onChange) {
      onChange(value);
    }
  };

  const editorOptions = {
    minimap: { enabled: true },
    fontSize: 14,
    fontFamily: "'Fira Code', 'JetBrains Mono', Consolas, monospace",
    fontLigatures: true,
    cursorBlinking: 'blink',
    cursorSmoothCaretAnimation: 'on',
    smoothScrolling: true,
    padding: { top: 8, bottom: 8 },
    readOnly: readOnly,
    automaticLayout: true,
    scrollBeyondLastLine: false,
    lineNumbersMinChars: 3,
    renderLineHighlight: 'all',
    scrollbar: {
      verticalScrollbarSize: 8,
      horizontalScrollbarSize: 8,
      vertical: 'visible',
      horizontal: 'visible',
    },
  };

  if (!filePath) {
    return (
      <div className="flex-1 flex flex-col items-center justify-center text-ide-muted bg-ide-panel select-none font-sans gap-2 p-6">
        <div className="w-12 h-12 rounded-full border border-ide-border flex items-center justify-center bg-ide-sidebar">
          <span className="text-xl">📄</span>
        </div>
        <p className="text-sm font-medium text-ide-text">No active file</p>
        <p className="text-xs text-center max-w-[200px]">
          Select a file from the explorer or create a new one to begin editing.
        </p>
      </div>
    );
  }

  return (
    <div className="flex-1 w-full h-full relative overflow-hidden bg-ide-panel">
      {/* Auto-save premium visual status badge */}
      {isDirty ? (
        <div className="absolute top-2 right-4 z-10 px-2 py-0.5 text-[9px] font-semibold tracking-wider uppercase rounded bg-accent-blue/20 text-accent-blue font-sans animate-pulse select-none pointer-events-none">
          Saving...
        </div>
      ) : (
        <div className="absolute top-2 right-4 z-10 px-2 py-0.5 text-[9px] font-semibold tracking-wider uppercase rounded bg-ide-border/50 text-ide-muted font-sans select-none pointer-events-none transition-opacity duration-300">
          Saved
        </div>
      )}

      <Editor
        height="100%"
        width="100%"
        path={filePath}
        language={getMonacoLanguage(language)}
        value={content}
        theme="vs-dark"
        options={editorOptions}
        onChange={handleEditorChange}
        loading={
          <div className="absolute inset-0 flex items-center justify-center bg-ide-panel">
            <Loader2 className="w-8 h-8 animate-spin text-accent-blue" />
          </div>
        }
      />
    </div>
  );
}
