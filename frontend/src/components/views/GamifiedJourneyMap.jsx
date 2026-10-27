import React, { useState, useEffect } from 'react';
import { 
  BookOpen, Dumbbell, Palette, Flag, Trophy, User, 
  Flame, Gem, Zap, Check, Lock, ArrowRight, Sparkles, Layers, CheckCircle2, PlayCircle, Code2, Globe, Cpu, Bot
} from 'lucide-react';
import { API_BASE_URL } from '../../api/agentApi';

export default function GamifiedJourneyMap({ 
  onStartLesson, 
  onOpenPricing, 
  userStats, 
  onSelectTab,
  initialTrack = 'python-developer' 
}) {
  const [activeSideTab, setActiveSideTab] = useState('journey');
  const [viewMode, setViewMode] = useState('grid');
  const [journeys, setJourneys] = useState([]);
  const [activeTrackId, setActiveTrackId] = useState(initialTrack);
  const [loading, setLoading] = useState(true);

  const userRole = localStorage.getItem('user_role') || '';
  const userPlan = localStorage.getItem('user_plan') || 'free';
  const isProOrAdmin = userRole === 'admin' || userPlan === 'pro' || userPlan === 'lifetime' || userPlan === 'pro_monthly' || userPlan === 'pro_annual';

  useEffect(() => {
    fetch(`${API_BASE_URL}/api/journeys`)
      .then(res => res.json())
      .then(data => {
        if (data.journeys && Array.isArray(data.journeys)) {
          setJourneys(data.journeys);
        }
        setLoading(false);
      })
      .catch(err => {
        console.error('Failed fetching curriculum journeys:', err);
        setLoading(false);
      });
  }, []);

  // Find currently active journey track
  const currentJourney = journeys.find(j => j.id === activeTrackId) || journeys[0] || null;
  const modules = currentJourney?.courses || [];

  const sideNavItems = [
    { id: 'journey', label: 'Modules Path', icon: <Layers className="w-4 h-4 text-emerald-400" /> },
    { id: 'practice', label: 'Practice Problems', icon: <Dumbbell className="w-4 h-4 text-teal-300" /> },
    { id: 'projects', label: 'Projects', icon: <Palette className="w-4 h-4 text-emerald-300" /> },
    { id: 'missions', label: 'Daily Missions', icon: <Flag className="w-4 h-4 text-rose-400" /> },
    { id: 'leaderboard', label: 'Leaderboard', icon: <Trophy className="w-4 h-4 text-emerald-400" /> },
    { id: 'profile', label: 'Profile', icon: <User className="w-4 h-4 text-teal-400" /> }
  ];

  const handleSideNavClick = (id) => {
    setActiveSideTab(id);
    if (id === 'practice' && onSelectTab) {
      onSelectTab('practice');
    }
  };

  return (
    <div className="h-full w-full bg-ide-bg text-slate-100 flex font-sans select-none overflow-hidden">
      {/* Left Navigation Sidebar */}
      <aside className="w-64 bg-slate-900/90 border-r border-slate-800/80 p-4 flex flex-col justify-between shrink-0 h-full overflow-y-auto pb-16">
        <div className="space-y-6">
          {/* Brand */}
          <div className="flex items-center gap-3 px-2">
            <div className="w-9 h-9 rounded-2xl bg-gradient-to-tr from-emerald-500 via-teal-400 to-emerald-300 flex items-center justify-center font-black text-xs text-slate-950 shadow-md shadow-emerald-500/20">
              PCA
            </div>
            <div>
              <span className="font-bold text-sm bg-gradient-to-r from-white via-slate-100 to-emerald-300 bg-clip-text text-transparent block">
                Prasana Code AI
              </span>
              <span className="text-[10px] text-emerald-400 font-semibold tracking-wide">
                Interactive Learning
              </span>
            </div>
          </div>

          {/* Navigation Items */}
          <nav className="space-y-1">
            {sideNavItems.map(item => (
              <button
                key={item.id}
                onClick={() => handleSideNavClick(item.id)}
                className={`w-full flex items-center gap-3 px-3.5 py-2.5 rounded-xl font-medium text-xs transition-all ${
                  activeSideTab === item.id
                    ? 'bg-emerald-500/10 text-emerald-300 border border-emerald-500/30 font-semibold shadow-sm'
                    : 'text-slate-400 hover:text-slate-100 hover:bg-slate-800/50'
                }`}
              >
                {item.icon}
                <span>{item.label}</span>
              </button>
            ))}
          </nav>
        </div>

        {/* Pro Upgrade Card */}
        {isProOrAdmin ? (
          <div className="p-4 rounded-2xl bg-slate-950/80 border border-emerald-500/30 text-center mt-6 shadow-lg shadow-emerald-950/30">
            <Sparkles className="w-5 h-5 text-emerald-400 mx-auto mb-1 animate-pulse" />
            <p className="text-xs font-bold text-white">{userRole === 'admin' ? 'Admin Access Active' : 'PRO Member Active'}</p>
            <p className="text-[10px] text-emerald-400 mt-0.5 font-normal">Unlimited energy & AI hints</p>
          </div>
        ) : (
          <div className="p-4 rounded-2xl bg-slate-950/80 border border-emerald-500/30 text-center mt-6 shadow-lg shadow-emerald-950/30">
            <Sparkles className="w-5 h-5 text-emerald-400 mx-auto mb-1 animate-pulse" />
            <p className="text-xs font-bold text-white">Upgrade to PRO</p>
            <p className="text-[10px] text-slate-400 mt-0.5 font-normal">Unlimited energy & AI Tutor hints</p>
            <button
              onClick={onOpenPricing}
              className="w-full mt-3 py-2 rounded-xl bg-gradient-to-r from-emerald-400 via-teal-400 to-emerald-300 hover:from-emerald-300 hover:to-teal-300 text-slate-950 font-bold text-xs transition-all shadow-md active:scale-95"
            >
              Become Pro
            </button>
          </div>
        )}
      </aside>

      {/* Main Center Module Grid Area */}
      <main className="flex-1 p-6 md:p-8 overflow-y-auto h-full pb-32">
        <div className="max-w-5xl mx-auto space-y-8">
          
          {/* Track Switcher Bar */}
          <div className="bg-slate-900/90 p-3 rounded-2xl border border-slate-800/90 shadow-xl backdrop-blur-md">
            <div className="flex items-center gap-2 overflow-x-auto pb-1 no-scrollbar">
              <span className="text-xs font-bold uppercase tracking-wider text-slate-400 px-3 whitespace-nowrap">
                Tracks:
              </span>
              {journeys.map(j => {
                const isActive = (currentJourney?.id === j.id);
                return (
                  <button
                    key={j.id}
                    onClick={() => setActiveTrackId(j.id)}
                    className={`flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-semibold whitespace-nowrap transition-all duration-200 ${
                      isActive
                        ? 'bg-gradient-to-r from-emerald-400 via-teal-400 to-emerald-300 text-slate-950 shadow-md shadow-emerald-500/20 font-bold'
                        : 'bg-slate-800/60 hover:bg-slate-800 text-slate-300 border border-slate-700/60'
                    }`}
                  >
                    <span>{j.icon}</span>
                    <span>{j.title}</span>
                    <span className={`text-[10px] px-1.5 py-0.2 rounded-full ${
                      isActive ? 'bg-slate-950/20 text-slate-950 font-bold' : 'bg-slate-700/60 text-slate-300'
                    }`}>
                      {j.totalLessons || j.courses?.reduce((acc, m) => acc + (m.lessons?.length || 0), 0) || 0}
                    </span>
                  </button>
                );
              })}
            </div>
          </div>

          {/* Track Header Card */}
          <div className="relative overflow-hidden bg-gradient-to-br from-slate-900 via-slate-900/90 to-emerald-950/40 p-6 md:p-8 rounded-3xl border border-emerald-500/20 shadow-2xl">
            <div className="flex flex-wrap items-center justify-between gap-4">
              <div>
                <div className="flex items-center gap-2 mb-2">
                  <span className="text-2xl">{currentJourney?.icon || '🐍'}</span>
                  <span className="px-3 py-1 rounded-full text-[11px] font-bold bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 uppercase tracking-wider">
                    {currentJourney?.badge || 'Skill Track'}
                  </span>
                  <span className="text-xs text-slate-400 font-medium">
                    {currentJourney?.estimatedHours || 12} Hours of hands-on coding
                  </span>
                </div>
                <h1 className="text-3xl md:text-4xl font-extrabold text-white tracking-tight">
                  {currentJourney?.title || 'Learning Curriculum'}
                </h1>
                <p className="text-sm text-slate-300 max-w-2xl mt-2 leading-relaxed">
                  {currentJourney?.description || 'Follow hands-on interactive lessons with real-time test execution and Telugu/English conceptual guidance.'}
                </p>
              </div>

              <div className="flex items-center gap-2">
                <button
                  onClick={() => setViewMode('grid')}
                  className={`px-3.5 py-2 rounded-xl text-xs font-semibold transition-all ${
                    viewMode === 'grid' 
                      ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 shadow-sm' 
                      : 'text-slate-400 hover:text-slate-200 bg-slate-800/40 border border-slate-700/40'
                  }`}
                >
                  Grid View
                </button>
                <button
                  onClick={() => setViewMode('list')}
                  className={`px-3.5 py-2 rounded-xl text-xs font-semibold transition-all ${
                    viewMode === 'list' 
                      ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 shadow-sm' 
                      : 'text-slate-400 hover:text-slate-200 bg-slate-800/40 border border-slate-700/40'
                  }`}
                >
                  List View
                </button>
              </div>
            </div>
          </div>

          {/* Modules List */}
          {loading ? (
            <div className="text-center py-20 text-slate-400 font-medium">Loading track curriculum...</div>
          ) : (
            <div className="space-y-6">
              {modules.map((mod, modIdx) => (
                <div
                  key={mod.id || modIdx}
                  className="rounded-3xl bg-slate-900/90 border border-slate-800/90 hover:border-slate-700 p-6 md:p-8 shadow-xl transition-all"
                >
                  {/* Module Header */}
                  <div className="flex flex-wrap items-center justify-between gap-4 pb-5 border-b border-slate-800/80 mb-6">
                    <div>
                      <div className="flex items-center gap-2.5 mb-1.5">
                        <span className="px-3 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider bg-emerald-500/10 text-emerald-300 border border-emerald-500/20">
                          Module {modIdx + 1}
                        </span>
                        <span className="text-xs text-slate-400 font-medium">
                          {mod.lessons?.length || 0} Coding Challenges
                        </span>
                      </div>
                      <h2 className="text-xl md:text-2xl font-bold text-white tracking-tight">{mod.title}</h2>
                      <p className="text-xs text-slate-300 mt-1 leading-relaxed max-w-2xl">{mod.desc || mod.description}</p>
                    </div>

                    <div className="text-right">
                      <span className="text-xs font-bold text-emerald-400">
                        {mod.lessons?.length || 0} Lessons
                      </span>
                    </div>
                  </div>

                  {/* Lessons Inside Module */}
                  <div className={viewMode === 'grid' ? 'grid md:grid-cols-2 gap-4' : 'space-y-3'}>
                    {mod.lessons?.map((lesson, lIdx) => (
                      <div
                        key={lesson.id || lIdx}
                        onClick={() => onStartLesson(lesson)}
                        className="p-5 rounded-2xl border border-slate-800 bg-slate-950 hover:bg-slate-900 hover:border-emerald-500/50 transition-all duration-200 flex flex-col justify-between gap-4 group shadow-md cursor-pointer"
                      >
                        <div>
                          <div className="flex items-center justify-between gap-2 mb-2">
                            <span className="px-2.5 py-0.5 rounded-md text-[10px] font-bold uppercase tracking-wide bg-slate-800 text-slate-300 border border-slate-700">
                              Lesson {lIdx + 1}
                            </span>
                            <span className="text-[11px] font-bold text-emerald-400 flex items-center gap-1">
                              +{lesson.xp || 10} XP
                            </span>
                          </div>

                          <h3 className="text-base font-bold text-white group-hover:text-emerald-300 transition-colors">
                            {lesson.title}
                          </h3>

                          {lesson.title_te && (
                            <p className="text-xs font-semibold text-teal-300 mt-0.5">
                              {lesson.title_te}
                            </p>
                          )}

                          <p className="text-xs md:text-sm text-slate-200 mt-2 leading-relaxed line-clamp-3">
                            {lesson.instructions_te || lesson.instructions || lesson.desc || "Click to solve the interactive coding challenge in the IDE."}
                          </p>
                        </div>

                        <div className="pt-3 border-t border-slate-800 flex items-center justify-between">
                          <span className="text-[11px] text-slate-400 font-mono capitalize">
                            Language: <strong className="text-slate-200">{lesson.language || 'python'}</strong>
                          </span>

                          <button
                            onClick={(e) => {
                              e.stopPropagation();
                              onStartLesson(lesson);
                            }}
                            className="px-4 py-2 rounded-xl bg-gradient-to-r from-emerald-500/20 via-teal-500/20 to-emerald-500/20 hover:from-emerald-400 hover:via-teal-400 hover:to-emerald-300 hover:text-slate-950 text-emerald-300 border border-emerald-500/40 hover:border-transparent font-bold text-xs transition-all duration-200 active:scale-95 flex items-center gap-1.5 shadow-sm"
                          >
                            <span>Start Challenge</span>
                            <ArrowRight className="w-3.5 h-3.5" />
                          </button>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          )}

        </div>
      </main>

      {/* Right Sidebar Widgets */}
      <aside className="w-80 bg-slate-900/90 p-6 space-y-6 shrink-0 overflow-y-auto border-l border-slate-800/80 h-full pb-32">
        {/* Top Badges */}
        <div className="flex items-center justify-between text-xs font-semibold bg-slate-950/80 p-3.5 rounded-2xl border border-slate-800">
          <span className="flex items-center gap-1.5 text-rose-400">
            <Flame className="w-4 h-4 fill-rose-400" />
            <span>{userStats?.streak || 2} Day Streak</span>
          </span>
          <span className="flex items-center gap-1.5 text-emerald-400">
            <Gem className="w-4 h-4 text-emerald-400 fill-emerald-400" />
            <span>{userStats?.xp || 76} XP</span>
          </span>
          <span className="flex items-center gap-1.5 text-teal-300">
            <Zap className="w-4 h-4 text-teal-300 fill-teal-300" />
            <span>{isProOrAdmin ? (userRole === 'admin' ? 'Unlimited (Admin)' : 'Unlimited (Pro)') : '5 Energy'}</span>
          </span>
        </div>

        {/* Level Progression */}
        <div className="p-5 rounded-3xl bg-slate-950/60 border border-slate-800 space-y-3">
          <div className="flex items-center justify-between text-xs">
            <span className="font-bold text-white">Level 5 · Kilo Coder</span>
            <span className="text-slate-400 font-mono">46 XP to go</span>
          </div>
          <div className="w-full bg-slate-800 h-2.5 rounded-full overflow-hidden border border-slate-700/60">
            <div className="bg-gradient-to-r from-emerald-400 to-teal-400 h-full rounded-full" style={{ width: '65%' }} />
          </div>
        </div>

        {/* Weekly Leaderboard */}
        <div className="p-5 rounded-3xl bg-slate-950/60 border border-slate-800 space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="font-bold text-xs uppercase tracking-wider text-slate-400">Weekly Leaderboard</h3>
            <span className="text-xs text-emerald-400 font-semibold cursor-pointer hover:underline">View</span>
          </div>
          <div className="text-center py-6 border border-dashed border-slate-800 rounded-2xl">
            <Trophy className="w-8 h-8 text-emerald-400 mx-auto mb-2" />
            <p className="text-xs font-semibold text-slate-300">Earn 50 XP to enter this week's top coders list!</p>
          </div>
        </div>

        {/* Daily Learning Missions */}
        <div className="p-5 rounded-3xl bg-slate-950/60 border border-slate-800 space-y-3">
          <h3 className="font-bold text-xs uppercase tracking-wider text-slate-400">Daily Missions</h3>
          <div className="space-y-2.5">
            <div className="flex items-center justify-between text-xs p-3 rounded-xl bg-slate-900 border border-slate-800">
              <span className="text-slate-200">Complete 1 coding exercise</span>
              <span className="text-emerald-400 font-bold">1/1 ✓</span>
            </div>
            <div className="flex items-center justify-between text-xs p-3 rounded-xl bg-slate-900 border border-slate-800">
              <span className="text-slate-200">Earn 50 XP today</span>
              <span className="text-slate-400 font-mono">0/50</span>
            </div>
          </div>
        </div>
      </aside>
    </div>
  );
}
