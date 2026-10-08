import React, { useState, useEffect } from 'react';
import { fetchMetricsApi, API_BASE_URL } from '../../api/agentApi';
import { Users, Clock, ShieldAlert, FileText, ArrowLeft, RefreshCw, Trash2, Eye, ShieldCheck } from 'lucide-react';

export default function AdminMonitor({ onClose }) {
  const [metrics, setMetrics] = useState({ users: [], engagement: [], logs: [] });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [selectedUserFiles, setSelectedUserFiles] = useState([]);
  const [inspectingUser, setInspectingUser] = useState(null);
  const [fileLoading, setFileLoading] = useState(false);

  const loadMetrics = async () => {
    setLoading(true);
    setError('');
    try {
      const data = await fetchMetricsApi();
      setMetrics(data);
    } catch (err) {
      setError('Failed to fetch dashboard metrics. Verify backend credentials.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadMetrics();
    const interval = setInterval(loadMetrics, 15000); // Auto-refresh every 15s
    return () => clearInterval(interval);
  }, []);

  const handleInspectUserFiles = async (user) => {
    setInspectingUser(user);
    setFileLoading(true);
    try {
      const token = localStorage.getItem("access_token");
      const res = await fetch(`${API_BASE_URL}/admin/files/${user.id}`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (res.ok) {
        const data = await res.json();
        setSelectedUserFiles(data);
      } else {
        setSelectedUserFiles([]);
      }
    } catch (err) {
      console.error('Failed to load files', err);
    } finally {
      setFileLoading(false);
    }
  };

  const handleDeleteUserFile = async (filename) => {
    if (!window.confirm(`Are you sure you want to delete "${filename}" for user ${inspectingUser.email}?`)) {
      return;
    }
    try {
      const token = localStorage.getItem("access_token");
      const res = await fetch(`${API_BASE_URL}/admin/files/${inspectingUser.id}/${encodeURIComponent(filename)}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (res.ok) {
        // Reload files
        handleInspectUserFiles(inspectingUser);
      } else {
        alert("Failed to delete file.");
      }
    } catch (err) {
      console.error('Failed to delete file', err);
    }
  };

  // Convert engagement seconds to human readable
  const formatTime = (seconds) => {
    if (seconds < 60) return `${seconds}s`;
    const mins = Math.floor(seconds / 60);
    if (mins < 60) return `${mins}m`;
    const hrs = Math.floor(mins / 60);
    return `${hrs}h ${mins % 60}m`;
  };

  return (
    <div className="fixed inset-0 z-50 w-screen h-screen bg-[#0a0d14] flex flex-col font-sans text-ide-text overflow-y-auto">
      {/* Navbar header */}
      <header className="h-16 bg-[#111622] border-b border-[#1e2638] px-6 flex items-center justify-between shrink-0">
        <div className="flex items-center gap-3">
          <button 
            onClick={onClose}
            className="p-2 hover:bg-[#1e2638] rounded-lg transition-colors text-ide-muted hover:text-ide-text"
          >
            <ArrowLeft className="w-5 h-5" />
          </button>
          <div className="flex items-center gap-2">
            <span className="h-2.5 w-2.5 rounded-full bg-purple-500 animate-pulse" />
            <h1 className="text-lg font-bold tracking-wide">LiveCodeAI Security Monitor</h1>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <button 
            onClick={loadMetrics}
            disabled={loading}
            className="flex items-center gap-1.5 px-3 py-1.5 bg-[#161d2d] hover:bg-[#232d44] text-xs font-semibold rounded-lg border border-[#232d44] transition-all disabled:opacity-50"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
            Refresh
          </button>
          <span className="text-xs text-ide-muted">Auto-refreshes every 15s</span>
        </div>
      </header>

      {/* Main dashboard content */}
      {(() => {
        const usersList = metrics?.users || [];
        const engagementList = metrics?.engagement || [];
        const logsList = metrics?.logs || [];

        return (
          <main className="flex-1 p-6 max-w-7xl w-full mx-auto space-y-6">
            
            {/* Metric Cards Row */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="bg-[#111622]/80 border border-[#1e2638] rounded-xl p-5 flex items-center gap-4">
                <div className="w-12 h-12 rounded-lg bg-purple-600/10 text-purple-400 flex items-center justify-center">
                  <Users className="w-6 h-6" />
                </div>
                <div>
                  <p className="text-xs text-ide-muted uppercase tracking-wider font-semibold">Registered Users</p>
                  <h3 className="text-2xl font-bold mt-0.5">{usersList.length}</h3>
                </div>
              </div>

              <div className="bg-[#111622]/80 border border-[#1e2638] rounded-xl p-5 flex items-center gap-4">
                <div className="w-12 h-12 rounded-lg bg-accent-blue/10 text-accent-blue flex items-center justify-center">
                  <Clock className="w-6 h-6" />
                </div>
                <div>
                  <p className="text-xs text-ide-muted uppercase tracking-wider font-semibold">Active Sessions</p>
                  <h3 className="text-2xl font-bold mt-0.5">{engagementList.length}</h3>
                </div>
              </div>

              <div className="bg-[#111622]/80 border border-[#1e2638] rounded-xl p-5 flex items-center gap-4">
                <div className="w-12 h-12 rounded-lg bg-rose-500/10 text-rose-400 flex items-center justify-center">
                  <ShieldAlert className="w-6 h-6" />
                </div>
                <div>
                  <p className="text-xs text-ide-muted uppercase tracking-wider font-semibold">Security Audits</p>
                  <h3 className="text-2xl font-bold mt-0.5">{logsList.length}</h3>
                </div>
              </div>
            </div>

            {/* Dynamic Panels */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              
              {/* User management and Engagement list */}
              <div className="bg-[#111622]/80 border border-[#1e2638] rounded-xl p-6 flex flex-col h-[400px]">
                <h3 className="text-sm font-bold uppercase tracking-wider text-ide-muted mb-4">User Oversight</h3>
                <div className="flex-1 overflow-y-auto space-y-3">
                  {usersList.map((user) => {
                    // Find matching active engagement session
                    const sessions = engagementList.filter(s => s.email === user.email);
                    const totalSeconds = sessions.reduce((acc, curr) => acc + (curr.engagement_seconds || 0), 0);
                    const ipList = sessions.map(s => s.ip_address).join(', ') || 'N/A';
                    
                    return (
                      <div key={user.id || user.email} className="bg-[#161d2d]/60 border border-[#232d44] rounded-lg p-4 flex items-center justify-between hover:border-purple-500/30 transition-all duration-300">
                        <div className="space-y-1">
                          <div className="flex items-center gap-2">
                            <span className="font-semibold text-sm text-ide-text">{user.email}</span>
                            {user.role === 'admin' && (
                              <span className="px-2 py-0.5 bg-purple-500/15 border border-purple-500/30 text-[10px] text-purple-300 rounded font-bold uppercase">
                                Admin
                              </span>
                            )}
                          </div>
                          <div className="text-[11px] text-ide-muted space-y-0.5">
                            <p>Engagement duration: <span className="text-accent-blue font-semibold">{formatTime(totalSeconds)}</span></p>
                            <p>IP Address: <span className="text-ide-text/80">{ipList}</span></p>
                          </div>
                        </div>

                        <button 
                          onClick={() => handleInspectUserFiles(user)}
                          className="flex items-center gap-1 bg-[#232d44] hover:bg-purple-600/80 text-xs font-semibold px-3 py-1.5 rounded-md transition-all active:scale-95"
                        >
                          <Eye className="w-3.5 h-3.5" />
                          Inspect Files
                        </button>
                      </div>
                    );
                  })}
                  {usersList.length === 0 && (
                    <div className="text-center text-xs text-ide-muted py-8">No users found.</div>
                  )}
                </div>
              </div>

              {/* User File Inspector details */}
              <div className="bg-[#111622]/80 border border-[#1e2638] rounded-xl p-6 flex flex-col h-[400px]">
                <h3 className="text-sm font-bold uppercase tracking-wider text-ide-muted mb-4">
                  File Storage Oversight: {inspectingUser ? inspectingUser.email : 'Select a user'}
                </h3>
                <div className="flex-1 overflow-y-auto">
                  {inspectingUser ? (
                    fileLoading ? (
                      <div className="flex flex-col items-center justify-center h-full gap-2">
                        <span className="w-8 h-8 border-2 border-accent-blue border-t-transparent rounded-full animate-spin" />
                        <p className="text-xs text-ide-muted">Fetching file indices...</p>
                      </div>
                    ) : selectedUserFiles.length > 0 ? (
                      <div className="space-y-2">
                        {selectedUserFiles.map((file) => (
                          <div key={file.name} className="flex items-center justify-between p-3 bg-[#161d2d]/60 border border-[#232d44] rounded-lg">
                            <div className="flex items-center gap-2">
                              <FileText className="w-4 h-4 text-accent-blue" />
                              <span className="text-xs font-medium text-ide-text/90">{file.name}</span>
                              <span className="text-[10px] text-ide-muted">({Math.round(file.metadata.size / 10.24) / 100} KB)</span>
                            </div>
                            <button 
                              onClick={() => handleDeleteUserFile(file.name)}
                              className="p-1.5 bg-[#232d44] hover:bg-rose-600/20 text-ide-muted hover:text-rose-400 border border-transparent hover:border-rose-500/30 rounded transition-all"
                            >
                              <Trash2 className="w-3.5 h-3.5" />
                            </button>
                          </div>
                        ))}
                      </div>
                    ) : (
                      <div className="text-center text-xs text-ide-muted py-8">
                        No files currently saved in Supabase for this workspace.
                      </div>
                    )
                  ) : (
                    <div className="flex items-center justify-center h-full text-xs text-ide-muted text-center p-4 border border-dashed border-[#232d44] rounded-lg">
                      Click "Inspect Files" on a user to view their persistent workspace filesystem.
                    </div>
                  )}
                </div>
              </div>
            </div>

            {/* Security Audit logs panel */}
            <div className="bg-[#111622]/80 border border-[#1e2638] rounded-xl p-6 flex flex-col h-[300px]">
              <h3 className="text-sm font-bold uppercase tracking-wider text-ide-muted mb-4">Security Guardrail Logs</h3>
              <div className="flex-1 overflow-y-auto space-y-2.5 font-mono text-[11px]">
                {logsList.map((log) => (
                  <div key={log.id} className="p-2.5 bg-[#161d2d]/60 border border-[#232d44] rounded flex items-start gap-3">
                    <div className="shrink-0 mt-0.5">
                      {log.action.includes('error') || log.action.includes('blocked') ? (
                        <ShieldAlert className="w-4 h-4 text-rose-400" />
                      ) : (
                        <ShieldCheck className="w-4 h-4 text-emerald-400" />
                      )}
                    </div>
                    <div className="flex-1 text-ide-text/95">
                      <div className="flex items-center justify-between text-[10px] text-ide-muted mb-1">
                        <span>User: {log.email}</span>
                        <span>{new Date(log.created_at).toLocaleString()}</span>
                      </div>
                      <span className="font-bold text-accent-blue uppercase text-[10px] bg-accent-blue/10 border border-accent-blue/20 px-1.5 py-0.5 rounded mr-2">
                        {log.action}
                      </span>
                      <span>{log.details}</span>
                    </div>
                  </div>
                ))}
                {logsList.length === 0 && (
                  <div className="text-center text-xs text-ide-muted py-8">No security logs recorded.</div>
                )}
              </div>
            </div>
          </main>
        );
      })()}
    </div>
  );
}
