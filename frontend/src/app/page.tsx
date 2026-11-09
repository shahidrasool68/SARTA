'use client';

import { useState, useEffect } from 'react';
import SkillGapDashboard, { GapAnalysis, InferredRoleData } from '@/components/SkillGapDashboard';
import AssessmentSession from '@/components/AssessmentSession';
import EvaluationReport, { PerformanceReport } from '@/components/EvaluationReport';

type WorkflowStep = 'upload' | 'dashboard' | 'assessment' | 'report';

export default function Home() {
  const [currentStep, setCurrentStep] = useState<WorkflowStep>('upload');
  const [resume, setResume] = useState<File | null>(null);
  const [jd, setJd] = useState<File | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  // Analysis state
  const [analysisResult, setAnalysisResult] = useState<GapAnalysis | null>(null);
  const [inferredRole, setInferredRole] = useState<InferredRoleData | null>(null);
  const [candidateSkills, setCandidateSkills] = useState<string[]>([]);
  const [missingSkills, setMissingSkills] = useState<string[]>([]);
  const [jdSkills, setJdSkills] = useState<string[]>([]);
  const [targetCompany, setTargetCompany] = useState<string | null>(null);
  const [availableCompanies, setAvailableCompanies] = useState<string[]>([]);
  const [companySearch, setCompanySearch] = useState<string>('');
  const [showCompanyList, setShowCompanyList] = useState<boolean>(false);

  // Load available companies on mount
  useEffect(() => {
    fetch('http://127.0.0.1:8000/api/assessment/available-companies')
      .then(res => res.json())
      .then(data => setAvailableCompanies(data.companies || []))
      .catch(() => {});
  }, []);

  // Assessment & Report state
  const [performanceReport, setPerformanceReport] = useState<PerformanceReport | null>(null);

  const handleAnalyze = async () => {
    if (!resume || !jd) return alert("Please upload both documents.");
    setIsAnalyzing(true);
    
    try {
      const formData = new FormData();
      formData.append("resume", resume);
      formData.append("jd", jd);

      const response = await fetch("http://127.0.0.1:8000/api/analyze-gap", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Server responded with ${response.status}`);
      }

      const data = await response.json();
      setAnalysisResult(data.gap_analysis);
      setInferredRole(data.inferred_role || null);
      // If user manually chose or typed a company, preserve it; otherwise use the JD-detected one
      setTargetCompany(prev => (prev && prev.trim() ? prev : (data.target_company || null)));
      
      const cSkills = data.candidate_skills || 
        [...data.gap_analysis.common.map((c: any) => c.candidate_has), ...data.gap_analysis.additional];
      setCandidateSkills(cSkills);
      setMissingSkills(data.gap_analysis.missing || []);

      setCurrentStep('dashboard');
    } catch (error) {
      console.error("Analysis failed:", error);
      alert("Failed to analyze documents. Please ensure the SARTA FastAPI backend is running.");
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleStartAssessment = (companyOverride?: string) => {
    if (companyOverride !== undefined) {
      setTargetCompany(companyOverride);
    }
    setCurrentStep('assessment');
  };

  const handleAssessmentFinish = (report: PerformanceReport) => {
    setPerformanceReport(report);
    setCurrentStep('report');
  };

  const handleRestart = () => {
    setResume(null);
    setJd(null);
    setAnalysisResult(null);
    setInferredRole(null);
    setTargetCompany(null);
    setJdSkills([]);
    setPerformanceReport(null);
    setCurrentStep('upload');
  };

  return (
    <main className="min-h-screen flex flex-col items-center p-6 md:p-12 lg:p-20 text-white selection:bg-emerald-500/30">
      <div className="z-10 max-w-5xl w-full">
        
        {/* Navigation Step Breadcrumbs */}
        <div className="flex justify-center items-center gap-2 mb-12 text-xs font-mono">
          <span className={`px-3 py-1 rounded-full ${currentStep === 'upload' ? 'bg-blue-600 text-white font-bold' : 'text-slate-500'}`}>
            1. Resume & JD Parsing
          </span>
          <span className="text-slate-600">→</span>
          <span className={`px-3 py-1 rounded-full ${currentStep === 'dashboard' ? 'bg-blue-600 text-white font-bold' : 'text-slate-500'}`}>
            2. Semantic Skill Gap
          </span>
          <span className="text-slate-600">→</span>
          <span className={`px-3 py-1 rounded-full ${currentStep === 'assessment' ? 'bg-blue-600 text-white font-bold' : 'text-slate-500'}`}>
            3. Adaptive Assessment
          </span>
          <span className="text-slate-600">→</span>
          <span className={`px-3 py-1 rounded-full ${currentStep === 'report' ? 'bg-blue-600 text-white font-bold' : 'text-slate-500'}`}>
            4. XAI Evaluation Report
          </span>
        </div>

        {/* STEP 1: UPLOAD VIEW */}
        {currentStep === 'upload' && (
          <div className="animate-fade-in-up">
            <div className="text-center mb-16">
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 text-emerald-400 text-xs font-mono font-medium mb-4 border border-emerald-500/20">
                SARTA Framework Prototype
              </div>
              <h1 className="text-5xl font-extrabold tracking-tight mb-4 bg-clip-text text-transparent bg-gradient-to-r from-blue-400 via-cyan-400 to-emerald-400">
                SARTA Assessment Platform
              </h1>
              <p className="text-base md:text-lg text-slate-400 max-w-2xl mx-auto leading-relaxed">
                Resume-Driven Skill Extraction, Role-Specific MCQ & Coding Assessment with Adaptive Difficulty
              </p>
            </div>

            <div className="grid md:grid-cols-2 gap-8 w-full max-w-4xl mx-auto">
              {/* Resume Upload Card */}
              <div className="glass-card rounded-2xl p-8 flex flex-col items-center justify-center text-center">
                <div className="w-16 h-16 rounded-full bg-blue-500/20 flex items-center justify-center mb-6">
                  <svg className="w-8 h-8 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                  </svg>
                </div>
                <h2 className="text-2xl font-bold mb-2">Candidate Resume</h2>
                <p className="text-slate-400 text-sm mb-6">PDF or DOCX structured profile</p>
                <label className="cursor-pointer bg-blue-600 hover:bg-blue-500 transition-colors px-6 py-3 rounded-lg font-semibold shadow-lg shadow-blue-500/30 text-sm">
                  Choose Resume
                  <input type="file" className="hidden" accept=".pdf,.docx" onChange={(e) => setResume(e.target.files?.[0] || null)} />
                </label>
                {resume && <p className="mt-4 text-xs font-mono text-emerald-400 truncate max-w-xs">{resume.name}</p>}
              </div>

              {/* JD Upload Card */}
              <div className="glass-card rounded-2xl p-8 flex flex-col items-center justify-center text-center">
                <div className="w-16 h-16 rounded-full bg-emerald-500/20 flex items-center justify-center mb-6">
                  <svg className="w-8 h-8 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
                  </svg>
                </div>
                <h2 className="text-2xl font-bold mb-2">Target Job Description</h2>
                <p className="text-slate-400 text-sm mb-6">PDF or DOCX technical requirements</p>
                <label className="cursor-pointer bg-emerald-600 hover:bg-emerald-500 transition-colors px-6 py-3 rounded-lg font-semibold shadow-lg shadow-emerald-500/30 text-sm">
                  Choose Job Description
                  <input type="file" className="hidden" accept=".pdf,.docx" onChange={(e) => setJd(e.target.files?.[0] || null)} />
                </label>
                {jd && <p className="mt-4 text-xs font-mono text-emerald-400 truncate max-w-xs">{jd.name}</p>}
              </div>
            </div>

            {/* Target Company Selector (Explicit Input or Auto-Detect) */}
            <div className="mt-8 max-w-4xl mx-auto glass-card rounded-2xl p-6 relative">
              <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
                <div>
                  <div className="flex items-center gap-2 mb-1">
                    <span className="text-sm font-bold text-white">Target Company</span>
                    <span className="text-[10px] uppercase font-mono px-2 py-0.5 rounded bg-blue-500/20 text-blue-300 border border-blue-500/30">
                      Tier-calibrated coding & difficulty
                    </span>
                  </div>
                  <p className="text-xs text-slate-400">
                    Specify the target company (e.g. Google, Amazon, TCS) or leave blank to auto-detect from the Job Description.
                  </p>
                </div>

                <div className="relative w-full sm:w-72">
                  <input
                    type="text"
                    value={targetCompany || companySearch}
                    placeholder="Search or enter company..."
                    onChange={(e) => {
                      setCompanySearch(e.target.value);
                      setTargetCompany(e.target.value || null);
                      setShowCompanyList(true);
                    }}
                    onFocus={() => setShowCompanyList(true)}
                    className="w-full bg-slate-900/80 border border-slate-700 rounded-xl px-4 py-2.5 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
                  />
                  {showCompanyList && availableCompanies.length > 0 && (
                    <div className="absolute left-0 right-0 top-full mt-1.5 bg-slate-900 border border-slate-700 rounded-xl shadow-2xl max-h-48 overflow-y-auto z-50 py-1">
                      {availableCompanies
                        .filter(c => !companySearch || c.toLowerCase().includes(companySearch.toLowerCase()))
                        .slice(0, 10)
                        .map(c => (
                          <button
                            key={c}
                            type="button"
                            onClick={() => {
                              setTargetCompany(c);
                              setCompanySearch(c);
                              setShowCompanyList(false);
                            }}
                            className="w-full text-left px-4 py-2 text-xs text-slate-200 hover:bg-blue-600/30 hover:text-white transition-colors"
                          >
                            {c}
                          </button>
                        ))}
                    </div>
                  )}
                </div>
              </div>

              {/* Quick Pills */}
              <div className="flex flex-wrap items-center gap-2 mt-4 pt-3 border-t border-slate-800">
                <span className="text-[11px] text-slate-500">Popular:</span>
                {['Google', 'Amazon', 'Microsoft', 'Meta', 'TCS', 'Infosys', 'Flipkart'].map(popular => (
                  <button
                    key={popular}
                    type="button"
                    onClick={() => {
                      setTargetCompany(popular);
                      setCompanySearch(popular);
                      setShowCompanyList(false);
                    }}
                    className={`text-[11px] px-2.5 py-1 rounded-lg border transition-all ${
                      targetCompany === popular
                        ? 'bg-blue-600 text-white border-blue-400 font-semibold shadow-sm'
                        : 'bg-slate-800/60 text-slate-400 border-slate-700/60 hover:text-white hover:border-slate-600'
                    }`}
                  >
                    {popular}
                  </button>
                ))}
                {targetCompany && (
                  <button
                    type="button"
                    onClick={() => {
                      setTargetCompany(null);
                      setCompanySearch('');
                    }}
                    className="text-[11px] text-rose-400 hover:text-rose-300 ml-auto underline"
                  >
                    Clear (Auto-detect from JD)
                  </button>
                )}
              </div>
            </div>

            {/* Action Area */}
            <div className="mt-12 flex justify-center">
              <button 
                onClick={handleAnalyze}
                disabled={!resume || !jd || isAnalyzing}
                className={`px-8 py-4 rounded-xl font-bold text-lg transition-all duration-300 ${
                  !resume || !jd || isAnalyzing 
                    ? 'bg-slate-800 text-slate-500 cursor-not-allowed' 
                    : 'bg-white text-slate-900 hover:scale-105 hover:shadow-xl hover:shadow-white/20'
                }`}
              >
                {isAnalyzing ? (
                  <span className="flex items-center gap-2">
                    <svg className="animate-spin h-5 w-5 text-current" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Extracting Semantic Skills & Inferring Role...
                  </span>
                ) : "Analyze Semantic Skill Gap"}
              </button>
            </div>
          </div>
        )}

        {/* STEP 2: DASHBOARD VIEW */}
        {currentStep === 'dashboard' && analysisResult && (
          <SkillGapDashboard 
            analysis={analysisResult} 
            inferredRole={inferredRole}
            targetCompany={targetCompany}
            onStartTest={handleStartAssessment} 
          />
        )}

        {/* STEP 3: ADAPTIVE ASSESSMENT SESSION */}
        {currentStep === 'assessment' && (
          <AssessmentSession 
            candidateSkills={inferredRole?.assessment_skills || candidateSkills}
            missingSkills={missingSkills}
            jdSkills={jdSkills}
            role={inferredRole?.role || 'Backend Developer'}
            targetCompany={targetCompany}
            onFinish={handleAssessmentFinish}
            onCancel={handleRestart}
          />
        )}

        {/* STEP 4: EXPLAINABLE EVALUATION REPORT */}
        {currentStep === 'report' && performanceReport && (
          <EvaluationReport 
            report={performanceReport}
            role={inferredRole?.role || performanceReport.role || 'Software Engineer'}
            onRestart={handleRestart}
          />
        )}

      </div>
    </main>
  );
}
