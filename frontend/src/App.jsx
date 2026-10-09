import React, { useState, useEffect, useRef } from 'react';
import Navbar from './components/layout/Navbar';
import SplitLayout from './components/layout/SplitLayout';
import FileTree from './components/filetree/FileTree';
import EditorTabs from './components/editor/EditorTabs';
import MonacoEditor from './components/editor/MonacoEditor';
import Terminal from './components/terminal/Terminal';
import ChatPanel from './components/chat/ChatPanel';
import LoginScreen from './components/auth/LoginScreen';
import AdminMonitor from './components/admin/AdminMonitor';

import LandingHome from './components/views/LandingHome';
import JourneysCatalog from './components/views/JourneysCatalog';
import PracticeCatalog from './components/views/PracticeCatalog';
import PricingView from './components/views/PricingView';
import InteractiveLessonView from './components/views/InteractiveLessonView';
import GamifiedJourneyMap from './components/views/GamifiedJourneyMap';

import {
  createSessionApi,
  destroySessionApi,
  fetchFileTree,
  readFileContent,
  saveFileContent,
  createFileNode,
  deleteFileNode,
  runCodeApi,
  getWebSocketUrl,
  logoutApi,
  pingEngagementApi
} from './api/agentApi';

export default function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(!!localStorage.getItem("access_token"));
  const [userRole, setUserRole] = useState(localStorage.getItem("user_role") || "user");
  const [showMonitor, setShowMonitor] = useState(false);
  const [showLoginModal, setShowLoginModal] = useState(false);
  const [activeLesson, setActiveLesson] = useState(null);
  const [userStats, setUserStats] = useState({ xp: 75, streak: 2 });
  const [activeTab, setActiveTab] = useState('home'); // 'home' | 'journeys' | 'practice' | 'ide' | 'pricing'
  const [sessionId, setSessionId] = useState(null);
  const [selectedLanguage, setSelectedLanguage] = useState('python');
  const [llmStatus, setLlmStatus] = useState('online');
  const [isRunning, setIsRunning] = useState(false);
  
  // File System State
  const [fileStates, setFileStates] = useState({});
  const [fileTree, setFileTree] = useState([]);
  const [openFiles, setOpenFiles] = useState([]);
  const [activeFile, setActiveFile] = useState(null);

  // Chat State
  const [messages, setMessages] = useState([
    {
      id: 'welcome',
      sender: 'assistant',
      text: "Welcome to Prasana Code AI! 🤖\n\nI am **Mitra**, your AI Tutor (by @itsprasana).\n\nAsk me for hints, error line debugging, or code review anytime! Try opening `main.py` or pick a Journey above.",
      tools: []
    }
  ]);
  const [agentStatus, setAgentStatus] = useState(null);
  const [agentCurrentFile, setAgentCurrentFile] = useState(null);
  const [isStreaming, setIsStreaming] = useState(false);

  // Terminal State
  const [terminalLines, setTerminalLines] = useState([
    { type: 'system', text: 'LiveCodeAI workspace environment initialized.' },
    { type: 'system', text: 'Python 3.11 sandbox execution container ready.' }
  ]);

  // WebSocket Connection ref
  const wsRef = useRef(null);

  const handleAgentMessage = (data) => {
    switch (data.type) {
      case 'status':
        setAgentStatus(data.status);
        setAgentCurrentFile(data.file);
        break;

      case 'file_modified':
        setFileStates(prev => {
          if (!prev[data.path]) return prev;
          return {
            ...prev,
            [data.path]: {
              ...prev[data.path],
              content: data.content,
              isDirty: false
            }
          };
        });
        break;

      case 'tool_executed':
        setMessages(prev => {
          const updated = [...prev];
          const lastMsg = updated[updated.length - 1];
          if (lastMsg && lastMsg.sender === 'user') {
            lastMsg.tools = lastMsg.tools || [];
            const exists = lastMsg.tools.some(t => t.name === data.tool && t.path === (data.args.path || ''));
            if (!exists) {
              lastMsg.tools.push({
                name: data.tool,
                path: data.args.path || '',
                status: 'success'
              });
            }
          }
          return updated;
        });

        if (data.tool === 'write_file') {
          const writtenPath = data.args.path;
          const content = data.args.content;
          setFileStates(prev => {
            if (!prev[writtenPath]) {
              return {
                ...prev,
                [writtenPath]: {
                  content: content,
                  language: writtenPath.split('.').pop() === 'py' ? 'python' : 'javascript',
                  isDirty: false
                }
              };
            }
            return {
              ...prev,
              [writtenPath]: {
                ...prev[writtenPath],
                content: content,
                isDirty: false
              }
            };
          });
          refreshTree(sessionId);
        } else if (data.tool === 'run_code') {
          try {
            const runRes = JSON.parse(data.result);
            const cmdRun = data.args.path.endsWith('.py') ? `python ${data.args.path}` : `node ${data.args.path}`;
            setTerminalLines(prev => [
              ...prev,
              { type: 'system', text: `Agent invoked test run command: ${cmdRun}` },
              runRes.stdout ? { type: 'stdout', text: runRes.stdout } : null,
              runRes.stderr ? { type: 'stderr', text: runRes.stderr } : null,
              { type: 'system', text: `Agent invocation completed (Exit Code ${runRes.exit_code})` }
            ].filter(Boolean));
          } catch (e) {
            console.error("Failed to parse agent run result:", e);
          }
        }
        break;

      case 'final_answer':
        setAgentStatus(null);
        setAgentCurrentFile(null);
        setIsStreaming(false);
        
        const aiMsg = {
          id: `ai-${Date.now()}`,
          sender: 'assistant',
          text: data.text,
          tools: []
        };
        setMessages(prev => [...prev, aiMsg]);
        break;

      case 'agent_stopped':
        setAgentStatus(null);
        setAgentCurrentFile(null);
        setIsStreaming(false);
        setMessages(prev => [...prev, {
          id: `stopped-${Date.now()}`,
          sender: 'assistant',
          text: '⛔ Agent execution was stopped.',
          tools: []
        }]);
        break;

      default:
        break;
    }
  };

  useEffect(() => {
    if (!sessionId) return;

    const wsUrl = getWebSocketUrl(sessionId);
    const socket = new WebSocket(wsUrl);

    socket.onopen = () => {
      console.log("WebSocket connection established with backend agent.");
    };

    socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        handleAgentMessage(data);
      } catch (err) {
        console.error("Failed to parse websocket message:", err);
      }
    };

    socket.onerror = (error) => {
      console.error("WebSocket error:", error);
    };

    socket.onclose = () => {
      console.log("WebSocket connection closed.");
    };

    wsRef.current = socket;

    return () => {
      if (socket) {
        socket.close();
      }
    };
  }, [sessionId]);

  // 1. Session Bootstrap on Authentication
  useEffect(() => {
    if (!isAuthenticated) return;
    let activeSessionId = null;

    async function initSession() {
      try {
        setTerminalLines(prev => [...prev, { type: 'system', text: 'Creating backend session sandbox...' }]);
        const id = await createSessionApi();
        activeSessionId = id;
        setSessionId(id);
        
        setTerminalLines(prev => [
          ...prev, 
          { type: 'system', text: `Session created: ${id}` }
        ]);

        // Load initial files tree
        const tree = await fetchFileTree(id);
        setFileTree(tree);

        // Load default main.py contents
        const mainFileData = await readFileContent(id, 'main.py');
        setFileStates({
          'main.py': {
            content: mainFileData.content,
            language: mainFileData.language,
            isDirty: false
          }
        });
        setOpenFiles(['main.py']);
        setActiveFile('main.py');
        setSelectedLanguage(mainFileData.language);
      } catch (err) {
        console.error(err);
        setTerminalLines(prev => [
          ...prev,
          { type: 'stderr', text: `Failed to initialize session: ${err.message}` }
        ]);
      }
    }

    initSession();

    // Cleanup session when window closed or refreshed
    return () => {
      if (activeSessionId) {
        destroySessionApi(activeSessionId).catch(err => console.error("Error destroying session:", err));
      }
    };
  }, [isAuthenticated]);

  // 2. User Engagement Heartbeat Ping
  useEffect(() => {
    if (!isAuthenticated || !sessionId) return;
    
    // Heartbeat immediately, then every 30s
    pingEngagementApi(sessionId).catch(e => console.error("Heartbeat ping failed", e));
    const interval = setInterval(() => {
      pingEngagementApi(sessionId).catch(e => console.error("Heartbeat ping failed", e));
    }, 30000);
    
    return () => clearInterval(interval);
  }, [isAuthenticated, sessionId]);

  const handleLogout = () => {
    logoutApi();
    setSessionId(null);
    setFileStates({});
    setFileTree([]);
    setOpenFiles([]);
    setActiveFile(null);
    setIsAuthenticated(false);
    setUserRole("user");
    setShowMonitor(false);
    setTerminalLines([
      { type: 'system', text: 'LiveCodeAI workspace environment initialized.' },
      { type: 'system', text: 'Python 3.11 sandbox execution container ready.' }
    ]);
  };

  // Synchronize language dropdown when changing active files
  useEffect(() => {
    if (activeFile && fileStates[activeFile]) {
      setSelectedLanguage(fileStates[activeFile].language);
    }
  }, [activeFile, fileStates]);

  const refreshTree = async (currSessionId) => {
    try {
      const tree = await fetchFileTree(currSessionId || sessionId);
      setFileTree(tree);
    } catch (err) {
      console.error("Error refreshing file tree:", err);
    }
  };

  // Sync file language when changing via navbar dropdown
  const handleLanguageChange = (newLang) => {
    setSelectedLanguage(newLang);
    if (activeFile && fileStates[activeFile]) {
      setFileStates(prev => ({
        ...prev,
        [activeFile]: {
          ...prev[activeFile],
          language: newLang,
          isDirty: true // Trigger auto-save to write language changes
        }
      }));
    }
  };

  // Run Code Command Execution (Piston API Sandbox)
  const handleRunCode = async () => {
    if (!activeFile || isRunning) return;
    setIsRunning(true);
    
    // Command line representation
    const cmdRun = activeFile.endsWith('.py') ? `python ${activeFile}` : `node ${activeFile}`;
    setTerminalLines(prev => [
      ...prev,
      { type: 'system', text: `$ ${cmdRun}` }
    ]);

    try {
      const result = await runCodeApi(sessionId, activeFile);
      
      const lines = [];
      if (result.stdout) {
        lines.push({ type: 'stdout', text: result.stdout });
      }
      if (result.stderr) {
        lines.push({ type: 'stderr', text: result.stderr });
      }
      
      const exitText = `Process finished with exit code ${result.exit_code}`;
      lines.push({ type: 'system', text: exitText });
      
      setTerminalLines(prev => [...prev, ...lines]);
    } catch (err) {
      setTerminalLines(prev => [
        ...prev,
        { type: 'stderr', text: `Execution failed: ${err.message}` }
      ]);
    } finally {
      setIsRunning(false);
    }
  };

  // Editor Content Edit handler
  const handleEditorChange = (newContent) => {
    if (!activeFile) return;
    setFileStates(prev => ({
      ...prev,
      [activeFile]: {
        ...prev[activeFile],
        content: newContent,
        isDirty: true
      }
    }));
  };

  // File explorer node clicked: fetches real contents from backend
  const handleFileClick = async (path) => {
    try {
      if (!fileStates[path]) {
        // Load content from API
        const data = await readFileContent(sessionId, path);
        setFileStates(prev => ({
          ...prev,
          [path]: {
            content: data.content,
            language: data.language,
            isDirty: false
          }
        }));
      }
      
      setActiveFile(path);
      if (!openFiles.includes(path)) {
        setOpenFiles(prev => [...prev, path]);
      }
    } catch (err) {
      console.error(`Failed to load file content: ${path}`, err);
    }
  };

  // Close active tab
  const handleCloseFile = (path) => {
    const nextOpen = openFiles.filter(f => f !== path);
    setOpenFiles(nextOpen);
    if (activeFile === path) {
      setActiveFile(nextOpen.length > 0 ? nextOpen[nextOpen.length - 1] : null);
    }
  };

  // Rename a file/folder (Implemented via Copy + Delete flow since no direct rename route)
  const handleRenameFile = async (path, newName) => {
    try {
      const parts = path.split('/');
      parts.pop();
      const newPath = [...parts, newName].join('/');

      if (fileStates[path]) {
        const fileContent = fileStates[path].content;
        // 1. Create file at new path
        await createFileNode(sessionId, parts.join('/'), newName, 'file', fileContent);
        // 2. Delete old file path
        await deleteFileNode(sessionId, path);
        
        // 3. Update React States
        setFileStates(prev => {
          const copy = { ...prev };
          copy[newPath] = { ...copy[path], isDirty: false };
          delete copy[path];
          return copy;
        });

        setOpenFiles(prev => prev.map(f => f === path ? newPath : f));
        if (activeFile === path) {
          setActiveFile(newPath);
        }
      } else {
        // Directory renaming
        await createFileNode(sessionId, parts.join('/'), newName, 'directory');
        // Delete old directory
        await deleteFileNode(sessionId, path);
      }

      await refreshTree();
    } catch (err) {
      console.error("Rename failed:", err);
    }
  };

  // Delete a file/folder
  const handleDeleteFile = async (path) => {
    try {
      await deleteFileNode(sessionId, path);
      
      // Clean tabs and states
      setFileStates(prev => {
        const copy = { ...prev };
        delete copy[path];
        return copy;
      });
      setOpenFiles(prev => prev.filter(f => f !== path));
      if (activeFile === path) {
        setActiveFile(openFiles.filter(f => f !== path)[0] || null);
      }

      await refreshTree();
    } catch (err) {
      console.error(`Failed to delete path: ${path}`, err);
    }
  };

  // Create new file
  const handleCreateFile = async (parentPath, fileName) => {
    try {
      const path = parentPath ? `${parentPath}/${fileName}` : fileName;
      const initialContent = `# Code file: ${fileName}\n`;
      const extension = fileName.split('.').pop();
      const language = extension === 'py' ? 'python' : extension === 'js' ? 'javascript' : 'plaintext';

      await createFileNode(sessionId, parentPath, fileName, 'file', initialContent);
      
      setFileStates(prev => ({
        ...prev,
        [path]: {
          content: initialContent,
          language,
          isDirty: false
        }
      }));

      await refreshTree();
      
      // Select and open the new file
      setOpenFiles(prev => [...prev, path]);
      setActiveFile(path);
    } catch (err) {
      console.error("Failed to create file:", err);
    }
  };

  // Create new folder
  const handleCreateFolder = async (parentPath, folderName) => {
    try {
      await createFileNode(sessionId, parentPath, folderName, 'directory');
      await refreshTree();
    } catch (err) {
      console.error("Failed to create folder:", err);
    }
  };

  // Clear Chat History
  const handleClearHistory = () => {
    setMessages([]);
  };

  // Real-time AI Agent loop trigger over WebSocket
  const handleSendMessage = (messageText) => {
    if (!messageText.trim()) return;

    const userMsg = {
      id: `user-${Date.now()}`,
      sender: 'user',
      text: messageText,
      tools: []
    };
    setMessages(prev => [...prev, userMsg]);
    setIsStreaming(true);

    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify({ prompt: messageText }));
    } else {
      setTerminalLines(prev => [
        ...prev,
        { type: 'stderr', text: 'Error: WebSocket not connected. Reconnecting to agent...' }
      ]);
      setIsStreaming(false);
      setAgentStatus(null);
    }
  };

  // Stop agent mid-execution
  const handleStopAgent = () => {
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify({ type: 'stop' }));
    }
    // Immediately clear UI state — don't wait for WS round-trip
    setAgentStatus(null);
    setAgentCurrentFile(null);
    setIsStreaming(false);
    setMessages(prev => [...prev, {
      id: `stopped-${Date.now()}`,
      sender: 'assistant',
      text: '⛔ Agent execution was stopped by you.',
      tools: []
    }]);
  };

  const handleToggleLlmStatus = () => {
    setLlmStatus(prev => {
      if (prev === 'online') return 'slow';
      if (prev === 'slow') return 'offline';
      return 'online';
    });
  };

  // Clean sessions list on unload
  const hasValidSession = sessionId !== null;

  return (
    <div className="h-screen w-screen flex flex-col bg-ide-bg overflow-hidden select-none font-sans relative">
      {/* Top Navbar */}
      <Navbar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        selectedLanguage={selectedLanguage}
        setSelectedLanguage={handleLanguageChange}
        llmStatus={llmStatus}
        isRunning={isRunning}
        onRunCode={handleRunCode}
        userRole={userRole}
        isAuthenticated={isAuthenticated}
        onOpenLogin={() => setShowLoginModal(true)}
        onOpenMonitor={() => setShowMonitor(true)}
        onLogout={handleLogout}
      />

      {/* Login Screen Modal Overlay */}
      {showLoginModal && (
        <LoginScreen
          onClose={() => setShowLoginModal(false)}
          onLoginSuccess={() => {
            setIsAuthenticated(true);
            setUserRole(localStorage.getItem("user_role") || "user");
            setShowLoginModal(false);
          }}
        />
      )}

      {/* Interactive Lesson View Overlay */}
      {activeLesson && (
        <InteractiveLessonView
          lesson={activeLesson}
          sessionId={sessionId}
          userStats={userStats}
          onClose={() => setActiveLesson(null)}
          onOpenPricing={() => {
            setActiveLesson(null);
            setActiveTab('pricing');
          }}
          onSendMessage={handleSendMessage}
          messages={messages}
          agentStatus={agentStatus}
          agentCurrentFile={agentCurrentFile}
          isStreaming={isStreaming}
          onClearHistory={handleClearHistory}
          onStopAgent={handleStopAgent}
        />
      )}

      {/* Admin Security Dashboard Oversight Overlay */}
      {showMonitor && <AdminMonitor onClose={() => setShowMonitor(false)} />}

      {/* Main View Area Routing */}
      <div className="flex-1 min-h-0 overflow-hidden relative flex flex-col">
        {activeTab === 'home' ? (
          <LandingHome
            onStartLearning={() => setActiveTab('journeys')}
            onExploreJourneys={() => setActiveTab('journeys')}
            onOpenPricing={() => setActiveTab('pricing')}
          />
        ) : activeTab === 'journeys' ? (
          <JourneysCatalog
            onSelectLesson={(lesson) => {
              setActiveTab('map');
            }}
          />
        ) : activeTab === 'map' ? (
          <GamifiedJourneyMap
            userStats={userStats}
            onOpenPricing={() => setActiveTab('pricing')}
            onStartLesson={(node) => {
              setActiveLesson({
                id: node.id,
                title: node.title,
                description: node.description || "Complete the task to proceed to the next node."
              });
            }}
          />
        ) : activeTab === 'practice' ? (
          <PracticeCatalog
            onSelectProblem={(prob) => {
              setActiveLesson(prob);
            }}
          />
        ) : activeTab === 'pricing' ? (
          <PricingView userEmail={localStorage.getItem("user_email")} />
        ) : hasValidSession ? (
          <SplitLayout
            left={
              <FileTree
                files={fileTree}
                activeFile={activeFile}
                onFileClick={handleFileClick}
                onDeleteFile={handleDeleteFile}
                onRenameFile={handleRenameFile}
                onCreateFile={handleCreateFile}
                onCreateFolder={handleCreateFolder}
              />
            }
            editor={
              <>
                <EditorTabs
                  openFiles={openFiles}
                  activeFile={activeFile}
                  setActiveFile={setActiveFile}
                  onCloseFile={handleCloseFile}
                  fileStates={fileStates}
                />
                <MonacoEditor
                  sessionId={sessionId}
                  filePath={activeFile}
                  content={activeFile ? fileStates[activeFile]?.content : ''}
                  language={activeFile ? fileStates[activeFile]?.language : 'plaintext'}
                  isDirty={activeFile ? fileStates[activeFile]?.isDirty : false}
                  onChange={handleEditorChange}
                  onSaved={() => {
                    if (activeFile) {
                      setFileStates(prev => ({
                        ...prev,
                        [activeFile]: {
                          ...prev[activeFile],
                          isDirty: false
                        }
                      }));
                    }
                  }}
                />
              </>
            }
            terminal={
              <Terminal
                lines={terminalLines}
                isRunning={isRunning}
                onClearTerminal={() => setTerminalLines([])}
              />
            }
            right={
              <ChatPanel
                messages={messages}
                onSendMessage={handleSendMessage}
                agentStatus={agentStatus}
                agentCurrentFile={agentCurrentFile}
                isStreaming={isStreaming}
                onClearHistory={handleClearHistory}
                onStopAgent={handleStopAgent}
              />
            }
          />
        ) : (
          <div className="flex-1 flex flex-col items-center justify-center bg-ide-bg text-ide-text">
            <div className="w-10 h-10 border-4 border-accent-blue border-t-transparent rounded-full animate-spin mb-4"></div>
            <span className="text-sm font-semibold">Configuring your Prasana Code AI sandbox workspace...</span>
          </div>
        )}
      </div>

      {/* LLM Offline Banner Overlay */}
      {llmStatus === 'offline' && (
        <div className="bg-rose-500/90 text-ide-text font-sans text-xs font-bold py-1.5 px-4 text-center select-none animate-bounce flex items-center justify-center gap-1.5">
          <span>⚠️ AI Agent Service Unavailable: Both Qwen primary and fallback LLMs are offline. Owner has been notified.</span>
          <button 
            onClick={handleToggleLlmStatus} 
            className="underline cursor-pointer hover:text-ide-text/80 border border-white/40 px-2 py-0.5 rounded ml-2 transition-colors"
          >
            Retry Connection
          </button>
        </div>
      )}

      {/* Quick Interactive Tooltip Info Footer */}
      <div 
        onClick={handleToggleLlmStatus}
        className="h-6 bg-ide-navbar border-t border-ide-border flex items-center px-4 justify-between text-[10px] text-ide-muted select-none cursor-pointer hover:bg-ide-border transition-colors font-sans"
        title="Click to toggle simulated LLM Health State"
      >
        <span>⚡ Double-click bottom footer to cycle LLM Health states (Online ➔ Slow ➔ Offline)</span>
        <span className="font-semibold text-accent-blue hover:underline">
          Status: {llmStatus.toUpperCase()} (Simulated)
        </span>
      </div>
    </div>
  );
}
