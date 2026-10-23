import React, { useState } from 'react';
import { loginApi, registerApi } from '../../api/agentApi';
import { Shield, User, Lock, Mail, ArrowRight, Code2, AlertCircle, X } from 'lucide-react';

export default function LoginScreen({ onLoginSuccess, onClose }) {
  const [authMode, setAuthMode] = useState('email'); // 'email'
  const [isAdminMode, setIsAdminMode] = useState(false);
  const [isRegister, setIsRegister] = useState(false);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      if (isRegister) {
        await registerApi(email, password);
        await loginApi(email, password);
      } else {
        const data = await loginApi(email, password);
        if (isAdminMode && data.user.role !== 'admin') {
          throw new Error('Access denied: You do not have administrator privileges.');
        }
      }
      onLoginSuccess();
    } catch (err) {
      setError(err.message || 'An authentication error occurred.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 w-screen h-screen flex items-center justify-center bg-black/80 backdrop-blur-md p-4 font-sans text-ide-text">
      {/* Container Card */}
      <div className="w-full max-w-md p-8 rounded-3xl bg-[#111622] border border-ide-border shadow-2xl relative z-10">
        {/* Close Button */}
        {onClose && (
          <button
            onClick={onClose}
            className="absolute top-5 right-5 p-2 rounded-xl bg-ide-sidebar/80 hover:bg-gray-700 text-ide-muted hover:text-ide-text transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        )}

        {/* Logo & Header */}
        <div className="flex flex-col items-center mb-6 text-center">
          <div className="w-12 h-12 rounded-2xl bg-gradient-to-tr from-emerald-500 via-teal-400 to-emerald-300 flex items-center justify-center shadow-lg shadow-emerald-500/20 mb-3">
            <Code2 className="w-6 h-6 text-slate-950 font-bold" />
          </div>
          <h2 className="text-2xl font-extrabold tracking-tight">Prasana Code AI</h2>
          <p className="text-xs text-ide-muted mt-1">Official Platform of @itsprasana</p>
        </div>

        {/* Form Inputs */}
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-[11px] font-bold text-ide-muted uppercase tracking-wider mb-1">Email Address</label>
            <div className="relative">
              <Mail className="absolute left-3 top-3 w-4 h-4 text-ide-muted" />
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="you@example.com"
                className="w-full bg-ide-panel border border-ide-border rounded-xl py-2.5 pl-10 pr-4 text-xs text-ide-text focus:outline-none focus:border-emerald-500"
              />
            </div>
          </div>

          <div>
            <label className="block text-[11px] font-bold text-ide-muted uppercase tracking-wider mb-1">Password</label>
            <div className="relative">
              <Lock className="absolute left-3 top-3 w-4 h-4 text-ide-muted" />
              <input
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                className="w-full bg-ide-panel border border-ide-border rounded-xl py-2.5 pl-10 pr-4 text-xs text-ide-text focus:outline-none focus:border-emerald-500"
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full py-3 rounded-2xl bg-gradient-to-r from-emerald-400 via-teal-400 to-emerald-300 hover:from-emerald-300 hover:to-teal-300 text-slate-950 font-bold text-xs shadow-lg shadow-emerald-500/20 active:scale-95 transition-all flex items-center justify-center gap-2"
          >
            {loading ? (
              <span className="w-4 h-4 border-2 border-slate-950 border-t-transparent rounded-full animate-spin" />
            ) : (
              <>
                <span>{isRegister ? 'Create Account' : 'Log In'}</span>
                <ArrowRight className="w-4 h-4" />
              </>
            )}
          </button>
        </form>

        {/* Register Toggle */}
        <div className="mt-4 text-center">
          <button
            onClick={() => setIsRegister(!isRegister)}
            className="text-xs text-emerald-400 hover:underline font-medium"
          >
            {isRegister ? 'Already have an account? Sign In' : "Don't have an account? Register Free"}
          </button>
        </div>
      </div>
    </div>
  );
}
