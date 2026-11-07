'use client';

import React from 'react';

export interface PerformanceReport {
  overall_percentage: number;
  mcq_score: number;
  coding_score: number;
  total_mcqs: number;
  total_mcqs_correct: number;
  role?: string;
  final_recommendation: string;
  recommendation_text: string;
  skill_breakdown: Record<string, {
    total: number;
    correct: number;
    highest_difficulty_passed: string | null;
    accuracy: number;
    difficulties_tested?: string[];
  }>;
  strengths: string[];
  weaknesses: string[];
  needs_practice: string[];
  coding_summary?: {
    total: number;
    passed: number;
    score: number;
    submissions?: Array<{
      title: string;
      difficulty: string;
      passed: boolean;
      time?: string;
      language?: string;
    }>;
  };
  difficulty_progression?: Array<{
    skill: string;
    difficulty: string;
    is_correct: boolean;
  }>;
}

interface EvaluationReportProps {
  report: PerformanceReport;
  role: string;
  onRestart: () => void;
}

export default function EvaluationReport({ report, role, onRestart }: EvaluationReportProps) {
  const isSuitable = report.final_recommendation === 'Suitable';
  const isNeedsImprovement = report.final_recommendation === 'Needs Improvement';

  const badgeColor = isSuitable
    ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30'
    : isNeedsImprovement
    ? 'bg-amber-500/10 text-amber-400 border-amber-500/30'
    : 'bg-rose-500/10 text-rose-400 border-rose-500/30';

  const scoreTextColor = isSuitable
    ? 'text-emerald-400'
    : isNeedsImprovement
    ? 'text-amber-400'
    : 'text-rose-400';

  return (
    <div className="w-full max-w-5xl mx-auto space-y-8 animate-in fade-in duration-500 pb-16">
      {/* Top Banner */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 pb-6 border-b border-white/10">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-500/10 text-blue-400 text-xs font-semibold mb-2 border border-blue-500/20">
            <span>SARTA Framework</span> • Section 4.7 Explainable Evaluation Report
          </div>
          <h1 className="text-3xl font-extrabold text-white tracking-tight">
            Candidate Assessment Report
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Target Role: <span className="text-emerald-400 font-semibold">{role || report.role || 'Software Engineer'}</span>
          </p>
        </div>

        <div className={`px-5 py-2.5 rounded-xl border font-bold text-sm tracking-wide uppercase ${badgeColor} shadow-lg`}>
          Recommendation: {report.final_recommendation}
        </div>
      </div>

      {/* Main Score Overview */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Composite Score */}
        <div className="glass-card rounded-2xl p-6 flex flex-col items-center justify-center text-center relative overflow-hidden">
          <div className="absolute top-0 right-0 w-32 h-32 bg-blue-500/10 rounded-full blur-2xl"></div>
          <p className="text-xs uppercase tracking-wider text-slate-400 font-semibold mb-2">Composite Score</p>
          <div className="relative my-2">
            <span className={`text-6xl font-black tracking-tight ${scoreTextColor}`}>
              {report.overall_percentage}%
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-2 max-w-xs">{report.recommendation_text}</p>
        </div>

        {/* Adaptive MCQ Performance */}
        <div className="glass-card rounded-2xl p-6 flex flex-col justify-between">
          <div>
            <div className="flex justify-between items-center mb-2">
              <span className="text-xs uppercase tracking-wider text-slate-400 font-semibold">Adaptive MCQ Accuracy</span>
              <span className="text-sm font-bold text-emerald-400">{report.mcq_score}%</span>
            </div>
            <div className="text-2xl font-bold text-white mb-1">
              {report.total_mcqs_correct} / {report.total_mcqs} <span className="text-xs font-normal text-slate-400">Correct</span>
            </div>
            <p className="text-xs text-slate-400 mb-4">
              Items dynamically calibrated to running ability using the adaptive CAT controller.
            </p>
          </div>
          <div className="w-full bg-slate-800 rounded-full h-2 overflow-hidden">
            <div
              className="bg-gradient-to-r from-blue-500 to-emerald-400 h-2 rounded-full transition-all duration-1000"
              style={{ width: `${Math.min(report.mcq_score, 100)}%` }}
            ></div>
          </div>
        </div>

        {/* Coding Assessment */}
        <div className="glass-card rounded-2xl p-6 flex flex-col justify-between">
          <div>
            <div className="flex justify-between items-center mb-2">
              <span className="text-xs uppercase tracking-wider text-slate-400 font-semibold">Coding Auto-Grading</span>
              <span className="text-sm font-bold text-cyan-400">{report.coding_score}%</span>
            </div>
            <div className="text-2xl font-bold text-white mb-1">
              {report.coding_summary?.passed || 0} / {report.coding_summary?.total || 0} <span className="text-xs font-normal text-slate-400">Challenges Passed</span>
            </div>
            <p className="text-xs text-slate-400 mb-4">
              Sandboxed runtime verification against hidden algorithmic test cases.
            </p>
          </div>
          <div className="w-full bg-slate-800 rounded-full h-2 overflow-hidden">
            <div
              className="bg-gradient-to-r from-cyan-500 to-blue-500 h-2 rounded-full transition-all duration-1000"
              style={{ width: `${Math.min(report.coding_score, 100)}%` }}
            ></div>
          </div>
        </div>
      </div>

      {/* Skill-Wise Breakdown & Competency Radar Chart (Section 4.7 & 6.1) */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* SVG Competency Radar Chart */}
        <div className="glass-card rounded-2xl p-6 border border-white/10 flex flex-col items-center justify-between">
          <div className="w-full text-left mb-2">
            <span className="text-xs uppercase tracking-wider text-slate-400 font-semibold block">
              Skill Competency Profile
            </span>
            <p className="text-[11px] text-slate-500">Multidimensional aptitude distribution</p>
          </div>

          <div className="relative w-full flex items-center justify-center py-4">
            {(() => {
              const skills = Object.keys(report.skill_breakdown || {});
              if (skills.length === 0) return <div className="text-slate-500 text-xs">No skill data</div>;
              
              const cx = 140;
              const cy = 130;
              const r = 90;
              const count = Math.max(skills.length, 3);
              const rings = [0.25, 0.5, 0.75, 1.0];

              // Helper for polygon points
              const getPolygonPoints = (scale: number) => {
                return Array.from({ length: count }).map((_, i) => {
                  const angle = (2 * Math.PI * i) / count - Math.PI / 2;
                  return `${cx + r * scale * Math.cos(angle)},${cy + r * scale * Math.sin(angle)}`;
                }).join(' ');
              };

              // Candidate data points
              const dataPoints = skills.map((skill, i) => {
                const angle = (2 * Math.PI * i) / count - Math.PI / 2;
                const acc = (report.skill_breakdown[skill]?.accuracy ?? 50) / 100;
                const valR = Math.max(0.15, Math.min(acc, 1.0)) * r;
                return `${cx + valR * Math.cos(angle)},${cy + valR * Math.sin(angle)}`;
              }).join(' ');

              return (
                <svg width="280" height="260" className="overflow-visible">
                  {/* Grid Rings */}
                  {rings.map((ring, idx) => (
                    <polygon
                      key={idx}
                      points={getPolygonPoints(ring)}
                      fill="none"
                      stroke="rgba(255, 255, 255, 0.08)"
                      strokeWidth="1"
                    />
                  ))}

                  {/* Axes */}
                  {Array.from({ length: count }).map((_, i) => {
                    const angle = (2 * Math.PI * i) / count - Math.PI / 2;
                    return (
                      <line
                        key={i}
                        x1={cx}
                        y1={cy}
                        x2={cx + r * Math.cos(angle)}
                        y2={cy + r * Math.sin(angle)}
                        stroke="rgba(255, 255, 255, 0.1)"
                        strokeWidth="1"
                      />
                    );
                  })}

                  {/* Data Polygon */}
                  <polygon
                    points={dataPoints}
                    fill="rgba(16, 185, 129, 0.25)"
                    stroke="#10b981"
                    strokeWidth="2"
                  />

                  {/* Labels */}
                  {skills.map((skill, i) => {
                    const angle = (2 * Math.PI * i) / count - Math.PI / 2;
                    const labelR = r + 20;
                    const lx = cx + labelR * Math.cos(angle);
                    const ly = cy + labelR * Math.sin(angle);
                    return (
                      <text
                        key={i}
                        x={lx}
                        y={ly}
                        textAnchor="middle"
                        dominantBaseline="central"
                        className="text-[10px] fill-slate-300 font-mono font-medium"
                      >
                        {skill}
                      </text>
                    );
                  })}
                </svg>
              );
            })()}
          </div>

          <div className="w-full flex justify-between text-[11px] text-slate-400 pt-2 border-t border-white/5">
            <span>Outer perimeter: 100%</span>
            <span className="text-emerald-400 font-medium">● Verified Proficiency</span>
          </div>
        </div>

        {/* Granular Skill List */}
        <div className="glass-card rounded-2xl p-6 border border-white/10 lg:col-span-2">
          <div className="flex items-center gap-3 mb-6">
            <div className="w-9 h-9 rounded-xl bg-emerald-500/20 flex items-center justify-center">
              <svg className="w-5 h-5 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
              </svg>
            </div>
            <div>
              <h2 className="text-lg font-bold text-white">Granular Skill Breakdown</h2>
              <p className="text-xs text-slate-400">Interpretable evaluation replacing opaque single aggregate scores</p>
            </div>
          </div>

          <div className="space-y-4">
            {Object.entries(report.skill_breakdown || {}).map(([skill, stats], idx) => {
              const skillAcc = stats.accuracy ?? (stats.total > 0 ? (stats.correct / stats.total) * 100 : 0);
              const diffColor =
                stats.highest_difficulty_passed === 'Hard'
                  ? 'text-rose-400 bg-rose-500/10 border-rose-500/20'
                  : stats.highest_difficulty_passed === 'Medium'
                  ? 'text-amber-400 bg-amber-500/10 border-amber-500/20'
                  : 'text-emerald-400 bg-emerald-500/10 border-emerald-500/20';

              return (
                <div key={idx} className="p-4 rounded-xl bg-slate-900/60 border border-white/5 space-y-2">
                  <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2">
                    <div className="flex items-center gap-3">
                      <span className="font-semibold text-white text-sm">{skill}</span>
                      <span className={`text-xs px-2.5 py-0.5 rounded-full border font-medium ${diffColor}`}>
                        Peak: {stats.highest_difficulty_passed || 'None'}
                      </span>
                    </div>
                    <div className="flex items-center gap-4 text-xs">
                      <span className="text-slate-400">
                        {stats.correct} of {stats.total} correct
                      </span>
                      <span className="font-bold text-white font-mono w-12 text-right">
                        {skillAcc.toFixed(0)}%
                      </span>
                    </div>
                  </div>

                  <div className="w-full bg-slate-800 rounded-full h-2 overflow-hidden">
                    <div
                      className={`h-2 rounded-full transition-all duration-700 ${
                        skillAcc >= 66 ? 'bg-emerald-400' : skillAcc >= 40 ? 'bg-amber-400' : 'bg-rose-400'
                      }`}
                      style={{ width: `${Math.min(skillAcc, 100)}%` }}
                    ></div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {/* Strengths & Weaknesses (XAI) */}
      <div className="grid md:grid-cols-2 gap-6">
        {/* Strengths */}
        <div className="glass-card rounded-2xl p-6 border-t-4 border-t-emerald-500">
          <div className="flex items-center gap-3 mb-4">
            <div className="w-7 h-7 rounded-full bg-emerald-500/20 flex items-center justify-center">
              <svg className="w-4 h-4 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
              </svg>
            </div>
            <h3 className="font-bold text-white">Demonstrated Strengths</h3>
          </div>
          <p className="text-xs text-slate-400 mb-4">Skills where the candidate consistently passed higher-difficulty items.</p>
          <div className="flex flex-wrap gap-2">
            {report.strengths && report.strengths.length > 0 ? (
              report.strengths.map((s, i) => (
                <span key={i} className="px-3 py-1 bg-emerald-500/15 text-emerald-300 rounded-lg text-xs font-medium border border-emerald-500/30">
                  {s}
                </span>
              ))
            ) : (
              <span className="text-xs text-slate-500 italic">No standout strengths detected</span>
            )}
          </div>
        </div>

        {/* Weaknesses / Learning Needs */}
        <div className="glass-card rounded-2xl p-6 border-t-4 border-t-rose-500">
          <div className="flex items-center gap-3 mb-4">
            <div className="w-7 h-7 rounded-full bg-rose-500/20 flex items-center justify-center">
              <svg className="w-4 h-4 text-rose-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path>
              </svg>
            </div>
            <h3 className="font-bold text-white">Areas for Improvement</h3>
          </div>
          <p className="text-xs text-slate-400 mb-4">Topics where difficulty drops were triggered during adaptive testing.</p>
          <div className="flex flex-wrap gap-2">
            {report.weaknesses && report.weaknesses.length > 0 ? (
              report.weaknesses.map((w, i) => (
                <span key={i} className="px-3 py-1 bg-rose-500/15 text-rose-300 rounded-lg text-xs font-medium border border-rose-500/30">
                  {w}
                </span>
              ))
            ) : (
              <span className="text-xs text-slate-500 italic">No severe skill deficiencies found</span>
            )}
          </div>
        </div>
      </div>

      {/* Action Footer */}
      <div className="flex justify-center gap-4 pt-4">
        <button
          onClick={onRestart}
          className="px-8 py-3.5 bg-gradient-to-r from-blue-600 to-emerald-600 hover:from-blue-500 hover:to-emerald-500 text-white font-bold rounded-xl shadow-lg shadow-emerald-500/20 transition-all hover:scale-105"
        >
          Start New Assessment
        </button>
      </div>
    </div>
  );
}
