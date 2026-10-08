import React, { useState, useEffect } from 'react';
import { X, Flame, Gem, Zap, Sparkles, Bug, Play, CheckCircle2, RotateCcw, ChevronDown, ChevronUp, Lock } from 'lucide-react';
import MonacoEditor from '../editor/MonacoEditor';
import ChatPanel from '../chat/ChatPanel';
import { API_BASE_URL } from '../../api/agentApi';

export default function InteractiveLessonView({
  lesson,
  sessionId,
  userStats,
  onClose,
  onOpenPricing,
  onSendMessage,
  messages,
  agentStatus,
  agentCurrentFile,
  isStreaming,
  onClearHistory,
  onStopAgent
}) {
  const [code, setCode] = useState(
    lesson?.starterCode || 
    `n1 = int(input()) # Don't change this line\nn2 = int(input()) # Don't change this line\nop = input() # Don't change this line\nresult = 0\n\n# Your code here\nif op == '+':\n    result = n1 + n2\nelif op == '-':\n    result = n1 - n2\nelif op == '*':\n    result = n1 * n2\nelif op == '/':\n    result = n1 / n2\n\nprint(f"result = {result}")`
  );

  const [activeTab, setActiveTab] = useState('testcases');
  const [selectedTestCase, setSelectedTestCase] = useState(0);
  const [isRunning, setIsRunning] = useState(false);
  const [energy, setEnergy] = useState(1); // 1 free energy unit left
  const [showEnergyModal, setShowEnergyModal] = useState(false);
  const [showHint, setShowHint] = useState(false);
  const [countdownMinutes, setCountdownMinutes] = useState(20);
  const [countdownSeconds, setCountdownSeconds] = useState(15);

  const [testResults, setTestResults] = useState([
    { id: 1, input: "12\n34\n+", output: "", expected: "result = 46\n", status: 'idle' },
    { id: 2, input: "50\n20\n-", output: "", expected: "result = 30\n", status: 'idle' },
    { id: 3, input: "6\n7\n*", output: "", expected: "result = 42\n", status: 'idle' },
    { id: 4, input: "100\n4\n/", output: "", expected: "result = 25.0\n", status: 'idle' }
  ]);

  // Renewal Countdown Timer
  useEffect(() => {
    const timer = setInterval(() => {
      setCountdownSeconds(prev => {
        if (prev === 0) {
          if (countdownMinutes === 0) return 0;
          setCountdownMinutes(m => m - 1);
          return 59;
        }
        return prev - 1;
      });
    }, 1000);
    return () => clearInterval(timer);
  }, [countdownMinutes]);

  const handleRunCode = async () => {
    if (energy <= 0) {
      setShowEnergyModal(true);
      return;
    }

    setIsRunning(true);
    setEnergy(prev => Math.max(0, prev - 1));

    try {
      const res = await fetch(`${API_BASE_URL}/api/verify-solution`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          session_id: sessionId || 'default_session',
          code: code,
          language: 'python',
          expected_output: testResults[selectedTestCase].expected
        })
      });
      const data = await res.json();
      
      setTestResults(prev => {
        const updated = [...prev];
        updated[selectedTestCase] = {
          ...updated[selectedTestCase],
          output: data.actual_output || data.stderr || 'No output',
          status: data.passed ? 'passed' : 'failed'
        };
        return updated;
      });
    } catch (err) {
      console.error('Run code error:', err);
    } finally {
      setIsRunning(false);
    }
  };

  const handleAskAI = (promptText) => {
    setActiveTab('ai');
    onSendMessage(promptText || `Can you analyze my code and give me a hint on line error? Do not spoil the full answer.`);
  };

  return (
    <div className="fixed inset-0 z-50 w-screen h-screen bg-ide-bg text-ide-text flex flex-col font-sans select-none overflow-hidden relative">
      {/* Energy Renewal Modal Overlay */}
      {showEnergyModal && (
        <div className="absolute inset-0 z-50 bg-black/80 backdrop-blur-md flex items-center justify-center p-4">
          <div className="w-full max-w-md bg-ide-panel border border-emerald-500/30 rounded-3xl p-8 text-center shadow-2xl relative">
            <button
              onClick={() => setShowEnergyModal(false)}
              className="absolute top-4 right-4 p-2 text-ide-muted hover:text-ide-text"
            >
              <X className="w-5 h-5" />
            </button>

            <div className="w-16 h-16 rounded-2xl bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center text-emerald-400 mx-auto mb-4 text-3xl">
              ⚡
            </div>

            <h2 className="text-2xl font-bold mb-2 text-ide-text">Energy Refill Needed</h2>
            <p className="text-ide-muted text-xs leading-relaxed mb-6 font-normal">
              Upgrade to <strong className="text-emerald-400 font-semibold">PRO</strong> for learning with unlimited energy, priority AI Tutor coaching, and verified certificates!
            </p>

            <button
              onClick={() => {
                setShowEnergyModal(false);
                onOpenPricing();
              }}
              className="w-full py-4 rounded-2xl bg-gradient-to-r from-emerald-400 via-teal-400 to-emerald-300 hover:from-emerald-300 hover:to-teal-300 text-slate-950 font-bold text-xs shadow-md shadow-emerald-500/20 active:scale-95 transition-all mb-6 uppercase tracking-wider"
            >
              Become Pro
            </button>

            <div className="border-t border-ide-border pt-4 text-xs text-ide-muted font-normal">
              Wait for next energy renewal: <strong className="text-emerald-400 font-mono">{String(countdownMinutes).padStart(2, '0')}:{String(countdownSeconds).padStart(2, '0')}</strong>
            </div>
          </div>
        </div>
      )}

      {/* Top Header Navigation Bar */}
      <header className="h-14 bg-ide-panel/90 border-b border-ide-border px-6 flex items-center justify-between shrink-0">
        <div className="flex items-center gap-4">
          <button
            onClick={onClose}
            className="p-1.5 rounded-xl bg-ide-sidebar hover:bg-slate-700 text-ide-muted hover:text-ide-text transition-all"
          >
            <X className="w-5 h-5" />
          </button>
          <span className="font-semibold text-sm text-ide-text">
            {lesson?.title || 'Decision Making'}
          </span>
        </div>

        {/* Gamification Stats Header Badges */}
        <div className="flex items-center gap-4 text-xs font-semibold">
          <div className="flex items-center gap-1.5 text-rose-400 bg-rose-500/10 border border-rose-500/20 px-3 py-1 rounded-full">
            <Flame className="w-3.5 h-3.5 fill-rose-400" />
            <span>{userStats?.streak || 2}</span>
          </div>

          <div className="flex items-center gap-1.5 text-emerald-400 bg-emerald-500/10 border border-emerald-500/20 px-3 py-1 rounded-full">
            <Gem className="w-3.5 h-3.5 text-emerald-400 fill-emerald-400" />
            <span>{userStats?.xp || 76} XP</span>
          </div>

          <div className="flex items-center gap-1.5 text-teal-300 bg-teal-500/10 border border-teal-500/20 px-3 py-1 rounded-full">
            <Zap className="w-3.5 h-3.5 text-teal-300 fill-teal-300" />
            <span>{energy}</span>
          </div>
        </div>
      </header>

      {/* Main Split Area */}
      <div className="flex-1 flex overflow-hidden">
        {/* Left Panel: Instructions */}
        <div className="w-1/2 p-8 border-r border-ide-border/80 overflow-y-auto bg-ide-bg">
          <div className="max-w-xl">
            <h1 className="text-3xl font-bold tracking-tight mb-4 text-ide-text">
              {lesson?.title || 'Recap - Simple Calculator'}
            </h1>

            <div className="flex items-center gap-2 mb-6">
              <span className="flex items-center gap-1 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-bold">
                <Sparkles className="w-3.5 h-3.5" />
                <span>Challenge</span>
              </span>
              <span className="px-3 py-1 rounded-full bg-teal-500/10 border border-teal-500/20 text-teal-300 text-xs font-bold">
                Beginner
              </span>
            </div>

            <div className="text-ide-text text-sm leading-relaxed space-y-4">
              <p>
                {lesson?.instructions || "You are given a code which gets as input two numbers n1 and n2 and a character op."}
              </p>

              <div className="p-4 rounded-2xl bg-ide-panel border border-ide-border space-y-2 text-xs">
                <p className="font-bold text-ide-text">The possible values for <code className="bg-ide-sidebar px-1.5 py-0.5 rounded text-emerald-400">'op'</code> are:</p>
                <div className="flex gap-2">
                  {["'+'", "'-'", "'/'", "'*'"].map((op, idx) => (
                    <code key={idx} className="bg-ide-sidebar border border-ide-border px-2 py-1 rounded text-emerald-400 font-mono font-bold">
                      {op}
                    </code>
                  ))}
                </div>
              </div>

              <button
                onClick={() => handleAskAI('Explain the challenge concept to me in simple terms.')}
                className="flex items-center gap-2 px-4 py-2 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 hover:bg-emerald-500/20 text-xs font-bold transition-all"
              >
                <Sparkles className="w-4 h-4" />
                <span>Explain Challenge</span>
              </button>

              {/* Hints Accordion */}
              <div className="mt-6 border-t border-ide-border pt-6">
                <h3 className="text-sm font-bold text-ide-text mb-3 flex items-center gap-2">
                  <span>🎯 Hints</span>
                </h3>
                <div className="border border-ide-border rounded-2xl overflow-hidden bg-ide-panel">
                  <button
                    onClick={() => setShowHint(!showHint)}
                    className="w-full p-4 flex items-center justify-between text-xs font-bold text-ide-text hover:bg-ide-sidebar/50 transition-colors"
                  >
                    <span>Hint 1</span>
                    {showHint ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
                  </button>
                  {showHint && (
                    <div className="p-4 pt-0 text-xs text-teal-300 border-t border-ide-border/60 leading-relaxed">
                      {lesson?.hint || "Use standard if / elif statements to test if op == '+', op == '-', op == '*', op == '/'."}
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Right Panel: Editor & Test Cases */}
        <div className="w-1/2 flex flex-col bg-ide-sidebar">
          {/* Top Half: Code Editor */}
          <div className="h-3/5 flex flex-col border-b border-ide-border">
            <div className="h-10 bg-ide-panel border-b border-ide-border px-4 flex items-center justify-between text-xs text-ide-muted">
              <span className="font-bold text-ide-text">Python 3</span>
              <div className="flex items-center gap-3">
                <RotateCcw className="w-4 h-4 cursor-pointer hover:text-ide-text" title="Reset Code" onClick={() => setCode(lesson?.starterCode || '')} />
              </div>
            </div>

            <div className="flex-1">
              <MonacoEditor
                sessionId={sessionId}
                filePath="main.py"
                content={code}
                language="python"
                onChange={setCode}
              />
            </div>

            {/* Action Bar */}
            <div className="h-14 bg-ide-panel border-t border-ide-border px-4 flex items-center justify-between">
              <div className="flex items-center gap-2">
                <button
                  onClick={() => handleAskAI('Help me understand where my bug is.')}
                  className="flex items-center gap-1.5 bg-ide-sidebar hover:bg-gray-700 text-emerald-400 border border-ide-border px-3 py-1.5 rounded-xl text-xs font-bold transition-all"
                >
                  <Sparkles className="w-3.5 h-3.5 text-emerald-400" />
                  <span>Ask AI</span>
                </button>

                <button
                  onClick={() => handleAskAI('Debug line error in my python code.')}
                  className="flex items-center gap-1.5 bg-ide-sidebar hover:bg-gray-700 text-teal-300 border border-ide-border px-3 py-1.5 rounded-xl text-xs font-bold transition-all"
                >
                  <Bug className="w-3.5 h-3.5 text-teal-300" />
                  <span>Debug</span>
                </button>
              </div>

              <button
                onClick={handleRunCode}
                disabled={isRunning}
                className="flex items-center gap-2 bg-gradient-to-r from-emerald-400 to-teal-400 hover:from-emerald-300 hover:to-teal-300 text-slate-950 font-bold text-xs px-5 py-2 rounded-xl transition-all shadow-lg shadow-emerald-500/20 active:scale-95"
              >
                <Play className="w-4 h-4 fill-slate-950" />
                <span>{isRunning ? 'Running...' : 'Run Code'}</span>
              </button>
            </div>
          </div>

          {/* Bottom Half: Test Cases or AI Tutor */}
          <div className="h-2/5 flex flex-col bg-ide-panel">
            <div className="h-10 bg-ide-panel border-b border-ide-border px-4 flex items-center justify-between text-xs font-bold">
              <div className="flex gap-4">
                <button
                  onClick={() => setActiveTab('testcases')}
                  className={`py-2 border-b-2 transition-all ${
                    activeTab === 'testcases' ? 'border-emerald-400 text-emerald-400' : 'border-transparent text-ide-muted hover:text-ide-text'
                  }`}
                >
                  TEST CASES
                </button>
                <button
                  onClick={() => setActiveTab('ai')}
                  className={`py-2 border-b-2 transition-all ${
                    activeTab === 'ai' ? 'border-emerald-400 text-emerald-400' : 'border-transparent text-ide-muted hover:text-ide-text'
                  }`}
                >
                  PRASANA AI TUTOR
                </button>
              </div>
            </div>

            <div className="flex-1 overflow-y-auto p-4">
              {activeTab === 'testcases' ? (
                <div className="flex h-full gap-4">
                  <div className="w-1/4 border-r border-ide-border space-y-2 pr-3">
                    {testResults.map((tc, idx) => (
                      <button
                        key={tc.id}
                        onClick={() => setSelectedTestCase(idx)}
                        className={`w-full p-2 rounded-xl text-xs font-bold flex items-center justify-between transition-all ${
                          selectedTestCase === idx
                            ? 'bg-ide-sidebar text-ide-text border border-ide-border'
                            : 'text-ide-muted hover:bg-ide-panel'
                        }`}
                      >
                        <span>Test #{tc.id}</span>
                        {tc.status === 'passed' && <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />}
                      </button>
                    ))}
                  </div>

                  <div className="w-3/4 grid grid-cols-3 gap-3 font-mono text-xs">
                    <div>
                      <span className="text-[10px] uppercase font-bold text-ide-muted block mb-1">Input</span>
                      <pre className="p-3 bg-ide-panel rounded-xl border border-ide-border text-ide-text">
                        {testResults[selectedTestCase].input}
                      </pre>
                    </div>

                    <div>
                      <span className="text-[10px] uppercase font-bold text-ide-muted block mb-1">Actual Output</span>
                      <pre className="p-3 bg-ide-panel rounded-xl border border-ide-border text-cyan-300">
                        {testResults[selectedTestCase].output || 'Click "Run Code" to view output'}
                      </pre>
                    </div>

                    <div>
                      <span className="text-[10px] uppercase font-bold text-ide-muted block mb-1">Expected Output</span>
                      <pre className="p-3 bg-ide-panel rounded-xl border border-ide-border text-emerald-400">
                        {testResults[selectedTestCase].expected}
                      </pre>
                    </div>
                  </div>
                </div>
              ) : (
                <ChatPanel
                  messages={messages}
                  onSendMessage={onSendMessage}
                  agentStatus={agentStatus}
                  agentCurrentFile={agentCurrentFile}
                  isStreaming={isStreaming}
                  onClearHistory={onClearHistory}
                  onStopAgent={onStopAgent}
                />
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
