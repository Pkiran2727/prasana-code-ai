import React, { useEffect, useRef } from 'react';
import { Bot, RefreshCw, Loader2, Square } from 'lucide-react';
import ChatMessage from './ChatMessage';
import ChatInput from './ChatInput';

export default function ChatPanel({
  messages,
  onSendMessage,
  agentStatus,
  agentCurrentFile,
  isStreaming,
  onClearHistory,
  onStopAgent,
}) {
  const chatEndRef = useRef(null);

  // Auto-scroll to bottom of chat
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, agentStatus]);

  // Translate status keyword to human text
  const getStatusText = () => {
    if (!agentStatus) return null;
    switch (agentStatus) {
      case 'reading':
        return `Reading ${agentCurrentFile || 'file'}...`;
      case 'writing':
        return `Updating ${agentCurrentFile || 'file'}...`;
      case 'running':
        return `Executing code...`;
      case 'searching':
        return `Searching code...`;
      default:
        return 'Thinking...';
    }
  };

  return (
    <div className="flex-grow flex flex-col overflow-hidden h-full bg-ide-sidebar font-sans select-none">
      {/* Panel Header */}
      <div className="h-9 px-3 border-b border-ide-border flex items-center justify-between text-xs font-bold text-ide-muted tracking-wider uppercase shrink-0">
        <span className="flex items-center gap-1.5">
          <Bot className="w-4 h-4 text-purple-400" />
          AI Agent Chat
        </span>
        {messages.length > 0 && (
          <button
            onClick={onClearHistory}
            title="Reset Conversation"
            className="p-1 rounded hover:bg-ide-border text-ide-muted hover:text-ide-text transition-colors"
          >
            <RefreshCw className="w-3.5 h-3.5" />
          </button>
        )}
      </div>

      {/* Messages area */}
      <div className="flex-1 overflow-y-auto p-4 flex flex-col gap-4">
        {messages.length === 0 ? (
          <div className="flex-1 flex flex-col items-center justify-center text-ide-muted text-center p-6 select-none my-auto">
            <div className="w-12 h-12 rounded-full border border-ide-border flex items-center justify-center bg-ide-panel text-xl mb-3 pulsing-glow">
              🤖
            </div>
            <p className="text-sm font-medium text-ide-text mb-1">Meet your AI Coding Agent</p>
            <p className="text-xs max-w-[200px]">
              Ask me to write code, debug, refactor files, or run tests in your workspace.
            </p>
          </div>
        ) : (
          messages.map((msg) => <ChatMessage key={msg.id} message={msg} />)
        )}

        {/* Real-time Agent Status Pill */}
        {agentStatus && (
          <div className="flex items-center gap-2 self-start bg-ide-panel/65 border border-ide-border px-3 py-1.5 rounded-lg text-xs text-ide-text animate-pulse shadow-sm shadow-black/20 select-none">
            <Loader2 className="w-3.5 h-3.5 animate-spin text-purple-400" />
            <span className="font-medium">{getStatusText()}</span>
          </div>
        )}
        <div ref={chatEndRef} />
      </div>

      {/* Chat input with integrated Stop button */}
      <ChatInput onSendMessage={onSendMessage} disabled={isStreaming} onStopAgent={onStopAgent} />
    </div>
  );
}
