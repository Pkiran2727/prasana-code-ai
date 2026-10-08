import React, { useState, useEffect } from 'react';
import { Award, Search, Filter, Code2, ArrowRight, CheckCircle2, AlertCircle } from 'lucide-react';
import { API_BASE_URL } from '../../api/agentApi';

export default function PracticeCatalog({ onSelectProblem }) {
  const [problems, setProblems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filterDifficulty, setFilterDifficulty] = useState('All');
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    fetch(`${API_BASE_URL}/api/problems`)
      .then(res => res.json())
      .then(data => {
        if (data.problems) setProblems(data.problems);
        setLoading(false);
      })
      .catch(err => {
        console.error('Error fetching problems:', err);
        setLoading(false);
      });
  }, []);

  const filtered = problems.filter(p => {
    const matchesDiff = filterDifficulty === 'All' || p.difficulty === filterDifficulty;
    const matchesSearch = p.title.toLowerCase().includes(searchQuery.toLowerCase()) || p.category.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesDiff && matchesSearch;
  });

  return (
    <div className="h-full w-full bg-ide-panel text-ide-text p-8 overflow-y-auto pb-32 font-sans">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-8 flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <h1 className="text-3xl font-extrabold tracking-tight">Practice & DSA Problem Bank</h1>
            <p className="text-ide-muted mt-1 text-sm">
              Master algorithm puzzles and interview problems with automated test verification.
            </p>
          </div>

          {/* Search & Filter */}
          <div className="flex items-center gap-3">
            <div className="relative">
              <Search className="w-4 h-4 text-ide-muted absolute left-3.5 top-3" />
              <input
                type="text"
                placeholder="Search problem..."
                value={searchQuery}
                onChange={e => setSearchQuery(e.target.value)}
                className="bg-ide-panel border border-ide-border rounded-xl pl-10 pr-4 py-2 text-xs text-ide-text focus:outline-none focus:border-emerald-500 w-48 sm:w-64"
              />
            </div>

            <div className="flex bg-ide-panel p-1 rounded-xl border border-ide-border">
              {['All', 'Easy', 'Medium', 'Hard'].map((diff) => (
                <button
                  key={diff}
                  onClick={() => setFilterDifficulty(diff)}
                  className={`px-3 py-1 rounded-lg text-xs font-semibold transition-all ${
                    filterDifficulty === diff
                      ? 'bg-emerald-500 text-slate-950 font-bold'
                      : 'text-ide-muted hover:text-ide-text'
                  }`}
                >
                  {diff}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Problems List */}
        {loading ? (
          <div className="text-center py-20 text-ide-muted">Loading problem bank...</div>
        ) : (
          <div className="space-y-3">
            {filtered.map((prob) => (
              <div
                key={prob.id}
                onClick={() => onSelectProblem(prob)}
                className="group p-5 rounded-2xl bg-ide-panel/80 border border-ide-border hover:border-emerald-500/50 flex items-center justify-between cursor-pointer transition-all duration-200 shadow-md"
              >
                <div className="flex items-center gap-4">
                  <div className="w-10 h-10 rounded-xl bg-ide-sidebar border border-ide-border flex items-center justify-center text-emerald-400 font-bold group-hover:scale-105 transition-transform">
                    <Code2 className="w-5 h-5" />
                  </div>
                  <div>
                    <h3 className="font-bold text-base group-hover:text-emerald-400 transition-colors">
                      {prob.title}
                    </h3>
                    <div className="flex items-center gap-3 text-xs text-ide-muted mt-1">
                      <span className="bg-ide-sidebar px-2 py-0.5 rounded text-[10px] font-medium text-ide-text">
                        {prob.category}
                      </span>
                      <span>Language: <strong className="text-ide-text capitalize">{prob.language}</strong></span>
                    </div>
                  </div>
                </div>

                <div className="flex items-center gap-4">
                  <span className={`px-3 py-1 rounded-full text-xs font-bold ${
                    prob.difficulty === 'Easy'
                      ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                      : prob.difficulty === 'Medium'
                      ? 'bg-teal-500/10 text-teal-300 border border-teal-500/20'
                      : 'bg-rose-500/10 text-rose-400 border border-rose-500/20'
                  }`}>
                    {prob.difficulty}
                  </span>

                  <div className="w-8 h-8 rounded-xl bg-ide-sidebar flex items-center justify-center group-hover:bg-emerald-500 group-hover:text-slate-950 transition-all">
                    <ArrowRight className="w-4 h-4" />
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
