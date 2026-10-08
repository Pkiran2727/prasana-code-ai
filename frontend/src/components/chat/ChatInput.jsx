import React, { useState, useRef } from 'react';
import { Send, Square } from 'lucide-react';

export default function ChatInput({ onSendMessage, disabled, onStopAgent }) {
  const [inputValue, setInputValue] = useState('');
  const textareaRef = useRef(null);

  const handleSubmit = (e) => {
    if (e) e.preventDefault();
    if (inputValue.trim() && !disabled) {
      onSendMessage(inputValue.trim());
      setInputValue('');
      if (textareaRef.current) {
        textareaRef.current.style.height = 'auto';
      }
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  const handleInput = (e) => {
    const textarea = e.target;
    textarea.style.height = 'auto';
    textarea.style.height = `${Math.min(textarea.scrollHeight, 120)}px`;
  };

  return (
    <form onSubmit={handleSubmit} className="p-3 border-t border-ide-border bg-ide-sidebar select-none shrink-0 flex items-end gap-2">
      <div className="flex-1 bg-ide-panel border border-ide-border rounded-lg focus-within:border-accent-blue transition-colors relative overflow-hidden flex items-end">
        <textarea
          ref={textareaRef}
          rows={1}
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyDown={handleKeyDown}
          onInput={handleInput}
          placeholder="Ask the agent... (e.g., 'write python bubble sort')"
          disabled={disabled}
          className="flex-1 bg-transparent text-ide-text px-3 py-2.5 max-h-[120px] resize-none outline-none text-xs leading-normal placeholder-ide-muted disabled:opacity-50 select-text"
        />
      </div>
      {disabled && onStopAgent ? (
        <button
          type="button"
          onClick={onStopAgent}
          title="Stop Agent"
          className="h-[36px] px-3 rounded-lg bg-red-600 hover:bg-red-500 text-ide-text text-xs font-semibold flex items-center gap-1.5 transition-all shadow-md shrink-0"
        >
          <Square className="w-3.5 h-3.5 fill-white" />
          Stop
        </button>
      ) : (
        <button
          type="submit"
          disabled={!inputValue.trim() || disabled}
          className="h-[36px] w-[36px] rounded-lg bg-accent-blue hover:bg-accent-blue-hover disabled:bg-ide-border text-ide-text disabled:text-ide-muted flex items-center justify-center transition-all shadow-md shadow-accent-blue/10 shrink-0"
        >
          <Send className="w-4 h-4" />
        </button>
      )}
    </form>
  );
}
