import React, { useState, useEffect } from 'react';
import { 
  BookOpen, Dumbbell, Palette, Flag, Trophy, User, 
  Flame, Gem, Zap, Check, Lock, ArrowRight, Sparkles, Layers, CheckCircle2, PlayCircle, 
  Code2, Globe, Cpu, Bot, Printer, Download, X, ShieldCheck, Award, Star, ExternalLink
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
  const [showInvoiceModal, setShowInvoiceModal] = useState(false);
  const [claimedMissions, setClaimedMissions] = useState({});

  const userEmail = localStorage.getItem('user_email') || 'student@prasana-code.ai';
  const userRole = localStorage.getItem('user_role') || 'student';
  const userPlan = localStorage.getItem('user_plan') || 'free';
  const isProOrAdmin = userRole === 'admin' || userPlan === 'pro' || userPlan === 'lifetime' || userPlan === 'pro_monthly' || userPlan === 'pro_annual';

  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'Escape') setShowInvoiceModal(false);
    };
    if (showInvoiceModal) {
      window.addEventListener('keydown', handleKeyDown);
      return () => window.removeEventListener('keydown', handleKeyDown);
    }
  }, [showInvoiceModal]);

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
  const allCurrentLessons = modules.flatMap(m => m.lessons || []);

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

  const handleClaimMission = (missionId, xp) => {
    setClaimedMissions(prev => ({ ...prev, [missionId]: true }));
  };

  // Portfolio Projects definitions
  const portfolioProjects = [
    {
      id: 'proj-01',
      title: 'Full-Stack AI Code Explainer & Reviewer',
      tech: ['Python', 'FastAPI', 'React', 'Ollama LLM'],
      difficulty: 'Intermediate',
      xp: 150,
      hours: '4-6 Hours',
      description: 'Build a production-grade code analysis microservice that ingests code snippets, generates AST trees, and feeds them to an LLM for real-time explanations and lint fixes.',
      topics: ['REST APIs', 'Async/Await', 'Prompt Engineering', 'Error Handling']
    },
    {
      id: 'proj-02',
      title: 'CLI Task & Habit Manager with SQLite',
      tech: ['Python', 'OOP', 'SQLite3', 'Rich CLI'],
      difficulty: 'Beginner-Friendly',
      xp: 100,
      hours: '3-4 Hours',
      description: 'Create an interactive terminal productivity application with persistent relational data, streak tracking, and ANSI-colored dashboard tables.',
      topics: ['Class Hierarchies', 'CRUD Operations', 'SQL Schemas', 'Command Arguments']
    },
    {
      id: 'proj-03',
      title: 'High-Performance Concurrency LRU Cache',
      tech: ['C++', 'STL', 'Pointers', 'Hash Map'],
      difficulty: 'Advanced',
      xp: 200,
      hours: '6-8 Hours',
      description: 'Design and implement an in-memory Least Recently Used (LRU) cache with O(1) lookup and eviction using Doubly Linked Lists and std::unordered_map.',
      topics: ['Pointers & References', 'Memory Layout', 'Time Complexity', 'Double Pointers']
    },
    {
      id: 'proj-04',
      title: 'Realtime Algorithmic Sorting Visualizer',
      tech: ['JavaScript', 'HTML5 Canvas', 'CSS3', 'Algorithms'],
      difficulty: 'Intermediate',
      xp: 120,
      hours: '3-5 Hours',
      description: 'An interactive web canvas that animates Bubble Sort, Merge Sort, and Quick Sort step-by-step with sound frequency feedback and speed controls.',
      topics: ['DOM Manipulation', 'Event Loop', 'Recursion', 'Canvas 2D']
    }
  ];

  // Leaderboard data
  const leaderboardUsers = [
    { rank: 1, name: 'Venkata Sai', xp: 2450, streak: 28, badge: 'Python Architect', avatar: '🥇' },
    { rank: 2, name: 'Ananya Sharma', xp: 2180, streak: 24, badge: 'DSA Master', avatar: '🥈' },
    { rank: 3, name: 'Karthik Reddy', xp: 1940, streak: 19, badge: 'Full-Stack Wizard', avatar: '🥉' },
    { rank: 4, name: 'Sneha Patel', xp: 1650, streak: 15, badge: 'Algorithm Ace', avatar: '⚡' },
    { rank: 5, name: 'Rohit Verma', xp: 1420, streak: 12, badge: 'Code Ninja', avatar: '🚀' },
    { rank: 6, name: 'Deepa Rao', xp: 1210, streak: 10, badge: 'Bug Crusher', avatar: '🎯' },
    { rank: 7, name: 'Arjun Das', xp: 980, streak: 8, badge: 'Telugu Scholar', avatar: '💡' },
    { rank: 8, name: 'Pooja Iyer', xp: 820, streak: 6, badge: 'Speed Demon', avatar: '🔥' },
    { rank: 9, name: 'Manoj Kumar', xp: 640, streak: 4, badge: 'Fast Thinker', avatar: '🌟' },
    { rank: 10, name: 'Harsha Vardhan', xp: 480, streak: 3, badge: 'Rising Star', avatar: '✨' }
  ];

  return (
    <div className="h-full w-full bg-ide-bg text-slate-100 flex font-sans select-none overflow-hidden relative">
      
      {/* GST Tax Invoice & Official Receipt Modal */}
      {showInvoiceModal && (
        <div className="fixed inset-0 z-50 bg-black/85 backdrop-blur-md flex items-center justify-center p-4 overflow-y-auto">
          <div className="w-full max-w-2xl bg-white text-slate-900 rounded-3xl p-8 shadow-2xl relative border border-slate-200">
            {/* Modal Controls */}
            <div className="flex items-center justify-between border-b border-slate-200 pb-4 mb-6">
              <div className="flex items-center gap-2">
                <div className="w-8 h-8 rounded-xl bg-emerald-600 text-white flex items-center justify-center font-bold text-xs">
                  PCA
                </div>
                <div>
                  <h3 className="font-extrabold text-base text-slate-900">Official GST Tax Invoice</h3>
                  <p className="text-[11px] text-slate-500">Government of India Compliant GST Receipt</p>
                </div>
              </div>
              <div className="flex items-center gap-2">
                <button
                  onClick={() => window.print()}
                  className="px-3.5 py-1.5 rounded-xl bg-slate-900 hover:bg-slate-800 text-white font-bold text-xs flex items-center gap-1.5 transition-all shadow-sm"
                  title="Print or Save as PDF"
                >
                  <Printer className="w-3.5 h-3.5" />
                  <span>Print / Save PDF</span>
                </button>
                <button
                  onClick={() => setShowInvoiceModal(false)}
                  className="p-1.5 rounded-xl text-slate-400 hover:text-slate-700 hover:bg-slate-100"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>
            </div>

            {/* Printable Invoice Body */}
            <div className="space-y-6 text-xs text-slate-700 print:text-black">
              {/* Header Info */}
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <p className="font-bold text-sm text-slate-900">Prasana Code AI Technologies Pvt Ltd</p>
                  <p className="text-[11px] text-slate-500 mt-0.5">Hyderabad, Telangana - 500081, India</p>
                  <p className="text-[11px] font-mono mt-1"><strong>GSTIN:</strong> 37AAECP1234F1Z8</p>
                  <p className="text-[11px] font-mono"><strong>PAN:</strong> AAECP1234F</p>
                  <p className="text-[11px]"><strong>Email:</strong> billing@prasana-code.ai</p>
                </div>
                <div className="text-right">
                  <span className="inline-block px-3 py-1 rounded-full text-[10px] font-bold bg-emerald-100 text-emerald-800 mb-2">
                    PAID IN FULL ✓
                  </span>
                  <p className="font-mono text-xs"><strong>Invoice #:</strong> PCA-INV-2026-9842</p>
                  <p className="text-[11px]"><strong>Date:</strong> October 28, 2026</p>
                  <p className="text-[11px]"><strong>Payment Mode:</strong> Razorpay / UPI Instant</p>
                  <p className="text-[11px]"><strong>Place of Supply:</strong> 36-Telangana</p>
                </div>
              </div>

              {/* Billed To */}
              <div className="p-3.5 rounded-2xl bg-slate-50 border border-slate-200">
                <span className="text-[10px] uppercase font-bold text-slate-400 tracking-wider block mb-1">
                  Billed To (Customer Details):
                </span>
                <p className="font-bold text-slate-800">{userEmail.split('@')[0].toUpperCase()}</p>
                <p className="text-slate-600">{userEmail}</p>
                <p className="text-slate-500 text-[11px]">Account Type: {userRole.toUpperCase()} · Plan: {userPlan.toUpperCase()}</p>
              </div>

              {/* Line Items Table */}
              <table className="w-full text-left border-collapse border border-slate-200 rounded-xl overflow-hidden">
                <thead>
                  <tr className="bg-slate-100 text-slate-700 font-bold border-b border-slate-200">
                    <th className="p-2.5">Item Description</th>
                    <th className="p-2.5">SAC / HSN</th>
                    <th className="p-2.5 text-center">Qty</th>
                    <th className="p-2.5 text-right">Taxable Amount</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-200 font-medium">
                  <tr>
                    <td className="p-2.5">
                      <p className="font-bold text-slate-900">Prasana Code AI Pro — Lifetime Membership</p>
                      <p className="text-[10px] text-slate-500">Unlimited sandbox runs, AI tutor hints, bilingual lessons & verifiable certifications</p>
                    </td>
                    <td className="p-2.5 font-mono">998431</td>
                    <td className="p-2.5 text-center">1</td>
                    <td className="p-2.5 text-right font-mono">₹2,541.53</td>
                  </tr>
                </tbody>
              </table>

              {/* Tax Breakup */}
              <div className="flex justify-end">
                <div className="w-64 space-y-1.5 text-xs">
                  <div className="flex justify-between py-1 border-b border-slate-100">
                    <span className="text-slate-500">Subtotal:</span>
                    <span className="font-mono">₹2,541.53</span>
                  </div>
                  <div className="flex justify-between py-1 border-b border-slate-100">
                    <span className="text-slate-500">CGST (9%):</span>
                    <span className="font-mono">₹228.74</span>
                  </div>
                  <div className="flex justify-between py-1 border-b border-slate-100">
                    <span className="text-slate-500">SGST (9%):</span>
                    <span className="font-mono">₹228.74</span>
                  </div>
                  <div className="flex justify-between py-2 border-t-2 border-slate-900 font-extrabold text-sm text-slate-900">
                    <span>Total Amount Paid:</span>
                    <span className="font-mono text-emerald-700">₹2,999.00</span>
                  </div>
                </div>
              </div>

              {/* Footer Note */}
              <div className="border-t border-slate-200 pt-3 text-[10px] text-slate-400 flex items-center justify-between">
                <span>This is an electronically generated invoice valid without physical signature.</span>
                <span className="flex items-center gap-1 text-emerald-600 font-bold">
                  <ShieldCheck className="w-3.5 h-3.5" />
                  <span>Authorized Official Receipt</span>
                </span>
              </div>
            </div>
          </div>
        </div>
      )}

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

      {/* Main Center Area */}
      <main className="flex-1 p-6 md:p-8 overflow-y-auto h-full pb-32">
        <div className="max-w-5xl mx-auto space-y-8">
          
          {/* TAB 1: CURRICULUM JOURNEY */}
          {activeSideTab === 'journey' && (
            <>
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
                          <h2 className="text-xl md:text-2xl font-bold text-white tracking-tight">
                            {mod.title}
                          </h2>
                          <p className="text-xs text-slate-400 mt-1">
                            {mod.desc || mod.description || 'Master key principles through interactive test-driven coding.'}
                          </p>
                        </div>
                      </div>

                      {/* Lessons Grid */}
                      <div className={`grid gap-4 ${viewMode === 'grid' ? 'grid-cols-1 md:grid-cols-2' : 'grid-cols-1'}`}>
                        {(mod.lessons || []).map((lesson, lIdx) => (
                          <div
                            key={lesson.id || lIdx}
                            onClick={() => onStartLesson(lesson, allCurrentLessons)}
                            className="group relative p-5 rounded-2xl bg-slate-950/70 border border-slate-800/90 hover:border-emerald-500/50 hover:bg-slate-900/90 transition-all duration-200 cursor-pointer flex flex-col justify-between shadow-md"
                          >
                            <div>
                              <div className="flex items-center justify-between gap-2 mb-2">
                                <span className="px-2.5 py-0.5 rounded-full text-[10px] font-mono font-bold bg-slate-800 text-slate-300 border border-slate-700/60">
                                  #{lIdx + 1}
                                </span>
                                <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-500/10 text-emerald-300 border border-emerald-500/20 flex items-center gap-1">
                                  <Gem className="w-3 h-3 text-emerald-400" />
                                  <span>+{lesson.xp || 10} XP</span>
                                </span>
                              </div>

                              <h3 className="font-bold text-sm text-white group-hover:text-emerald-300 transition-colors">
                                {lesson.title}
                              </h3>
                              {lesson.title_te && (
                                <p className="text-xs text-emerald-400/90 font-medium mt-0.5">
                                  {lesson.title_te}
                                </p>
                              )}
                              <p className="text-xs text-slate-400 mt-2 line-clamp-2 leading-relaxed">
                                {lesson.instructions || lesson.description || 'Complete the exercise to pass all unit test cases.'}
                              </p>
                            </div>

                            <div className="flex items-center justify-between pt-4 mt-4 border-t border-slate-800/60">
                              <span className="text-[11px] font-mono font-bold text-slate-400 capitalize">
                                {lesson.language || 'python'}
                              </span>

                              <button
                                onClick={(e) => {
                                  e.stopPropagation();
                                  onStartLesson(lesson, allCurrentLessons);
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
            </>
          )}

          {/* TAB 2: PORTFOLIO PROJECTS */}
          {activeSideTab === 'projects' && (
            <div className="space-y-6">
              <div className="p-8 rounded-3xl bg-gradient-to-br from-slate-900 via-slate-900/90 to-emerald-950/40 border border-emerald-500/20 shadow-2xl">
                <div className="flex items-center gap-2 mb-2">
                  <Palette className="w-5 h-5 text-emerald-400" />
                  <span className="px-3 py-1 rounded-full text-[11px] font-bold bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 uppercase tracking-wider">
                    Hands-On Engineering
                  </span>
                </div>
                <h1 className="text-3xl font-extrabold text-white">Portfolio Projects & Capstones</h1>
                <p className="text-sm text-slate-300 mt-2 max-w-2xl leading-relaxed">
                  Real-world full-stack and systems projects designed to prove your competency to tech recruiters and engineering leads.
                </p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {portfolioProjects.map(proj => (
                  <div
                    key={proj.id}
                    className="p-6 rounded-3xl bg-slate-900/90 border border-slate-800 hover:border-emerald-500/40 transition-all flex flex-col justify-between shadow-xl"
                  >
                    <div>
                      <div className="flex items-center justify-between gap-2 mb-3">
                        <span className="px-3 py-1 rounded-full text-[10px] font-bold uppercase tracking-wider bg-emerald-500/10 text-emerald-300 border border-emerald-500/20">
                          {proj.difficulty}
                        </span>
                        <div className="flex items-center gap-2 text-xs font-semibold text-slate-400">
                          <span>{proj.hours}</span>
                          <span>·</span>
                          <span className="text-emerald-400 font-bold">+{proj.xp} XP</span>
                        </div>
                      </div>

                      <h2 className="text-lg font-bold text-white mb-2">{proj.title}</h2>
                      <p className="text-xs text-slate-300 leading-relaxed mb-4">{proj.description}</p>

                      <div className="flex flex-wrap gap-1.5 mb-4">
                        {proj.tech.map(t => (
                          <span key={t} className="px-2.5 py-1 rounded-lg bg-slate-950 text-slate-300 font-mono text-[10px] border border-slate-800">
                            {t}
                          </span>
                        ))}
                      </div>
                    </div>

                    <div className="pt-4 border-t border-slate-800 flex items-center justify-between">
                      <div className="flex items-center gap-1.5 text-xs text-slate-400">
                        <Code2 className="w-4 h-4 text-emerald-400" />
                        <span>Interactive Sandbox Ready</span>
                      </div>
                      <button
                        onClick={() => {
                          if (allCurrentLessons.length > 0) {
                            onStartLesson(allCurrentLessons[0], allCurrentLessons);
                          } else {
                            handleSideNavClick('journey');
                          }
                        }}
                        className="px-4 py-2 rounded-xl bg-gradient-to-r from-emerald-400 via-teal-400 to-emerald-300 hover:from-emerald-300 hover:to-teal-300 text-slate-950 font-bold text-xs transition-all shadow-md active:scale-95 flex items-center gap-1.5"
                      >
                        <span>Open Project</span>
                        <ArrowRight className="w-3.5 h-3.5" />
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* TAB 3: DAILY MISSIONS & QUESTS */}
          {activeSideTab === 'missions' && (
            <div className="space-y-6">
              <div className="p-8 rounded-3xl bg-gradient-to-br from-slate-900 via-slate-900/90 to-rose-950/30 border border-rose-500/20 shadow-2xl">
                <div className="flex items-center gap-2 mb-2">
                  <Flag className="w-5 h-5 text-rose-400" />
                  <span className="px-3 py-1 rounded-full text-[11px] font-bold bg-rose-500/10 border border-rose-500/30 text-rose-300 uppercase tracking-wider">
                    Daily Quests
                  </span>
                </div>
                <h1 className="text-3xl font-extrabold text-white">Daily Learning Missions</h1>
                <p className="text-sm text-slate-300 mt-2 max-w-2xl leading-relaxed">
                  Consistent practice builds muscle memory. Complete daily targets to boost your streak, earn gems, and unlock exclusive platform badges.
                </p>
              </div>

              {/* Missions Grid */}
              <div className="space-y-4">
                {[
                  { id: 'm1', title: 'Morning Code Sprint', desc: 'Solve 1 Coding Challenge in any language track', progress: '1/1', completed: true, xp: 25 },
                  { id: 'm2', title: 'Bilingual Deep Dive', desc: 'Read Telugu & English conceptual theory for any lesson', progress: '1/1', completed: true, xp: 20 },
                  { id: 'm3', title: 'Test Perfectionist', desc: 'Pass all unit tests on your first execution run', progress: '2/3', completed: false, xp: 35 },
                  { id: 'm4', title: 'Weekend Track Master', desc: 'Complete 1 full curriculum module', progress: '3/4', completed: false, xp: 75 }
                ].map(quest => (
                  <div
                    key={quest.id}
                    className="p-5 rounded-2xl bg-slate-900/90 border border-slate-800 flex items-center justify-between gap-4 shadow-lg"
                  >
                    <div className="flex items-center gap-4">
                      <div className={`w-11 h-11 rounded-2xl flex items-center justify-center text-lg ${
                        quest.completed ? 'bg-emerald-500/10 border border-emerald-500/30 text-emerald-400' : 'bg-slate-800 text-slate-400'
                      }`}>
                        {quest.completed ? '✓' : '⚡'}
                      </div>
                      <div>
                        <h2 className="font-bold text-sm text-white">{quest.title}</h2>
                        <p className="text-xs text-slate-400 mt-0.5">{quest.desc}</p>
                        <div className="flex items-center gap-2 mt-2">
                          <div className="w-32 bg-slate-800 h-2 rounded-full overflow-hidden">
                            <div 
                              className="bg-emerald-400 h-full rounded-full" 
                              style={{ width: quest.completed ? '100%' : '65%' }} 
                            />
                          </div>
                          <span className="text-[10px] text-slate-400 font-mono">{quest.progress}</span>
                        </div>
                      </div>
                    </div>

                    <div>
                      {claimedMissions[quest.id] ? (
                        <span className="px-4 py-2 rounded-xl bg-slate-800 text-slate-400 font-bold text-xs flex items-center gap-1">
                          <Check className="w-3.5 h-3.5 text-emerald-400" />
                          <span>Claimed</span>
                        </span>
                      ) : quest.completed ? (
                        <button
                          onClick={() => handleClaimMission(quest.id, quest.xp)}
                          className="px-4 py-2 rounded-xl bg-gradient-to-r from-emerald-400 via-teal-400 to-emerald-300 hover:from-emerald-300 hover:to-teal-300 text-slate-950 font-black text-xs transition-all shadow-md active:scale-95 flex items-center gap-1.5"
                        >
                          <Gem className="w-3.5 h-3.5" />
                          <span>Claim +{quest.xp} XP</span>
                        </button>
                      ) : (
                        <button
                          onClick={() => handleSideNavClick('journey')}
                          className="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 font-bold text-xs transition-all"
                        >
                          In Progress
                        </button>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* TAB 4: LEADERBOARD */}
          {activeSideTab === 'leaderboard' && (
            <div className="space-y-6">
              <div className="p-8 rounded-3xl bg-gradient-to-br from-slate-900 via-slate-900/90 to-amber-950/30 border border-amber-500/20 shadow-2xl">
                <div className="flex items-center gap-2 mb-2">
                  <Trophy className="w-5 h-5 text-amber-400" />
                  <span className="px-3 py-1 rounded-full text-[11px] font-bold bg-amber-500/10 border border-amber-500/30 text-amber-300 uppercase tracking-wider">
                    Community Rankings
                  </span>
                </div>
                <h1 className="text-3xl font-extrabold text-white">Top Coder Leaderboard</h1>
                <p className="text-sm text-slate-300 mt-2 max-w-2xl leading-relaxed">
                  Compete with thousands of ambitious software developers across India. Top weekly performers earn official verified certifications and pro swags.
                </p>
              </div>

              {/* Top 3 Podium */}
              <div className="grid grid-cols-3 gap-4 text-center">
                <div className="p-5 rounded-3xl bg-slate-900/90 border border-slate-800 flex flex-col items-center justify-center">
                  <span className="text-3xl mb-1">🥈</span>
                  <p className="text-xs font-bold text-slate-300">Ananya Sharma</p>
                  <p className="text-[11px] text-emerald-400 font-mono font-bold mt-1">2,180 XP</p>
                  <span className="text-[10px] text-slate-400 mt-0.5">Rank #2</span>
                </div>
                <div className="p-6 rounded-3xl bg-gradient-to-b from-amber-500/10 to-slate-900 border border-amber-500/40 flex flex-col items-center justify-center shadow-lg -translate-y-2">
                  <span className="text-4xl mb-1">🥇</span>
                  <p className="text-sm font-black text-amber-300">Venkata Sai</p>
                  <p className="text-xs text-amber-400 font-mono font-bold mt-1">2,450 XP</p>
                  <span className="px-2 py-0.5 rounded-full text-[9px] font-bold bg-amber-500/20 text-amber-300 border border-amber-500/40 mt-1">
                    Week Champion
                  </span>
                </div>
                <div className="p-5 rounded-3xl bg-slate-900/90 border border-slate-800 flex flex-col items-center justify-center">
                  <span className="text-3xl mb-1">🥉</span>
                  <p className="text-xs font-bold text-slate-300">Karthik Reddy</p>
                  <p className="text-[11px] text-emerald-400 font-mono font-bold mt-1">1,940 XP</p>
                  <span className="text-[10px] text-slate-400 mt-0.5">Rank #3</span>
                </div>
              </div>

              {/* Leaderboard Table */}
              <div className="rounded-3xl bg-slate-900/90 border border-slate-800 overflow-hidden shadow-xl">
                <table className="w-full text-left text-xs">
                  <thead className="bg-slate-950/80 text-slate-400 uppercase font-bold text-[10px] tracking-wider border-b border-slate-800">
                    <tr>
                      <th className="p-4">Rank</th>
                      <th className="p-4">Developer</th>
                      <th className="p-4">Tier Badge</th>
                      <th className="p-4 text-center">Streak</th>
                      <th className="p-4 text-right">Total XP</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-800/80 font-medium">
                    {leaderboardUsers.map(user => (
                      <tr key={user.rank} className="hover:bg-slate-800/40 transition-colors">
                        <td className="p-4 font-mono font-bold text-slate-400">
                          #{user.rank}
                        </td>
                        <td className="p-4 flex items-center gap-2.5 font-bold text-white">
                          <span className="text-base">{user.avatar}</span>
                          <span>{user.name}</span>
                        </td>
                        <td className="p-4">
                          <span className="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-emerald-500/10 text-emerald-300 border border-emerald-500/20">
                            {user.badge}
                          </span>
                        </td>
                        <td className="p-4 text-center text-rose-400 font-mono font-bold">
                          {user.streak}d 🔥
                        </td>
                        <td className="p-4 text-right font-mono font-bold text-emerald-400">
                          {user.xp} XP
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {/* TAB 5: PROFILE & BILLING OPS */}
          {activeSideTab === 'profile' && (
            <div className="space-y-6">
              {/* Profile Header */}
              <div className="p-8 rounded-3xl bg-gradient-to-br from-slate-900 via-slate-900/90 to-emerald-950/40 border border-emerald-500/20 shadow-2xl flex flex-wrap items-center justify-between gap-6">
                <div className="flex items-center gap-4">
                  <div className="w-16 h-16 rounded-3xl bg-gradient-to-tr from-emerald-500 via-teal-400 to-emerald-300 flex items-center justify-center font-black text-2xl text-slate-950 shadow-lg shadow-emerald-500/25">
                    {userEmail.charAt(0).toUpperCase()}
                  </div>
                  <div>
                    <div className="flex items-center gap-2">
                      <h1 className="text-2xl font-extrabold text-white">{userEmail.split('@')[0]}</h1>
                      <span className="px-3 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider bg-emerald-500/10 text-emerald-300 border border-emerald-500/30">
                        {isProOrAdmin ? (userRole === 'admin' ? 'Administrator' : 'PRO Lifetime') : 'Free Explorer'}
                      </span>
                    </div>
                    <p className="text-xs text-slate-400 mt-1">{userEmail}</p>
                    <p className="text-[11px] text-emerald-400 font-semibold mt-1">Active Learner · Joined October 2026</p>
                  </div>
                </div>

                <div className="flex items-center gap-3">
                  <button
                    onClick={() => setShowInvoiceModal(true)}
                    className="px-4 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-white font-bold text-xs transition-all border border-slate-700 flex items-center gap-2 shadow-sm"
                  >
                    <Download className="w-4 h-4 text-emerald-400" />
                    <span>Download GST Invoice</span>
                  </button>
                  {!isProOrAdmin && (
                    <button
                      onClick={onOpenPricing}
                      className="px-5 py-2.5 rounded-xl bg-gradient-to-r from-emerald-400 via-teal-400 to-emerald-300 hover:from-emerald-300 hover:to-teal-300 text-slate-950 font-black text-xs transition-all shadow-md active:scale-95"
                    >
                      Upgrade to Pro
                    </button>
                  )}
                </div>
              </div>

              {/* Stats Grid */}
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="p-5 rounded-2xl bg-slate-900/90 border border-slate-800 text-center">
                  <Gem className="w-6 h-6 text-emerald-400 mx-auto mb-2" />
                  <p className="text-2xl font-black text-white">{userStats?.xp || 76}</p>
                  <p className="text-[11px] text-slate-400 uppercase font-bold tracking-wider mt-1">Total XP Earned</p>
                </div>
                <div className="p-5 rounded-2xl bg-slate-900/90 border border-slate-800 text-center">
                  <Flame className="w-6 h-6 text-rose-400 fill-rose-400 mx-auto mb-2" />
                  <p className="text-2xl font-black text-white">{userStats?.streak || 2} Days</p>
                  <p className="text-[11px] text-slate-400 uppercase font-bold tracking-wider mt-1">Current Streak</p>
                </div>
                <div className="p-5 rounded-2xl bg-slate-900/90 border border-slate-800 text-center">
                  <Zap className="w-6 h-6 text-teal-300 mx-auto mb-2" />
                  <p className="text-2xl font-black text-white">{isProOrAdmin ? 'Unlimited' : '5 Units'}</p>
                  <p className="text-[11px] text-slate-400 uppercase font-bold tracking-wider mt-1">Daily Energy</p>
                </div>
                <div className="p-5 rounded-2xl bg-slate-900/90 border border-slate-800 text-center">
                  <Award className="w-6 h-6 text-amber-400 mx-auto mb-2" />
                  <p className="text-2xl font-black text-white">Level 5</p>
                  <p className="text-[11px] text-slate-400 uppercase font-bold tracking-wider mt-1">Coder Ranking</p>
                </div>
              </div>

              {/* Earned Badges Showcase */}
              <div className="p-6 rounded-3xl bg-slate-900/90 border border-slate-800 space-y-4">
                <h2 className="text-sm font-bold uppercase tracking-wider text-slate-400">Earned Badges & Milestones</h2>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  {[
                    { title: 'Genesis Coder', desc: 'Executed first code test', icon: '⚡' },
                    { title: 'Python Pioneer', desc: 'Completed Python Module 1', icon: '🐍' },
                    { title: 'Telugu Scholar', desc: 'Practiced Telugu concepts', icon: '📜' },
                    { title: 'Bug Crusher', desc: 'Fixed syntax error in sandbox', icon: '🎯' }
                  ].map(b => (
                    <div key={b.title} className="p-4 rounded-2xl bg-slate-950 border border-slate-800 text-center">
                      <span className="text-2xl mb-1 block">{b.icon}</span>
                      <p className="text-xs font-bold text-white">{b.title}</p>
                      <p className="text-[10px] text-slate-400 mt-1">{b.desc}</p>
                    </div>
                  ))}
                </div>
              </div>

              {/* Billing Details Card */}
              <div className="p-6 rounded-3xl bg-slate-900/90 border border-slate-800 flex flex-wrap items-center justify-between gap-4">
                <div>
                  <h2 className="text-sm font-bold uppercase tracking-wider text-slate-400">Subscription & Billing Status</h2>
                  <p className="text-base font-extrabold text-white mt-1">
                    {isProOrAdmin ? 'Prasana Code AI Pro — Lifetime Access' : 'Free Explorer Tier'}
                  </p>
                  <p className="text-xs text-slate-400 mt-0.5">
                    {isProOrAdmin 
                      ? 'Continuous access to all 5 language tracks, Mitra AI Tutor, and verified certificates.' 
                      : 'Basic sandbox execution with 5 daily energy units. Upgrade anytime.'}
                  </p>
                </div>

                <button
                  onClick={() => setShowInvoiceModal(true)}
                  className="px-4 py-2 rounded-xl bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 text-xs font-bold transition-all flex items-center gap-2"
                >
                  <Printer className="w-3.5 h-3.5" />
                  <span>View Official GST Receipt</span>
                </button>
              </div>
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

        {/* Weekly Leaderboard Widget */}
        <div className="p-5 rounded-3xl bg-slate-950/60 border border-slate-800 space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="font-bold text-xs uppercase tracking-wider text-slate-400">Weekly Leaderboard</h3>
            <span 
              onClick={() => handleSideNavClick('leaderboard')}
              className="text-xs text-emerald-400 font-semibold cursor-pointer hover:underline"
            >
              View All
            </span>
          </div>
          <div className="text-center py-6 border border-dashed border-slate-800 rounded-2xl">
            <Trophy className="w-8 h-8 text-emerald-400 mx-auto mb-2" />
            <p className="text-xs font-semibold text-slate-300">Earn 50 XP to enter this week's top coders list!</p>
          </div>
        </div>

        {/* Daily Learning Missions Widget */}
        <div className="p-5 rounded-3xl bg-slate-950/60 border border-slate-800 space-y-3">
          <div className="flex items-center justify-between">
            <h3 className="font-bold text-xs uppercase tracking-wider text-slate-400">Daily Missions</h3>
            <span 
              onClick={() => handleSideNavClick('missions')}
              className="text-xs text-emerald-400 font-semibold cursor-pointer hover:underline"
            >
              View Quests
            </span>
          </div>
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
