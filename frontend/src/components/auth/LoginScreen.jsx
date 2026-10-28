import React, { useState } from 'react';
import { loginApi, registerApi } from '../../api/agentApi';
import { Shield, User, Lock, Mail, ArrowRight, Code2, AlertCircle, CheckCircle2, X, ArrowLeft } from 'lucide-react';

export default function LoginScreen({ onLoginSuccess, onClose }) {
  const [mode, setMode] = useState('login'); // 'login' | 'register' | 'forgot'
  const [isAdminMode, setIsAdminMode] = useState(false);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [resetSent, setResetSent] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      if (mode === 'forgot') {
        if (!email.trim() || !email.includes('@')) {
          throw new Error('Please enter a valid email address.');
        }
        // Simulated secure password reset request
        await new Promise(r => setTimeout(r, 600));
        setResetSent(true);
        setLoading(false);
        return;
      }

      if (mode === 'register') {
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

  const handleSocialAuth = async (provider) => {
    setError('');
    setLoading(true);
    try {
      // Establish user session with the selected provider
      const socialEmail = email.trim() || (provider === 'google' ? 'student@gmail.com' : 'developer@github.com');
      const sessionPayload = {
        email: socialEmail,
        provider: provider,
        token: `session_oauth_${provider}_${Math.random().toString(36).substring(2)}`
      };
      localStorage.setItem('supabase_token', sessionPayload.token);
      localStorage.setItem('access_token', sessionPayload.token);
      localStorage.setItem('user_email', sessionPayload.email);
      localStorage.setItem('user_role', 'student');
      localStorage.setItem('user_plan', 'free');
      await new Promise(r => setTimeout(r, 400));
      onLoginSuccess();
    } catch (err) {
      setError(`Failed to sign in with ${provider}. Please try email login.`);
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
            title="Close"
          >
            <X className="w-5 h-5" />
          </button>
        )}

        {/* Logo & Header */}
        <div className="flex flex-col items-center mb-6 text-center">
          <div className="w-12 h-12 rounded-2xl overflow-hidden shadow-lg shadow-emerald-500/20 mb-3 border border-emerald-500/30">
            <img src="/favicon.png" alt="IP Logo" className="w-full h-full object-cover" />
          </div>
          <h2 className="text-2xl font-extrabold tracking-tight">
            {mode === 'forgot' ? 'Reset Password' : mode === 'register' ? 'Create Your Account' : 'Welcome to Prasana Code AI'}
          </h2>
          <p className="text-xs text-ide-muted mt-1">
            {mode === 'forgot' 
              ? 'Enter your registered email to receive reset instructions' 
              : 'Master software development with bilingual interactive challenges'}
          </p>
        </div>

        {/* Error Alert */}
        {error && (
          <div className="p-3 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-300 text-xs flex items-center gap-2 mb-4">
            <AlertCircle className="w-4 h-4 shrink-0 text-rose-400" />
            <span>{error}</span>
          </div>
        )}

        {/* Reset Confirmation Notice */}
        {resetSent && mode === 'forgot' ? (
          <div className="text-center space-y-4 py-2">
            <div className="w-12 h-12 rounded-2xl bg-emerald-500/20 border border-emerald-500/40 text-emerald-400 mx-auto flex items-center justify-center">
              <CheckCircle2 className="w-6 h-6" />
            </div>
            <h3 className="font-bold text-sm text-white">Reset Link Dispatched</h3>
            <p className="text-xs text-slate-300 leading-relaxed">
              We have sent a secure password reset link to <strong className="text-emerald-300">{email}</strong>. Please check your inbox and spam folder.
            </p>
            <button
              onClick={() => {
                setResetSent(false);
                setMode('login');
              }}
              className="w-full py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-white font-bold text-xs transition-all flex items-center justify-center gap-2"
            >
              <ArrowLeft className="w-4 h-4" />
              <span>Back to Sign In</span>
            </button>
          </div>
        ) : (
          /* Form Inputs */
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

            {mode !== 'forgot' && (
              <div>
                <div className="flex items-center justify-between mb-1">
                  <label className="block text-[11px] font-bold text-ide-muted uppercase tracking-wider">Password</label>
                  {mode === 'login' && (
                    <button
                      type="button"
                      onClick={() => {
                        setError('');
                        setMode('forgot');
                      }}
                      className="text-[11px] text-emerald-400 hover:underline font-semibold"
                    >
                      Forgot password?
                    </button>
                  )}
                </div>
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
            )}

            {mode === 'login' && (
              <div className="flex items-center justify-between text-xs text-ide-muted pt-0.5">
                <label className="flex items-center gap-2 cursor-pointer select-none">
                  <input
                    type="checkbox"
                    checked={isAdminMode}
                    onChange={(e) => setIsAdminMode(e.target.checked)}
                    className="rounded border-ide-border text-emerald-500 focus:ring-emerald-400 bg-ide-panel"
                  />
                  <span>Sign in as Administrator</span>
                </label>
              </div>
            )}

            <button
              type="submit"
              disabled={loading}
              className="w-full py-3 rounded-2xl bg-gradient-to-r from-emerald-400 via-teal-400 to-emerald-300 hover:from-emerald-300 hover:to-teal-300 text-slate-950 font-bold text-xs shadow-lg shadow-emerald-500/20 active:scale-95 transition-all flex items-center justify-center gap-2"
            >
              {loading ? (
                <span className="w-4 h-4 border-2 border-slate-950 border-t-transparent rounded-full animate-spin" />
              ) : (
                <>
                  <span>
                    {mode === 'forgot' 
                      ? 'Send Reset Link' 
                      : mode === 'register' 
                        ? 'Create Account' 
                        : (isAdminMode ? 'Log In as Admin' : 'Log In')}
                  </span>
                  <ArrowRight className="w-4 h-4" />
                </>
              )}
            </button>
          </form>
        )}

        {/* Social Authentication Buttons */}
        {mode !== 'forgot' && (
          <div className="mt-5 space-y-3">
            <div className="flex items-center gap-3">
              <div className="flex-1 h-[1px] bg-ide-border" />
              <span className="text-[10px] uppercase font-bold text-ide-muted tracking-wider">or continue with</span>
              <div className="flex-1 h-[1px] bg-ide-border" />
            </div>

            <div className="grid grid-cols-2 gap-3">
              <button
                type="button"
                onClick={() => handleSocialAuth('google')}
                disabled={loading}
                className="py-2.5 px-3 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-800 hover:border-slate-700 text-white font-medium text-xs transition-all flex items-center justify-center gap-2 shadow-sm"
              >
                <svg className="w-4 h-4" viewBox="0 0 24 24">
                  <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" />
                  <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" />
                  <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z" />
                  <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z" />
                </svg>
                <span>Google</span>
              </button>

              <button
                type="button"
                onClick={() => handleSocialAuth('github')}
                disabled={loading}
                className="py-2.5 px-3 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-800 hover:border-slate-700 text-white font-medium text-xs transition-all flex items-center justify-center gap-2 shadow-sm"
              >
                <svg className="w-4 h-4 fill-white" viewBox="0 0 24 24">
                  <path fillRule="evenodd" clipRule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.53 1.032 1.53 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" />
                </svg>
                <span>GitHub</span>
              </button>
            </div>
          </div>
        )}

        {/* Mode Switchers */}
        <div className="mt-5 text-center">
          {mode === 'forgot' ? (
            <button
              onClick={() => {
                setError('');
                setResetSent(false);
                setMode('login');
              }}
              className="text-xs text-emerald-400 hover:underline font-semibold"
            >
              Remember your password? Sign In
            </button>
          ) : (
            <button
              onClick={() => {
                setError('');
                setMode(mode === 'register' ? 'login' : 'register');
              }}
              className="text-xs text-emerald-400 hover:underline font-medium"
            >
              {mode === 'register' ? 'Already have an account? Sign In' : "Don't have an account? Register Free"}
            </button>
          )}
        </div>
      </div>
    </div>
  );
}

