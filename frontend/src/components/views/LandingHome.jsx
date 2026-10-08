import React from 'react';
import { Sparkles, Code2, Rocket, Award, CheckCircle2, ArrowRight, Zap, Play, Terminal } from 'lucide-react';

export default function LandingHome({ onStartLearning, onExploreJourneys, onOpenPricing }) {
  return (
    <div className="h-full w-full bg-ide-bg text-ide-text font-sans overflow-y-auto pb-32 selection:bg-purple-500 selection:text-ide-text">
      {/* Hero Section */}
      <section className="relative pt-16 pb-20 px-6 max-w-7xl mx-auto text-center flex flex-col items-center">
        {/* Youtube Brand Pill */}
        <a
          href="https://www.youtube.com/@itsprasana"
          target="_blank"
          rel="noreferrer"
          className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-rose-500/10 border border-rose-500/20 text-rose-300 text-xs font-medium hover:border-rose-500/40 transition-all duration-300 mb-8 shadow-sm"
        >
          <svg className="w-4 h-4 fill-rose-400 text-rose-400" viewBox="0 0 24 24">
            <path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/>
          </svg>
          <span>Official Platform of @itsprasana Channel</span>
          <ArrowRight className="w-3.5 h-3.5" />
        </a>

        {/* Hero Title */}
        <h1 className="text-4xl md:text-6xl lg:text-7xl font-bold tracking-tight max-w-5xl leading-tight text-ide-text">
          Master Software Engineering & AI <span className="bg-gradient-to-r from-emerald-300 via-teal-300 to-emerald-200 bg-clip-text text-transparent">Through Live Practice</span>
        </h1>

        <p className="mt-6 text-lg md:text-xl text-ide-muted max-w-3xl leading-relaxed font-normal">
          Interactive bite-sized skill paths, instant multi-language execution, and your personal <strong className="text-emerald-400 font-semibold">Prasana AI Tutor</strong> providing real-time line-by-line guidance.
        </p>

        {/* CTA Buttons */}
        <div className="mt-10 flex flex-wrap items-center justify-center gap-4">
          <button
            onClick={onStartLearning}
            className="flex items-center gap-2.5 px-8 py-4 rounded-2xl bg-gradient-to-r from-emerald-400 via-teal-400 to-emerald-300 hover:from-emerald-300 hover:to-teal-300 text-slate-950 font-bold text-base shadow-lg shadow-emerald-500/20 active:scale-95 transition-all duration-200"
          >
            <Rocket className="w-5 h-5 text-slate-950" />
            <span>Start Learning Free</span>
          </button>
          
          <button
            onClick={onExploreJourneys}
            className="flex items-center gap-2 px-7 py-4 rounded-2xl bg-ide-panel/90 hover:bg-ide-sidebar border border-ide-border text-ide-text font-medium text-base active:scale-95 transition-all duration-200"
          >
            <Code2 className="w-5 h-5 text-emerald-400" />
            <span>Explore Skill Paths</span>
          </button>
        </div>

        {/* Interactive Feature Stats */}
        <div className="mt-16 grid grid-cols-2 md:grid-cols-4 gap-4 w-full max-w-4xl">
          {[
            { label: 'Interactive Skill Paths', val: '5 Full Tracks' },
            { label: 'AI Tutor Guidance', val: 'Line-by-Line Hints' },
            { label: 'In-Browser Languages', val: 'Python, JS, C++, DSA' },
            { label: 'Payment Gateway', val: 'Razorpay & Direct UPI' }
          ].map((stat, idx) => (
            <div key={idx} className="p-4 rounded-2xl bg-ide-panel/60 border border-ide-border/80 text-center">
              <div className="text-xl font-bold text-emerald-400">{stat.val}</div>
              <div className="text-xs text-ide-muted mt-1 font-normal">{stat.label}</div>
            </div>
          ))}
        </div>
      </section>

      {/* Feature Grid */}
      <section className="py-20 px-6 bg-ide-panel/40 border-t border-b border-ide-border/80">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-5xl font-bold tracking-tight text-ide-text">Designed for Real Career Growth</h2>
            <p className="text-ide-muted mt-4 text-base max-w-2xl mx-auto">
              Everything you need to go from beginner to pro software engineer with intelligent AI coaching.
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            <div className="p-8 rounded-3xl bg-ide-panel/80 border border-ide-border/80 hover:border-emerald-400/40 transition-all duration-300 shadow-xl">
              <div className="w-12 h-12 rounded-2xl bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center text-emerald-400 mb-6">
                <Sparkles className="w-6 h-6" />
              </div>
              <h3 className="text-xl font-bold mb-3 text-ide-text">Prasana AI Tutor</h3>
              <p className="text-ide-muted text-sm leading-relaxed">
                Intelligent coding coach. Analyzes logic errors, highlights exact line numbers, and hints fixes without spoiling complete solutions.
              </p>
            </div>

            <div className="p-8 rounded-3xl bg-ide-panel/80 border border-ide-border/80 hover:border-teal-400/40 transition-all duration-300 shadow-xl">
              <div className="w-12 h-12 rounded-2xl bg-teal-500/10 border border-teal-500/30 flex items-center justify-center text-teal-300 mb-6">
                <Terminal className="w-6 h-6" />
              </div>
              <h3 className="text-xl font-bold mb-3 text-ide-text">Instant Execution Sandbox</h3>
              <p className="text-ide-muted text-sm leading-relaxed">
                Integrated code runner with live Python, Node.js, C++, and Bash execution running inside secure isolated sandbox containers.
              </p>
            </div>

            <div className="p-8 rounded-3xl bg-ide-panel/80 border border-ide-border/80 hover:border-emerald-400/40 transition-all duration-300 shadow-xl">
              <div className="w-12 h-12 rounded-2xl bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center text-emerald-300 mb-6">
                <Award className="w-6 h-6" />
              </div>
              <h3 className="text-xl font-bold mb-3 text-ide-text">DSA & Interview Prep</h3>
              <p className="text-ide-muted text-sm leading-relaxed">
                Comprehensive algorithmic challenges with automated test case validation and time/space complexity insights.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Footer Branding */}
      <footer className="py-10 text-center text-xs text-slate-500 border-t border-ide-border/80">
        <p>© 2026 Prasana Code AI — Built for @itsprasana Community. Powered by FastAPI & React.</p>
      </footer>
    </div>
  );
}

