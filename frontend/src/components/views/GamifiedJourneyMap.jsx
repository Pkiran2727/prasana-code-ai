import React, { useState } from 'react';
import { 
  BookOpen, Dumbbell, Palette, Flag, History, Trophy, Store, User, 
  Search, Flame, Gem, Zap, Check, Star, Lock, ArrowRight, Sparkles, ChevronRight, Layers, CheckCircle2, PlayCircle
} from 'lucide-react';

export default function GamifiedJourneyMap({ onStartLesson, onOpenPricing, userStats }) {
  const [activeSideTab, setActiveSideTab] = useState('journey');
  const [viewMode, setViewMode] = useState('grid'); // 'grid' or 'list'

  // Structured Professional Syllabus Modules List
  const modules = [
    {
      id: 'mod-1',
      title: 'Module 1: Fundamentals & Variables',
      desc: 'Master core variable declaration, data types, and standard input/output formatting.',
      status: 'completed',
      progress: 100,
      lessons: [
        { id: 1, title: 'Variables & Data Types', status: 'completed', desc: 'Declare integers, floats, strings, and booleans.' },
        { id: 2, title: 'Input & Output Functions', status: 'completed', desc: 'Read user input and format output strings.' }
      ]
    },
    {
      id: 'mod-2',
      title: 'Module 2: Conditional Logic & Decision Making',
      desc: 'Learn branching control flows using if, else if, and logical operators.',
      status: 'active',
      progress: 50,
      lessons: [
        { id: 3, title: 'If-Else Conditionals', status: 'completed', desc: 'Evaluate Boolean expressions to control code path.' },
        { id: 4, title: 'Nested If - Else Logic', status: 'active', desc: 'Build multi-condition decision trees for real apps.' },
        { id: 5, title: 'Logical Operators (AND / OR)', status: 'locked', desc: 'Combine multiple condition checks in one statement.' }
      ]
    },
    {
      id: 'mod-3',
      title: 'Module 3: Loops & Algorithmic Iteration',
      desc: 'Automate repetitive tasks with while loops, for loops, and break/continue statements.',
      status: 'locked',
      progress: 0,
      lessons: [
        { id: 6, title: 'Recap - Simple Calculator', status: 'locked', desc: 'Build a interactive multi-op calculator.' },
        { id: 7, title: 'For Loop Sequence Iteration', status: 'locked', desc: 'Iterate over ranges, lists, and string sequences.' },
        { id: 8, title: 'While Loops & Exit Flags', status: 'locked', desc: 'Run code blocks dynamically until condition becomes false.' }
      ]
    }
  ];

  const sideNavItems = [
    { id: 'journey', label: 'Modules Path', icon: <Layers className="w-4 h-4 text-emerald-400" /> },
    { id: 'practice', label: 'Practice Problems', icon: <Dumbbell className="w-4 h-4 text-teal-300" /> },
    { id: 'projects', label: 'Projects', icon: <Palette className="w-4 h-4 text-emerald-300" /> },
    { id: 'missions', label: 'Daily Missions', icon: <Flag className="w-4 h-4 text-rose-400" /> },
    { id: 'leaderboard', label: 'Leaderboard', icon: <Trophy className="w-4 h-4 text-emerald-400" /> },
    { id: 'profile', label: 'Profile', icon: <User className="w-4 h-4 text-teal-400" /> }
  ];

  return (
    <div className="h-full w-full bg-ide-bg text-ide-text flex font-sans select-none overflow-hidden">
      {/* Left Navigation Sidebar */}
      <aside className="w-64 bg-ide-panel/90 border-r border-ide-border/80 p-4 flex flex-col justify-between shrink-0 h-full overflow-y-auto pb-16">
        <div className="space-y-6">
          {/* Brand */}
          <div className="flex items-center gap-3 px-2">
            <div className="w-8 h-8 rounded-xl bg-gradient-to-tr from-emerald-500 via-teal-400 to-emerald-300 flex items-center justify-center font-bold text-xs text-slate-950">
              PCA
            </div>
            <span className="font-bold text-sm bg-gradient-to-r from-slate-100 via-emerald-200 to-teal-300 bg-clip-text text-transparent">
              Prasana Code AI
            </span>
          </div>

          {/* Navigation Items */}
          <nav className="space-y-1">
            {sideNavItems.map(item => (
              <button
                key={item.id}
                onClick={() => setActiveSideTab(item.id)}
                className={`w-full flex items-center gap-3 px-3.5 py-2.5 rounded-xl font-medium text-xs transition-all ${
                  activeSideTab === item.id
                    ? 'bg-ide-sidebar text-ide-text border border-ide-border/80 shadow-sm'
                    : 'text-ide-muted hover:text-ide-text hover:bg-ide-panel/50'
                }`}
              >
                {item.icon}
                <span>{item.label}</span>
              </button>
            ))}
          </nav>
        </div>

        {/* Pro Upgrade Card */}
        <div className="p-4 rounded-2xl bg-ide-sidebar/80 border border-emerald-500/20 text-center mt-6">
          <Sparkles className="w-5 h-5 text-emerald-400 mx-auto mb-1" />
          <p className="text-xs font-bold text-ide-text">Upgrade to PRO</p>
          <p className="text-[10px] text-ide-muted mt-0.5 font-normal">Unlimited energy & AI Tutor hints</p>
          <button
            onClick={onOpenPricing}
            className="w-full mt-3 py-2 rounded-xl bg-gradient-to-r from-emerald-400 via-teal-400 to-emerald-300 hover:from-emerald-300 hover:to-teal-300 text-slate-950 font-bold text-xs transition-all shadow-sm"
          >
            Become Pro
          </button>
        </div>
      </aside>

      {/* Main Center Module Grid Area */}
      <main className="flex-1 p-8 overflow-y-auto h-full pb-32">
        <div className="max-w-4xl mx-auto">
          {/* Header */}
          <div className="flex flex-wrap items-center justify-between gap-4 mb-8 bg-ide-panel/80 p-6 rounded-3xl border border-ide-border/80">
            <div>
              <span className="text-xs font-semibold text-emerald-400 uppercase tracking-wider block">
                Python Skill Path · Section 1
              </span>
              <h1 className="text-3xl font-bold text-ide-text mt-1">Python Foundations Curriculum</h1>
            </div>

            <div className="flex items-center gap-2">
              <button
                onClick={() => setViewMode('grid')}
                className={`px-3 py-1.5 rounded-xl text-xs font-medium transition-all ${
                  viewMode === 'grid' ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30' : 'text-ide-muted hover:text-ide-text'
                }`}
              >
                Grid View
              </button>
              <button
                onClick={() => setViewMode('list')}
                className={`px-3 py-1.5 rounded-xl text-xs font-medium transition-all ${
                  viewMode === 'list' ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30' : 'text-ide-muted hover:text-ide-text'
                }`}
              >
                List View
              </button>
            </div>
          </div>

          {/* Modules List / Grid Display */}
          <div className="space-y-6">
            {modules.map((mod) => (
              <div
                key={mod.id}
                className="rounded-3xl bg-ide-panel/80 border border-ide-border/80 p-6 shadow-xl transition-all hover:border-ide-border"
              >
                <div className="flex flex-wrap items-center justify-between gap-4 pb-4 border-b border-ide-border/80 mb-6">
                  <div>
                    <div className="flex items-center gap-2 mb-1">
                      <span className={`px-2.5 py-0.5 rounded-full text-[10px] font-medium uppercase tracking-wider ${
                        mod.status === 'completed'
                          ? 'bg-emerald-500/10 text-emerald-300 border border-emerald-500/20'
                          : mod.status === 'active'
                          ? 'bg-teal-500/10 text-teal-300 border border-teal-500/20'
                          : 'bg-ide-sidebar text-slate-500 border border-ide-border'
                      }`}>
                        {mod.status}
                      </span>
                      <span className="text-xs text-ide-muted font-medium">{mod.progress}% Completed</span>
                    </div>
                    <h2 className="text-xl font-bold text-ide-text">{mod.title}</h2>
                    <p className="text-xs text-ide-muted mt-1">{mod.desc}</p>
                  </div>

                  {/* Module Progress Bar */}
                  <div className="w-32">
                    <div className="w-full bg-ide-bg h-2 rounded-full overflow-hidden border border-ide-border">
                      <div
                        className="bg-gradient-to-r from-emerald-400 via-teal-400 to-emerald-300 h-full transition-all duration-500"
                        style={{ width: `${mod.progress}%` }}
                      />
                    </div>
                  </div>
                </div>

                {/* Lessons Grid / List inside Module */}
                <div className={viewMode === 'grid' ? 'grid md:grid-cols-2 gap-4' : 'space-y-3'}>
                  {mod.lessons.map((lesson) => (
                    <div
                      key={lesson.id}
                      className={`p-4 rounded-2xl border transition-all flex items-center justify-between gap-4 ${
                        lesson.status === 'completed'
                          ? 'bg-ide-bg/60 border-ide-border/80 text-ide-text'
                          : lesson.status === 'active'
                          ? 'bg-emerald-500/10 border-emerald-500/40 text-ide-text ring-1 ring-emerald-500/20'
                          : 'bg-ide-bg/30 border-ide-border/40 text-slate-500 opacity-60'
                      }`}
                    >
                      <div className="flex items-center gap-3">
                        {lesson.status === 'completed' ? (
                          <CheckCircle2 className="w-5 h-5 text-emerald-400 shrink-0" />
                        ) : lesson.status === 'active' ? (
                          <PlayCircle className="w-5 h-5 text-emerald-300 shrink-0 animate-pulse" />
                        ) : (
                          <Lock className="w-4 h-4 text-slate-600 shrink-0" />
                        )}

                        <div>
                          <h4 className="text-xs font-bold text-ide-text mb-0.5">{lesson.title}</h4>
                          <p className="text-[11px] text-ide-muted font-normal">{lesson.desc}</p>
                        </div>
                      </div>

                      {lesson.status !== 'locked' && (
                        <button
                          onClick={() => onStartLesson(lesson)}
                          className="px-3.5 py-1.5 rounded-xl bg-ide-sidebar hover:bg-gradient-to-r hover:from-emerald-400 hover:to-teal-400 hover:text-slate-950 text-ide-text font-bold text-[11px] transition-all shrink-0 active:scale-95 shadow-sm"
                        >
                          {lesson.status === 'active' ? 'Continue' : 'Review'}
                        </button>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      </main>

      {/* Right Sidebar Widgets */}
      <aside className="w-80 bg-ide-panel/90 p-6 space-y-6 shrink-0 overflow-y-auto border-l border-ide-border/80 h-full pb-32">
        {/* Top Gamification Header Badges */}
        <div className="flex items-center justify-between text-xs font-semibold bg-ide-bg p-3 rounded-2xl border border-ide-border">
          <span className="flex items-center gap-1.5 text-rose-400">
            <Flame className="w-4 h-4 fill-rose-400" />
            <span>2 Day Streak</span>
          </span>
          <span className="flex items-center gap-1.5 text-emerald-400">
            <Gem className="w-4 h-4 text-emerald-400 fill-emerald-400" />
            <span>76 XP</span>
          </span>
          <span className="flex items-center gap-1.5 text-teal-300">
            <Zap className="w-4 h-4 text-teal-300 fill-teal-300" />
            <span>0</span>
          </span>
        </div>

        {/* Level Progress Card */}
        <div className="p-5 rounded-2xl bg-ide-bg border border-ide-border">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-bold text-ide-text">Level 5 · Kilo</span>
            <span className="text-[10px] text-emerald-400 font-medium">46 XP to go</span>
          </div>
          <div className="w-full bg-ide-panel h-2 rounded-full overflow-hidden border border-ide-border">
            <div className="bg-gradient-to-r from-emerald-400 via-teal-400 to-emerald-300 h-full w-[65%]" />
          </div>
        </div>

        {/* Leaderboard Widget */}
        <div className="p-5 rounded-2xl bg-ide-bg border border-ide-border space-y-3">
          <div className="flex items-center justify-between">
            <h4 className="text-xs font-bold text-ide-text">Weekly Leaderboard</h4>
            <span className="text-[11px] text-emerald-400 font-medium hover:underline cursor-pointer">View</span>
          </div>
          <div className="p-4 rounded-xl bg-ide-panel/60 border border-ide-border/80 text-center">
            <Trophy className="w-7 h-7 text-emerald-400 mx-auto mb-2" />
            <p className="text-xs font-medium text-ide-text">Earn 50 XP to enter this week's top coders list!</p>
          </div>
        </div>

        {/* Daily Missions Widget */}
        <div className="p-5 rounded-2xl bg-ide-bg border border-ide-border space-y-3">
          <h4 className="text-xs font-bold text-ide-text">Daily Learning Missions</h4>
          <div className="space-y-2 text-xs">
            <div className="p-3 rounded-xl bg-ide-panel/60 border border-ide-border flex items-center justify-between">
              <span className="text-ide-text">Complete 1 coding exercise</span>
              <span className="text-emerald-400 font-bold">1/1 ✅</span>
            </div>
            <div className="p-3 rounded-xl bg-ide-panel/60 border border-ide-border flex items-center justify-between text-ide-muted">
              <span>Earn 50 XP today</span>
              <span className="font-medium">0/50</span>
            </div>
          </div>
        </div>
      </aside>
    </div>
  );
}

