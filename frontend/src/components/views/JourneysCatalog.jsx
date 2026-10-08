import React, { useState, useEffect } from 'react';
import { BookOpen, Clock, Award, Sparkles, ArrowRight, Play, CheckCircle2 } from 'lucide-react';
import { API_BASE_URL } from '../../api/agentApi';

export default function JourneysCatalog({ onSelectLesson }) {
  const [journeys, setJourneys] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedCategory, setSelectedCategory] = useState('All');

  useEffect(() => {
    fetch(`${API_BASE_URL}/api/journeys`)
      .then(res => res.json())
      .then(data => {
        if (data.journeys) setJourneys(data.journeys);
        setLoading(false);
      })
      .catch(err => {
        console.error('Error fetching journeys:', err);
        setLoading(false);
      });
  }, []);

  const categories = ['All', 'Python', 'Web Dev', 'DSA', 'C++', 'AI'];

  const filteredJourneys = selectedCategory === 'All'
    ? journeys
    : journeys.filter(j => j.category.toLowerCase().includes(selectedCategory.toLowerCase()));

  return (
    <div className="h-full w-full bg-ide-bg text-ide-text p-8 overflow-y-auto pb-32 font-sans">
      <div className="max-w-7xl mx-auto">
        {/* Page Header */}
        <div className="mb-10">
          <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-300 text-xs font-medium mb-3">
            <Sparkles className="w-3.5 h-3.5" />
            <span>Prasana Mastery Tracks</span>
          </div>
          <h1 className="text-4xl font-bold tracking-tight text-ide-text">Choose Your Skill Track</h1>
          <p className="text-ide-muted mt-2 text-base max-w-2xl">
            Guided step-by-step tracks designed to build real-world coding capability and algorithmic confidence.
          </p>
        </div>

        {/* Category Filters */}
        <div className="flex flex-wrap gap-2 mb-8">
          {categories.map((cat) => (
            <button
              key={cat}
              onClick={() => setSelectedCategory(cat)}
              className={`px-4 py-2 rounded-xl text-xs font-semibold transition-all duration-200 ${
                selectedCategory === cat
                  ? 'bg-gradient-to-r from-emerald-400 via-teal-400 to-emerald-300 text-slate-950 shadow-md shadow-emerald-500/20'
                  : 'bg-ide-panel/90 hover:bg-ide-sidebar text-ide-muted border border-ide-border'
              }`}
            >
              {cat}
            </button>
          ))}
        </div>

        {/* Journeys Cards Grid */}
        {loading ? (
          <div className="text-center py-20 text-slate-500 font-medium">Loading skill paths...</div>
        ) : (
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredJourneys.map((journey) => (
              <div
                key={journey.id}
                className="group relative rounded-3xl bg-ide-panel/80 border border-ide-border/80 hover:border-emerald-400/40 p-6 flex flex-col justify-between transition-all duration-300 shadow-xl"
              >
                <div>
                  <div className="flex items-center justify-between mb-4">
                    <span className="text-3xl p-3 rounded-2xl bg-ide-sidebar/80 border border-ide-border/50 group-hover:scale-105 transition-transform">
                      {journey.icon}
                    </span>
                    <span className="px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-300 text-xs font-medium">
                      {journey.badge}
                    </span>
                  </div>

                  <h2 className="text-xl font-bold mb-2 text-ide-text group-hover:text-emerald-300 transition-colors">
                    {journey.title}
                  </h2>
                  
                  <p className="text-ide-muted text-sm leading-relaxed mb-6">
                    {journey.description}
                  </p>
                </div>

                <div>
                  <div className="flex items-center justify-between text-xs text-ide-muted font-medium mb-6 pt-4 border-t border-ide-border/80">
                    <span className="flex items-center gap-1.5">
                      <BookOpen className="w-4 h-4 text-emerald-400" />
                      {journey.totalLessons} Lessons
                    </span>
                    <span className="flex items-center gap-1.5">
                      <Clock className="w-4 h-4 text-teal-300" />
                      {journey.estimatedHours} Hours
                    </span>
                  </div>

                  <button
                    onClick={() => {
                      const firstLesson = journey.courses[0]?.lessons[0];
                      if (firstLesson) onSelectLesson(firstLesson);
                    }}
                    className="w-full flex items-center justify-center gap-2 py-3 rounded-2xl bg-ide-sidebar hover:bg-gradient-to-r hover:from-emerald-400 hover:via-teal-400 hover:to-emerald-300 hover:text-slate-950 text-ide-text font-semibold text-xs transition-all duration-200 shadow-sm active:scale-95"
                  >
                    <span>Start Track</span>
                    <ArrowRight className="w-4 h-4" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

