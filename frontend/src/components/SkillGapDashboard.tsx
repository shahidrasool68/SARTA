import React from 'react';

export interface InferredRoleData {
  role: string;
  confidence: number;
  matched_skills: string[];
  missing_core_skills: string[];
  assessment_skills: string[];
}

export interface GapAnalysis {
  match_score: number;
  common: { required: string; candidate_has: string; similarity_score: number }[];
  missing: string[];
  additional: string[];
  bipartite_matches?: { resume_skill: string; jd_skill: string; similarity: number; is_match: boolean }[];
}

interface SkillGapDashboardProps {
  analysis: GapAnalysis;
  inferredRole?: InferredRoleData | null;
  onStartTest: () => void;
}

export default function SkillGapDashboard({ analysis, inferredRole, onStartTest }: SkillGapDashboardProps) {
  // Determine color based on match score
  const scoreColor = 
    analysis.match_score >= 80 ? 'text-emerald-400' :
    analysis.match_score >= 50 ? 'text-yellow-400' : 'text-rose-400';

  return (
    <div className="w-full max-w-5xl mx-auto mt-8 animate-fade-in-up space-y-8">
      {/* Header / Score */}
      <div className="glass-card rounded-3xl p-8 flex flex-col items-center text-center relative overflow-hidden">
        <div className="absolute top-0 right-0 w-64 h-64 bg-blue-500/10 rounded-full blur-3xl -mr-32 -mt-32"></div>
        <div className="absolute bottom-0 left-0 w-64 h-64 bg-emerald-500/10 rounded-full blur-3xl -ml-32 -mb-32"></div>
        
        <h2 className="text-3xl font-bold mb-2 z-10">Candidate-Job Compatibility</h2>
        <p className="text-slate-400 mb-6 z-10">Semantic Match Analysis Complete (spaCy + SBERT + Hungarian Algorithm)</p>
        
        <div className="flex items-center justify-center w-44 h-44 rounded-full border-8 border-slate-800 bg-slate-900/50 shadow-[0_0_40px_rgba(0,0,0,0.5)] z-10 relative">
           <span className={`text-6xl font-black tracking-tighter ${scoreColor}`}>
             {analysis.match_score.toFixed(0)}<span className="text-3xl">%</span>
           </span>
        </div>
      </div>

      {/* Section 4.3: Inferred Role Mapping Card */}
      {inferredRole && (
        <div className="glass-card rounded-2xl p-6 border-l-4 border-l-indigo-500 bg-indigo-950/20">
          <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
            <div>
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/20 text-indigo-300 text-xs font-semibold mb-2">
                Section 4.3 Role Mapping Pipeline
              </div>
              <h3 className="text-2xl font-bold text-white flex items-center gap-3">
                <span>{inferredRole.role}</span>
                <span className="text-xs px-2.5 py-1 rounded-full bg-indigo-500/30 text-indigo-200 border border-indigo-400/30">
                  {inferredRole.confidence}% Match Confidence
                </span>
              </h3>
              <p className="text-xs text-slate-400 mt-1">
                Automated role inference derived from semantic comparison with predefined job-role taxonomies.
              </p>
            </div>

            <div className="text-left sm:text-right">
              <span className="text-xs text-slate-400 block mb-1">Adaptive Assessment Targets:</span>
              <div className="flex flex-wrap gap-1.5 justify-start sm:justify-end">
                {inferredRole.assessment_skills.map((s, i) => (
                  <span key={i} className="px-2.5 py-0.5 rounded bg-indigo-500/20 text-indigo-300 text-xs font-medium border border-indigo-500/30">
                    {s}
                  </span>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Grid for Skills */}
      <div className="grid md:grid-cols-3 gap-6">
        {/* Missing Skills (The Gap) */}
        <div className="glass-card rounded-2xl p-6 border-t-4 border-t-rose-500">
          <div className="flex items-center gap-3 mb-4">
            <div className="w-8 h-8 rounded-full bg-rose-500/20 flex items-center justify-center">
              <svg className="w-4 h-4 text-rose-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12"></path></svg>
            </div>
            <h3 className="text-xl font-bold">Skill Gaps</h3>
          </div>
          <p className="text-xs text-slate-400 mb-4">Required by job, missing from resume.</p>
          <div className="flex flex-wrap gap-2">
            {analysis.missing.length > 0 ? analysis.missing.map((skill, i) => (
              <span key={i} className="px-3 py-1 text-sm bg-rose-500/10 text-rose-400 rounded-full border border-rose-500/20">
                {skill}
              </span>
            )) : <span className="text-slate-500 text-sm italic">No skill gaps found!</span>}
          </div>
        </div>

        {/* Common Skills — Compact pill layout */}
        <div className="glass-card rounded-2xl p-6 border-t-4 border-t-emerald-500">
          <div className="flex items-center gap-3 mb-4">
            <div className="w-8 h-8 rounded-full bg-emerald-500/20 flex items-center justify-center">
              <svg className="w-4 h-4 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path></svg>
            </div>
            <h3 className="text-xl font-bold">Verified Matches</h3>
            <span className="ml-auto text-sm text-emerald-400 font-semibold">{analysis.common.length}</span>
          </div>
          <p className="text-xs text-slate-400 mb-4">Core overlapping competencies.</p>
          <div className="flex flex-wrap gap-2">
            {analysis.common.length > 0 ? analysis.common.map((item, i) => (
              <span key={i} className="px-3 py-1 text-sm bg-emerald-500/10 text-emerald-400 rounded-full border border-emerald-500/20" title={`Matched: ${item.candidate_has} (${(item.similarity_score * 100).toFixed(0)}%)`}>
                {item.required}
              </span>
            )) : <span className="text-slate-500 text-sm italic">No core matches found.</span>}
          </div>
        </div>

        {/* Additional Skills */}
        <div className="glass-card rounded-2xl p-6 border-t-4 border-t-blue-500">
          <div className="flex items-center gap-3 mb-4">
            <div className="w-8 h-8 rounded-full bg-blue-500/20 flex items-center justify-center">
              <svg className="w-4 h-4 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path></svg>
            </div>
            <h3 className="text-xl font-bold">Bonus Skills</h3>
          </div>
          <p className="text-xs text-slate-400 mb-4">On resume, but not explicitly requested.</p>
          <div className="flex flex-wrap gap-2">
            {analysis.additional.slice(0, 10).map((skill, i) => (
              <span key={i} className="px-3 py-1 text-sm bg-blue-500/10 text-blue-400 rounded-full border border-blue-500/20">
                {skill}
              </span>
            ))}
            {analysis.additional.length > 10 && (
              <span className="px-3 py-1 text-sm bg-slate-800 text-slate-400 rounded-full">+{analysis.additional.length - 10} more</span>
            )}
          </div>
        </div>
      </div>

      {/* Bipartite Matching Table */}
      {analysis.bipartite_matches && analysis.bipartite_matches.length > 0 && (
        <div className="glass-card rounded-2xl p-8 border border-white/10 overflow-x-auto">
          <div className="flex items-center gap-3 mb-2">
            <svg className="w-5 h-5 text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"></path></svg>
            <h3 className="text-xl font-bold">Optimal Bipartite Matching (Hungarian Algorithm)</h3>
          </div>
          <p className="text-sm text-slate-400 mb-6">Optimal 1-to-1 skill pairings via cosine similarity on SBERT embeddings. Match threshold: ≥35%.</p>
          
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="border-b border-white/10 text-slate-400 text-sm">
                <th className="pb-3 font-medium">Resume Skill</th>
                <th className="pb-3 font-medium">JD Skill</th>
                <th className="pb-3 font-medium">Similarity</th>
                <th className="pb-3 font-medium text-center">Match</th>
              </tr>
            </thead>
            <tbody>
              {[...analysis.bipartite_matches]
                .filter(m => m.similarity >= 0.15)
                .sort((a, b) => b.similarity - a.similarity)
                .map((match, idx) => {
                  const sim = match.similarity;
                  let textColor = 'text-rose-400';
                  let bgColor = 'bg-rose-500/10';
                  let icon = '✗';
                  
                  if (sim >= 0.99) {
                    textColor = 'text-emerald-400';
                    bgColor = 'bg-emerald-500/10';
                    icon = '✓';
                  } else if (sim >= 0.35) {
                    textColor = 'text-amber-400';
                    bgColor = 'bg-amber-500/10';
                    icon = '✓';
                  }

                  return (
                    <tr key={idx} className="border-b border-white/5 hover:bg-white/5 transition-colors">
                      <td className="py-3 text-sm text-slate-300 font-mono">{match.resume_skill}</td>
                      <td className="py-3 text-sm text-slate-300 font-mono">{match.jd_skill}</td>
                      <td className={`py-3 text-sm font-semibold ${textColor}`}>
                        {(sim * 100).toFixed(1)}%
                      </td>
                      <td className="py-3 text-center">
                        <span className={`inline-flex items-center justify-center w-6 h-6 rounded-full ${bgColor} ${textColor}`}>
                          {icon}
                        </span>
                      </td>
                    </tr>
                  );
                })}
            </tbody>
          </table>
        </div>
      )}

      {/* Start Button */}
      <div className="flex justify-center pt-4">
        <button 
          onClick={onStartTest}
          className="px-10 py-4 bg-gradient-to-r from-blue-600 to-emerald-600 hover:from-blue-500 hover:to-emerald-500 text-white font-bold rounded-xl shadow-[0_0_30px_rgba(16,185,129,0.3)] transition-all hover:scale-105"
        >
          Proceed to Adaptive Assessment
        </button>
      </div>
    </div>
  );
}
