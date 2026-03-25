import React from 'react';
import { motion } from 'framer-motion';
import { ArrowLeft, CheckCircle2, AlertTriangle, TrendingUp, Presentation, BriefcaseBusiness, UserCheck, Flame } from 'lucide-react';

const containerVariants = {
  hidden: { opacity: 0 },
  visible: { 
    opacity: 1, 
    transition: { staggerChildren: 0.1 } 
  }
};

const cardVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: { 
    opacity: 1, 
    y: 0, 
    transition: { type: "spring", stiffness: 100, damping: 15 } 
  }
};

export default function MatchResults({ results, onReset }) {
  const { match_score, matched_skills, missing_critical_skills, missing_nice_to_have_skills, suggestions, ats_score, recruiter_summary, market_trends, quantifiable_metrics_count = 0, strong_action_verbs = [] } = results;

  const scoreColor = match_score >= 80 ? 'text-emerald-500' : match_score >= 60 ? 'text-amber-500' : 'text-rose-500';
  const strokeColor = match_score >= 80 ? '#10b981' : match_score >= 60 ? '#f59e0b' : '#f43f5e';
  const scoreGradient = match_score >= 80 ? 'from-emerald-400 to-emerald-600' : match_score >= 60 ? 'from-amber-400 to-amber-600' : 'from-rose-400 to-rose-600';

  return (
    <motion.div variants={containerVariants} initial="hidden" animate="visible" className="space-y-8 max-w-6xl mx-auto">
      <motion.button 
        variants={cardVariants}
        onClick={onReset} 
        className="text-sm font-bold text-slate-500 hover:text-slate-800 flex items-center mb-4 px-3 py-2 rounded-xl hover:bg-white/60 backdrop-blur-sm transition-all shadow-sm w-max border border-transparent hover:border-slate-200"
      >
        <ArrowLeft className="w-4 h-4 mr-2" />
        Analyze Another Resume
      </motion.button>

      {/* Recruiter Summary Hero */}
      <motion.div variants={cardVariants} className="bg-gradient-to-br from-slate-900 to-slate-800 rounded-3xl p-8 relative overflow-hidden shadow-2xl border border-slate-700">
        <div className="absolute top-0 right-0 p-8 opacity-10">
          <Presentation className="w-32 h-32 text-white" />
        </div>
        <h2 className="text-slate-400 text-sm font-bold tracking-widest uppercase mb-3 flex items-center">
          <UserCheck className="w-4 h-4 mr-2" /> Recruiter's Take
        </h2>
        <p className="text-2xl md:text-3xl font-medium text-white leading-tight max-w-3xl relative z-10">
          "{recruiter_summary}"
        </p>
      </motion.div>

      <div className="grid grid-cols-1 md:grid-cols-12 gap-6">
        {/* Core Metrics Column */}
        <div className="md:col-span-5 space-y-6">
          {/* Main Score Card */}
          <motion.div variants={cardVariants} className="bg-white/80 backdrop-blur-xl p-8 rounded-3xl shadow-[0_8px_30px_rgba(0,0,0,0.04)] border border-white flex flex-col items-center justify-center relative overflow-hidden group">
            <div className={`absolute top-0 left-0 w-full h-1.5 bg-gradient-to-r ${scoreGradient}`}></div>
            <h3 className="text-sm font-bold tracking-widest uppercase text-slate-400 mb-8">Overall Match Score</h3>
            <div className="relative w-44 h-44 mb-4">
              <svg viewBox="0 0 36 36" className="w-full h-full -rotate-90 filter drop-shadow-md">
                <path
                  className="text-slate-100"
                  d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2.5"
                />
                <motion.path
                  initial={{ strokeDasharray: "0, 100" }}
                  animate={{ strokeDasharray: `${match_score}, 100` }}
                  transition={{ duration: 1.5, ease: "easeOut", delay: 0.5 }}
                  d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                  fill="none"
                  stroke={strokeColor}
                  strokeWidth="2.5"
                  strokeLinecap="round"
                />
              </svg>
              <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 text-center">
                <div className={`text-4xl font-extrabold tracking-tighter ${scoreColor}`}>
                  {Number(match_score).toFixed(1)}%
                </div>
              </div>
            </div>
            <p className="text-sm text-slate-500 font-medium text-center px-6">Calculated using TF-IDF AI Cosine Similarity + Semantic Keyword mappings.</p>
          </motion.div>

          <div className="grid grid-cols-2 gap-6">
            {/* ATS Format Score */}
            <motion.div variants={cardVariants} className="bg-white/80 backdrop-blur-xl p-6 rounded-3xl shadow-[0_8px_30px_rgba(0,0,0,0.04)] border border-white flex flex-col items-center justify-center">
              <h3 className="text-xs font-bold tracking-widest uppercase text-slate-400 mb-4 text-center">ATS Format</h3>
              <div className="text-4xl font-extrabold text-transparent bg-clip-text bg-gradient-to-br from-indigo-500 to-purple-600 mb-1">
                {Number(ats_score).toFixed(1)}
              </div>
              <div className="text-xs text-slate-400 font-bold uppercase">/ 100</div>
            </motion.div>

            {/* Missing Skills Count */}
            <motion.div variants={cardVariants} className="bg-white/80 backdrop-blur-xl p-6 rounded-3xl shadow-[0_8px_30px_rgba(0,0,0,0.04)] border border-white flex flex-col items-center justify-center">
              <h3 className="text-xs font-bold tracking-widest uppercase text-slate-400 mb-4 text-center">Skill Gaps</h3>
              <div className="text-4xl font-extrabold text-transparent bg-clip-text bg-gradient-to-br from-rose-400 to-red-600 mb-1">
                {missing_critical_skills.length + missing_nice_to_have_skills.length}
              </div>
              <div className="text-xs text-slate-400 font-bold uppercase">Identified</div>
            </motion.div>
          </div>

          <div className="grid grid-cols-2 gap-6">
            {/* Resume Impact Metrics */}
            <motion.div variants={cardVariants} className="bg-white/80 backdrop-blur-xl p-6 rounded-3xl shadow-[0_8px_30px_rgba(0,0,0,0.04)] border border-white flex flex-col items-center justify-center">
              <h3 className="text-xs font-bold tracking-widest uppercase text-slate-400 mb-4 text-center">Impact Metrics</h3>
              <div className="text-4xl font-extrabold text-transparent bg-clip-text bg-gradient-to-br from-emerald-400 to-teal-500 mb-1">
                {quantifiable_metrics_count}
              </div>
              <div className="text-xs text-slate-400 font-bold uppercase">Found in Text</div>
            </motion.div>

            {/* Action Verbs */}
            <motion.div variants={cardVariants} className="bg-white/80 backdrop-blur-xl p-6 rounded-3xl shadow-[0_8px_30px_rgba(0,0,0,0.04)] border border-white flex flex-col items-center justify-center">
              <h3 className="text-xs font-bold tracking-widest uppercase text-slate-400 mb-4 text-center">Action Verbs</h3>
              <div className="text-4xl font-extrabold text-transparent bg-clip-text bg-gradient-to-br from-sky-400 to-blue-500 mb-1">
                {strong_action_verbs.length}
              </div>
              <div className="text-xs text-slate-400 font-bold uppercase">Strong Verbs</div>
            </motion.div>
          </div>
        </div>

        {/* Detailed Breakdown Column */}
        <div className="md:col-span-7 space-y-6">
          {/* Match Analysis Breakdown */}
          <motion.div variants={cardVariants} className="bg-white/80 backdrop-blur-xl p-8 rounded-3xl shadow-[0_8px_30px_rgba(0,0,0,0.04)] border border-white h-full flex flex-col">
            <h3 className="text-xl font-extrabold text-slate-800 mb-8 flex items-center">
              <BriefcaseBusiness className="w-6 h-6 mr-3 text-indigo-500" />
              Skill Requirement Cross-Reference
            </h3>
            
            <div className="space-y-8 flex-1">
              {/* Matched */}
              <div>
                <h4 className="flex justify-between items-center text-sm font-bold text-slate-600 uppercase tracking-wider mb-4 border-b border-slate-100 pb-2">
                  <span className="flex items-center"><CheckCircle2 className="w-4 h-4 mr-2 text-emerald-500" /> Requisites Met</span>
                  <span className="bg-emerald-100 text-emerald-700 px-2 py-0.5 rounded-md text-xs">{matched_skills.length}</span>
                </h4>
                <div className="flex flex-wrap gap-2.5">
                  {matched_skills.map((skill, i) => (
                    <span key={i} className="bg-emerald-50 border border-emerald-200 text-emerald-700 px-3 py-1.5 rounded-lg text-sm font-semibold shadow-sm">
                      {skill}
                    </span>
                  ))}
                  {matched_skills.length === 0 && <p className="text-slate-400 text-sm italic">No exact matches found.</p>}
                </div>
              </div>

              {/* Critical Missing */}
              <div>
                <h4 className="flex justify-between items-center text-sm font-bold text-slate-600 uppercase tracking-wider mb-4 border-b border-slate-100 pb-2">
                  <span className="flex items-center"><AlertTriangle className="w-4 h-4 mr-2 text-rose-500" /> Critical Deficiencies</span>
                  <span className="bg-rose-100 text-rose-700 px-2 py-0.5 rounded-md text-xs">{missing_critical_skills.length}</span>
                </h4>
                <div className="flex flex-wrap gap-2.5">
                  {missing_critical_skills.map((skill, i) => (
                    <span key={i} className="bg-rose-50 border border-rose-200 text-rose-700 px-3 py-1.5 rounded-lg text-sm font-semibold shadow-sm">
                      {skill}
                    </span>
                  ))}
                  {missing_critical_skills.length === 0 && <p className="text-slate-400 text-sm italic">Excellent, no critical gaps.</p>}
                </div>
              </div>

              {/* Nice to haves */}
              {missing_nice_to_have_skills.length > 0 && (
                <div>
                  <h4 className="flex justify-between items-center text-sm font-bold text-slate-500 uppercase tracking-wider mb-4 border-b border-slate-100 pb-2">
                    Bonus Qualifications Missing
                    <span className="bg-slate-100 text-slate-600 px-2 py-0.5 rounded-md text-xs">{missing_nice_to_have_skills.length}</span>
                  </h4>
                  <div className="flex flex-wrap gap-2">
                    {missing_nice_to_have_skills.map((skill, i) => (
                      <span key={i} className="bg-slate-50 border border-slate-200 text-slate-600 px-2.5 py-1 rounded-md text-xs font-medium">
                        {skill}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </motion.div>
        </div>
      </div>

      {/* Bottom Actionable Bar */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 pb-12">
        <motion.div variants={cardVariants} className="bg-indigo-50/80 p-8 rounded-3xl border border-indigo-100 backdrop-blur-xl">
          <h3 className="text-lg font-extrabold text-indigo-900 mb-5 flex items-center">
            <Flame className="w-5 h-5 mr-3 text-indigo-500" />
            AI Enhancement Recommendations
          </h3>
          <ul className="space-y-4">
            {suggestions.map((s, i) => (
              <li key={i} className="flex text-indigo-800 font-medium text-sm bg-white/60 p-4 rounded-2xl shadow-sm border border-indigo-50/50">
                <span className="w-1.5 h-1.5 rounded-full bg-indigo-500 mt-2 mr-3 flex-shrink-0"></span>
                {s}
              </li>
            ))}
          </ul>
        </motion.div>

        <motion.div variants={cardVariants} className="bg-purple-50/80 p-8 rounded-3xl border border-purple-100 backdrop-blur-xl">
           <h3 className="text-lg font-extrabold text-purple-900 mb-5 flex items-center">
            <TrendingUp className="w-5 h-5 mr-3 text-purple-500" />
            Market Competitiveness (Missing Trends)
          </h3>
          <p className="text-sm font-medium text-purple-800/80 mb-5 leading-relaxed">
            Based on millions of recent hires, these skills mentioned in the job description are highly demanded in the current market and you should prioritize learning them.
          </p>
          <div className="flex flex-wrap gap-3">
            {market_trends.map((trend, i) => (
              <div key={i} className="flex items-center bg-white px-4 py-2.5 rounded-xl text-sm font-bold text-purple-700 shadow-sm border border-purple-100/50">
                <TrendingUp className="w-4 h-4 mr-2 opacity-50" />
                {trend}
              </div>
            ))}
          </div>
        </motion.div>
      </div>

    </motion.div>
  );
}
