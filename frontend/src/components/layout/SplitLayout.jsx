import React, { useState, useRef, useEffect } from 'react';

export default function SplitLayout({ left, editor, terminal, right }) {
  const [fileTreeWidth, setFileTreeWidth] = useState(220);
  const [chatWidth, setChatWidth] = useState(320);
  const [terminalHeight, setTerminalHeight] = useState(220);

  const containerRef = useRef(null);
  const isDraggingFileTree = useRef(false);
  const isDraggingChat = useRef(false);
  const isDraggingTerminal = useRef(false);

  // Resize boundaries
  const minFileTreeWidth = 160;
  const maxFileTreeWidth = 400;
  const minChatWidth = 260;
  const maxChatWidth = 500;
  const minTerminalHeight = 120;
  const maxTerminalHeight = 500;

  useEffect(() => {
    const handleMouseMove = (e) => {
      if (!containerRef.current) return;
      const containerRect = containerRef.current.getBoundingClientRect();

      if (isDraggingFileTree.current) {
        const newWidth = e.clientX - containerRect.left;
        if (newWidth >= minFileTreeWidth && newWidth <= maxFileTreeWidth) {
          setFileTreeWidth(newWidth);
        }
      }

      if (isDraggingChat.current) {
        const newWidth = containerRect.right - e.clientX;
        if (newWidth >= minChatWidth && newWidth <= maxChatWidth) {
          setChatWidth(newWidth);
        }
      }

      if (isDraggingTerminal.current) {
        const editorAreaHeight = containerRect.height;
        // Since terminal is at the bottom of the editor section, we calculate height from bottom
        const newHeight = containerRect.bottom - e.clientY;
        if (newHeight >= minTerminalHeight && newHeight <= maxTerminalHeight) {
          setTerminalHeight(newHeight);
        }
      }
    };

    const handleMouseUp = () => {
      isDraggingFileTree.current = false;
      isDraggingChat.current = false;
      isDraggingTerminal.current = false;
      document.body.classList.remove('select-none', 'cursor-col-resize', 'cursor-row-resize');
    };

    window.addEventListener('mousemove', handleMouseMove);
    window.addEventListener('mouseup', handleMouseUp);

    return () => {
      window.removeEventListener('mousemove', handleMouseMove);
      window.removeEventListener('mouseup', handleMouseUp);
    };
  }, []);

  const startResizeFileTree = (e) => {
    e.preventDefault();
    isDraggingFileTree.current = true;
    document.body.classList.add('select-none', 'cursor-col-resize');
  };

  const startResizeChat = (e) => {
    e.preventDefault();
    isDraggingChat.current = true;
    document.body.classList.add('select-none', 'cursor-col-resize');
  };

  const startResizeTerminal = (e) => {
    e.preventDefault();
    isDraggingTerminal.current = true;
    document.body.classList.add('select-none', 'cursor-row-resize');
  };

  return (
    <div
      ref={containerRef}
      className="flex-1 flex overflow-hidden w-full bg-ide-bg border-t border-ide-border relative"
    >
      {/* 1. Left Panel: File Tree */}
      <div
        style={{ width: `${fileTreeWidth}px` }}
        className="h-full bg-ide-sidebar border-r border-ide-border flex flex-col shrink-0 overflow-hidden"
      >
        {left}
      </div>

      {/* Resize Bar 1: File Tree Divider */}
      <div
        onMouseDown={startResizeFileTree}
        className="w-1 hover:w-1.5 h-full bg-transparent hover:bg-accent-blue/55 cursor-col-resize transition-colors shrink-0 z-10"
      />

      {/* 2. Middle Panel: Editor & Terminal */}
      <div className="flex-1 flex flex-col h-full overflow-hidden min-w-[300px]">
        {/* Editor Area */}
        <div className="flex-1 min-h-[100px] flex flex-col overflow-hidden bg-ide-panel">
          {editor}
        </div>

        {/* Resize Bar 2: Terminal Divider */}
        <div
          onMouseDown={startResizeTerminal}
          className="h-1 hover:h-1.5 w-full bg-transparent hover:bg-accent-blue/55 cursor-row-resize transition-colors shrink-0 z-10"
        />

        {/* Terminal Area */}
        <div
          style={{ height: `${terminalHeight}px` }}
          className="bg-ide-terminal border-t border-ide-border flex flex-col shrink-0 overflow-hidden"
        >
          {terminal}
        </div>
      </div>

      {/* Resize Bar 3: Chat Panel Divider */}
      <div
        onMouseDown={startResizeChat}
        className="w-1 hover:w-1.5 h-full bg-transparent hover:bg-accent-blue/55 cursor-col-resize transition-colors shrink-0 z-10"
      />

      {/* 3. Right Panel: Chat Panel */}
      <div
        style={{ width: `${chatWidth}px` }}
        className="h-full bg-ide-sidebar border-l border-ide-border flex flex-col shrink-0 overflow-hidden"
      >
        {right}
      </div>
    </div>
  );
}
