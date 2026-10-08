import React from 'react';
import { Eye, FileText, Play, Search, FolderPlus, Trash2, Edit } from 'lucide-react';

export default function ChatMessage({ message }) {
  const isUser = message.sender === 'user';

  // Helper to get tool icons for the execution pills
  const getToolIcon = (toolName) => {
    switch (toolName) {
      case 'read_file':
        return <Eye className="w-3 h-3 text-emerald-400" />;
      case 'write_file':
      case 'create_file':
        return <FileText className="w-3.5 h-3.5 text-blue-400" />;
      case 'delete_file':
        return <Trash2 className="w-3 h-3 text-rose-400" />;
      case 'run_code':
        return <Play className="w-3 h-3 text-amber-400 fill-amber-400/20" />;
      case 'search_code':
        return <Search className="w-3 h-3 text-cyan-400" />;
      case 'create_folder':
        return <FolderPlus className="w-3 h-3 text-amber-500" />;
      default:
        return <Eye className="w-3 h-3 text-ide-muted" />;
    }
  };

  // Simple custom markdown-like renderer (bold, code blocks, backticks)
  const renderMessageContent = (text) => {
    if (!text) return null;

    // Split text by code blocks (```code```)
    const codeBlockRegex = /```(\w*)\n([\s\S]*?)```/g;
    const parts = [];
    let lastIndex = 0;
    let match;

    while ((match = codeBlockRegex.exec(text)) !== null) {
      const textBefore = text.slice(lastIndex, match.index);
      if (textBefore) {
        parts.push({ type: 'text', content: textBefore });
      }

      parts.push({
        type: 'code_block',
        language: match[1] || 'code',
        content: match[2],
      });

      lastIndex = codeBlockRegex.lastIndex;
    }

    const remainingText = text.slice(lastIndex);
    if (remainingText) {
      parts.push({ type: 'text', content: remainingText });
    }

    return parts.map((part, index) => {
      if (part.type === 'code_block') {
        return (
          <div key={index} className="my-3 rounded overflow-hidden border border-ide-border bg-ide-terminal select-text">
            <div className="bg-ide-navbar text-[10px] text-ide-muted px-3 py-1 font-mono flex justify-between items-center select-none border-b border-ide-border">
              <span>{part.language || 'code'}</span>
              <span className="text-emerald-500 font-semibold">Copy</span>
            </div>
            <pre className="p-3 text-xs overflow-x-auto font-mono text-ide-text select-text leading-relaxed">
              <code>{part.content.trim()}</code>
            </pre>
          </div>
        );
      }

      // Inline code format parsing (`inline code` and **bold**)
      const inlineParts = [];
      const lines = part.content.split('\n');

      return (
        <p key={index} className="text-xs leading-relaxed mb-1.5 whitespace-pre-wrap break-words select-text">
          {lines.map((line, lIdx) => {
            const inlineCodeRegex = /`([^`]+)`|\*\*([^*]+)\*\*/g;
            const segments = [];
            let segmentIdx = 0;
            let m;

            while ((m = inlineCodeRegex.exec(line)) !== null) {
              const textBefore = line.slice(segmentIdx, m.index);
              if (textBefore) {
                segments.push(textBefore);
              }

              if (m[1]) {
                // backtick code
                segments.push(
                  <code key={m.index} className="bg-ide-terminal border border-ide-border px-1.5 py-0.5 rounded text-[11px] font-mono text-accent-yellow mx-0.5">
                    {m[1]}
                  </code>
                );
              } else if (m[2]) {
                // bold text
                segments.push(
                  <strong key={m.index} className="font-bold text-ide-text">
                    {m[2]}
                  </strong>
                );
              }
              segmentIdx = inlineCodeRegex.lastIndex;
            }

            const remainingSegment = line.slice(segmentIdx);
            if (remainingSegment) {
              segments.push(remainingSegment);
            }

            return (
              <span key={lIdx} className="block min-h-[1.2em]">
                {segments}
              </span>
            );
          })}
        </p>
      );
    });
  };

  return (
    <div className={`flex flex-col gap-1.5 max-w-[85%] ${isUser ? 'self-end' : 'self-start'}`}>
      {/* Sender Tag */}
      <span className={`text-[10px] font-bold tracking-wider uppercase px-1 select-none ${isUser ? 'text-accent-blue text-right' : 'text-purple-400 text-left'}`}>
        {isUser ? 'You' : 'LiveCodeAI Agent'}
      </span>

      {/* Bubble container */}
      <div
        className={`rounded-lg px-3.5 py-2.5 border transition-all duration-200 ${
          isUser
            ? 'bg-accent-blue/10 border-accent-blue/20 text-ide-text rounded-tr-none'
            : 'bg-ide-panel/85 border-ide-border text-ide-text rounded-tl-none'
        }`}
      >
        {/* Tool Call Events (if assistant and has tools) */}
        {!isUser && message.tools && message.tools.length > 0 && (
          <div className="flex flex-wrap gap-1.5 mb-2.5 select-none border-b border-ide-border/40 pb-2">
            {message.tools.map((t, idx) => (
              <div
                key={idx}
                className="flex items-center gap-1.5 bg-ide-sidebar border border-ide-border px-2 py-1 rounded text-[10px] font-semibold text-ide-muted"
              >
                {getToolIcon(t.name)}
                <span className="font-mono text-ide-text">{t.name}</span>
                {t.path && <span className="text-[9px] text-ide-muted truncate max-w-[80px]">({t.path})</span>}
                <span className="text-[9px] text-emerald-400 font-bold ml-0.5">✓</span>
              </div>
            ))}
          </div>
        )}

        {/* Text body */}
        <div>{renderMessageContent(message.text)}</div>
      </div>
    </div>
  );
}
