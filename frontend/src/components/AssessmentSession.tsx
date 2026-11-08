'use client';

import { useState, useEffect } from 'react';
import Editor from '@monaco-editor/react';

type QuestionType = 'MCQ' | 'CODING';

interface AssessmentSessionProps {
  candidateSkills?: string[];
  missingSkills?: string[];
  role?: string;
  targetCompany?: string | null;
  onFinish: (report: any) => void;
  onCancel?: () => void;
}

const LANGUAGE_MAP: Record<string, { id: number; monaco: string; starter: string }> = {
  'Python': {
    id: 71,
    monaco: 'python',
    starter: 'def solution():\n    # Implement your algorithm here\n    pass\n\nprint(solution())\n'
  },
  'JavaScript': {
    id: 63,
    monaco: 'javascript',
    starter: 'function solution() {\n    // Implement your algorithm here\n    return true;\n}\n\nconsole.log(solution());\n'
  },
  'Java': {
    id: 62,
    monaco: 'java',
    starter: 'public class Main {\n    public static void main(String[] args) {\n        // Your code here\n        System.out.println("Solution");\n    }\n}\n'
  },
  'C++': {
    id: 54,
    monaco: 'cpp',
    starter: '#include <iostream>\nusing namespace std;\n\nint main() {\n    // Your code here\n    cout << "Solution" << endl;\n    return 0;\n}\n'
  }
};

export default function AssessmentSession({
  candidateSkills = ['Python', 'SQL', 'OOP'],
  missingSkills = [],
  role = 'Backend Developer',
  targetCompany = null,
  onFinish,
  onCancel
}: AssessmentSessionProps) {
  // Session State
  const [sessionId, setSessionId] = useState<string>('');
  const [error, setError] = useState<string>('');
  const [skillsToAssess, setSkillsToAssess] = useState<string[]>([]);
  const [currentSkillIdx, setCurrentSkillIdx] = useState<number>(0);
  const [currentQuestionInSkill, setCurrentQuestionInSkill] = useState<number>(1);
  const questionsPerSkill = 3; // three questions per skill allow difficulty progression

  const [currentType, setCurrentType] = useState<QuestionType>('MCQ');
  const [currentDifficulty, setCurrentDifficulty] = useState<string>('Medium');
  const [streak, setStreak] = useState<number>(0);

  // MCQ State
  const [mcqData, setMcqData] = useState<any>(null);
  const [selectedOption, setSelectedOption] = useState<string | null>(null);
  const [isAnswerSubmitted, setIsAnswerSubmitted] = useState<boolean>(false);
  const [answerFeedback, setAnswerFeedback] = useState<{ is_correct: boolean; correct_answer: string } | null>(null);
  const [loadingQuestion, setLoadingQuestion] = useState<boolean>(true);

  // Coding State
  const [codingData, setCodingData] = useState<any>(null);
  const [companyProblems, setCompanyProblems] = useState<any[]>([]);
  const [companyStats, setCompanyStats] = useState<any>(null);
  const [selectedLanguage, setSelectedLanguage] = useState<string>('Python');
  const [code, setCode] = useState<string>(LANGUAGE_MAP['Python'].starter);
  const [isExecutingCode, setIsExecutingCode] = useState<boolean>(false);
  const [executionResult, setExecutionResult] = useState<any>(null);

  // Timer State (45:00 countdown)
  const [secondsLeft, setSecondsLeft] = useState<number>(45 * 60);

  // 1. Initialize Adaptive Assessment Session
  useEffect(() => {
    let timer: NodeJS.Timeout;
    timer = setInterval(() => {
      setSecondsLeft((prev) => (prev > 0 ? prev - 1 : 0));
    }, 1000);

    const initSession = async () => {
      try {
        const res = await fetch('http://127.0.0.1:8000/api/assessment/start-session', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            skills: candidateSkills,
            role: role,
            missing_skills: missingSkills,
            target_company: targetCompany
          })
        });

        if (res.ok) {
          const data = await res.json();
          setSessionId(data.session_id);
          const assessList = data.skills_to_assess && data.skills_to_assess.length > 0
            ? data.skills_to_assess
            : ['Python', 'Data Structures', 'OOP'];
          setSkillsToAssess(assessList);
          // Use the company-tier-based initial difficulty from the server
          const initialDiff = data.blueprint?.initial_difficulty || 'Medium';
          setCurrentDifficulty(initialDiff);
          loadNextMCQ(assessList[0], initialDiff, 0, true, data.session_id);
        } else {
          throw new Error('Unable to start assessment session');
        }
      } catch (e) {
        setError(e instanceof Error ? e.message : 'Backend unavailable');
        setLoadingQuestion(false);
      }

      fetchCodingQuestion();
    };

    initSession();

    return () => clearInterval(timer);
  }, []);

  // Format timer
  const minutes = Math.floor(secondsLeft / 60);
  const seconds = secondsLeft % 60;
  const formattedTime = `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;

  // Fetch Next MCQ
  const loadNextMCQ = async (
    skillName: string,
    difficulty: string,
    curStreak: number,
    lastCorrect: boolean,
    sessId: string
  ) => {
    setLoadingQuestion(true);
    setSelectedOption(null);
    setIsAnswerSubmitted(false);
    setAnswerFeedback(null);

    try {
      const res = await fetch('http://127.0.0.1:8000/api/assessment/next-mcq', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          session_id: sessId || sessionId,
          skill: skillName,
          current_difficulty: difficulty,
          is_last_correct: lastCorrect,
          streak: curStreak
        })
      });

      if (res.ok) {
        const data = await res.json();
        setMcqData(data.question);
        setCurrentDifficulty(data.adaptive_state?.next_difficulty || difficulty);
      } else {
        throw new Error('Fallback needed');
      }
    } catch {
      setError('Could not retrieve an assessment question. Check the backend server.');
      setMcqData(null);
    } finally {
      setLoadingQuestion(false);
    }
  };

  // Fetch Coding Question
  const fetchCodingQuestion = async () => {
    try {
      const companyParam = encodeURIComponent(targetCompany || 'General');
      const res = await fetch(`http://127.0.0.1:8000/api/assessment/coding-question/${companyParam}`);
      if (res.ok) {
        const data = await res.json();
        if (!res.ok) throw new Error('Coding question unavailable');
        setCodingData(data);
        if (data.company_problems) setCompanyProblems(data.company_problems);
        if (data.company_stats) setCompanyStats(data.company_stats);
        if (data.starter_code && selectedLanguage === 'Python') {
          setCode(data.starter_code);
        }
      }
    } catch {
      setError('Could not load coding problem.');
    }
  };

  // Handle MCQ Option Selection & Instant Feedback
  const handleSelectOption = async (option: string) => {
    if (isAnswerSubmitted || !mcqData) return;
    setSelectedOption(option);
    setIsAnswerSubmitted(true);
    setError('');

    try {
      const res = await fetch('http://127.0.0.1:8000/api/assessment/submit-answer', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          session_id: sessionId,
          question_id: mcqData._id || 'q_id',
          selected_answer: option,
          skill: mcqData.skill,
          difficulty: mcqData.difficulty,
        })
      });

      if (res.ok) {
        const data = await res.json();
        setAnswerFeedback({
          is_correct: data.is_correct,
          correct_answer: data.correct_answer
        });
        setStreak(data.streak);
        setCurrentDifficulty(data.next_difficulty);
      } else {
        setError('Answer submission failed; please retry from a new session.');
        setIsAnswerSubmitted(false);
      }
    } catch {
      setError('Network error while submitting answer.');
      setIsAnswerSubmitted(false);
    }
  };

  // Advance to next MCQ or Transition to Coding
  const handleAdvance = () => {
    const nextQInSkill = currentQuestionInSkill + 1;

    if (nextQInSkill <= questionsPerSkill) {
      setCurrentQuestionInSkill(nextQInSkill);
      const currSkill = skillsToAssess[currentSkillIdx] || 'Python';
      loadNextMCQ(currSkill, currentDifficulty, streak, answerFeedback?.is_correct ?? true, sessionId);
    } else {
      // Finished questions for this skill, move to next skill
      const nextSkillIdx = currentSkillIdx + 1;
      if (nextSkillIdx < skillsToAssess.length) {
        setCurrentSkillIdx(nextSkillIdx);
        setCurrentQuestionInSkill(1);
        const nextSkill = skillsToAssess[nextSkillIdx];
        // Keep using the current adaptive difficulty (server-authoritative)
        loadNextMCQ(nextSkill, currentDifficulty, 0, true, sessionId);
      } else {
        // All MCQs complete -> transition to Coding phase
        setCurrentType('CODING');
      }
    }
  };

  // Run sample cases or submit all cases using the server-held coding problem.
  const handleRunCode = async (mode: 'run' | 'submit' = 'run') => {
    if (!sessionId || !codingData?._id) {
      setError('Assessment session or coding problem not initialized.');
      return;
    }
    setIsExecutingCode(true);
    setExecutionResult(null);
    setError('');
    const langConfig = LANGUAGE_MAP[selectedLanguage] || LANGUAGE_MAP['Python'];
    try {
      const res = await fetch('http://127.0.0.1:8000/api/assessment/evaluate-code', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          session_id: sessionId,
          problem_id: codingData._id,
          mode,
          language_id: langConfig.id,
          source_code: code
        })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Judge0 grading failed');
      setExecutionResult({ ...data, mode });
      return data;
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Coding sandbox unavailable');
      return null;
    } finally {
      setIsExecutingCode(false);
    }
  };

  const handleFinalSubmit = async (skipped = false) => {
    setError('');
    if (!skipped) {
      const result = await handleRunCode('submit');
      if (!result) return; // do not synthesize successful evaluations
    }
    try {
      const res = await fetch('http://127.0.0.1:8000/api/assessment/complete', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ session_id: sessionId })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Could not complete the assessment');
      onFinish(data.report);
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Unable to retrieve verified report');
    }
  };

  const currentSkill = skillsToAssess[currentSkillIdx] || 'Python';
  const totalMCQs = skillsToAssess.length * questionsPerSkill;
  const currentOverallMCQIndex = currentSkillIdx * questionsPerSkill + currentQuestionInSkill;

  return (
    <div className="w-full max-w-5xl mx-auto space-y-6 animate-in fade-in duration-500 pb-16">
      {error && <div role="alert" className="rounded-xl border border-rose-500/40 bg-rose-950/30 p-4 text-sm text-rose-200">{error}</div>}
      {/* Assessment Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 pb-4 border-b border-white/10">
        <div>
          <div className="flex items-center gap-2">
            <span className="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-ping"></span>
            <h1 className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-emerald-400 to-cyan-400">
              SARTA Adaptive Assessment
            </h1>
          </div>
          <p className="text-slate-400 text-xs mt-1">
            {currentType === 'MCQ' ? (
              <>
                Section 4.4 & 4.6 • Item {currentOverallMCQIndex} of {totalMCQs} • Skill: <span className="text-white font-semibold">{currentSkill}</span>
              </>
            ) : (
              <>Section 4.5 • Automated Coding Evaluation Sandbox</>
            )}
          </p>
        </div>

        <div className="flex items-center gap-3">
          {/* Active Adaptive Difficulty Badge */}
          {currentType === 'MCQ' && (
            <span
              className={`px-3 py-1 rounded-full text-xs font-semibold border ${
                currentDifficulty === 'Hard'
                  ? 'bg-rose-500/10 text-rose-400 border-rose-500/30'
                  : currentDifficulty === 'Medium'
                  ? 'bg-amber-500/10 text-amber-400 border-amber-500/30'
                  : 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30'
              }`}
            >
              Adaptive: {currentDifficulty}
            </span>
          )}

          {/* Countdown Timer */}
          <div className="font-mono text-sm px-3.5 py-1.5 rounded-lg bg-slate-900 border border-emerald-500/30 text-emerald-400 shadow-inner">
            ⏱ {formattedTime}
          </div>
        </div>
      </div>

      {/* Progress Bar */}
      <div className="w-full bg-slate-800 rounded-full h-1.5 overflow-hidden">
        <div
          className="bg-gradient-to-r from-blue-500 to-emerald-400 h-1.5 rounded-full transition-all duration-500"
          style={{
            width: `${
              currentType === 'MCQ'
                ? (currentOverallMCQIndex / (totalMCQs + 1)) * 100
                : 95
            }%`
          }}
        ></div>
      </div>

      {/* PHASE 1: ADAPTIVE MCQ */}
      {currentType === 'MCQ' ? (
        <div className="glass-card rounded-2xl p-8 border border-white/10 relative overflow-hidden">
          {loadingQuestion ? (
            <div className="py-16 text-center text-slate-400 animate-pulse">
              Calibrating next adaptive question based on observed performance...
            </div>
          ) : (
            <>
              <div className="flex justify-between items-center mb-4">
                <span className="text-xs uppercase tracking-wider text-slate-400 font-semibold">
                  Competency: <span className="text-emerald-400">{mcqData?.skill}</span>
                </span>
                <span className="text-xs text-slate-400">
                  Question {currentQuestionInSkill} of {questionsPerSkill} for this topic
                </span>
              </div>

              <h2 className="text-xl font-medium text-white mb-8 leading-relaxed">
                {mcqData?.question}
              </h2>

              {/* Options Grid */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8">
                {mcqData?.options?.map((opt: string, idx: number) => {
                  const isSelected = selectedOption === opt;
                  const isCorrect = answerFeedback && opt.trim().toLowerCase() === answerFeedback.correct_answer?.trim().toLowerCase();
                  const isWrongSelected = isAnswerSubmitted && isSelected && !answerFeedback?.is_correct;

                  let optClass = 'border-white/10 bg-white/5 hover:bg-white/10 text-slate-300';

                  if (isAnswerSubmitted) {
                    if (isCorrect) {
                      optClass = 'border-emerald-500 bg-emerald-500/20 text-emerald-300 shadow-[0_0_15px_rgba(16,185,129,0.2)]';
                    } else if (isWrongSelected) {
                      optClass = 'border-rose-500 bg-rose-500/20 text-rose-300';
                    } else {
                      optClass = 'border-white/5 bg-slate-900/40 text-slate-500 opacity-60';
                    }
                  }

                  return (
                    <button
                      key={idx}
                      disabled={isAnswerSubmitted}
                      onClick={() => handleSelectOption(opt)}
                      className={`text-left p-4 rounded-xl border transition-all duration-200 flex items-start gap-3 ${optClass}`}
                    >
                      <span className="font-mono text-xs font-semibold px-2 py-0.5 rounded bg-white/10 text-slate-300">
                        {String.fromCharCode(65 + idx)}
                      </span>
                      <span className="text-sm flex-1">{opt}</span>
                    </button>
                  );
                })}
              </div>

              {/* Instant Feedback Banner */}
              {answerFeedback && (
                <div
                  className={`p-4 rounded-xl border mb-6 text-sm flex items-center justify-between ${
                    answerFeedback.is_correct
                      ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-300'
                      : 'bg-rose-500/10 border-rose-500/30 text-rose-300'
                  }`}
                >
                  <div className="flex items-center gap-2">
                    <span>{answerFeedback.is_correct ? '✓ Correct!' : '✗ Incorrect.'}</span>
                    {!answerFeedback.is_correct && (
                      <span className="text-xs text-slate-300">
                        Correct Answer: <strong className="text-emerald-400">{answerFeedback.correct_answer}</strong>
                      </span>
                    )}
                  </div>
                  <span className="text-xs opacity-75">Adaptive difficulty calibrated</span>
                </div>
              )}

              {/* Action Button */}
              {isAnswerSubmitted && (
                <div className="flex justify-end">
                  <button
                    onClick={handleAdvance}
                    className="px-6 py-2.5 bg-gradient-to-r from-emerald-500 to-cyan-500 hover:from-emerald-400 hover:to-cyan-400 text-white font-medium rounded-xl shadow-lg shadow-emerald-500/25 transition-all flex items-center gap-2"
                  >
                    <span>Continue</span>
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5l7 7-7 7" />
                    </svg>
                  </button>
                </div>
              )}
            </>
          )}
        </div>
      ) : (
        /* PHASE 2: CODING ASSESSMENT */
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Problem Statement Card */}
          <div className="glass-card rounded-2xl p-6 border border-white/10 flex flex-col max-h-[620px] overflow-y-auto">
            <div className="flex items-center gap-2 mb-4">
              <span className="px-2.5 py-0.5 rounded bg-purple-500/20 text-purple-400 text-xs font-semibold border border-purple-500/30">
                Algorithm Problem
              </span>
              <span className="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400 text-xs font-medium">
                {codingData?.difficulty || 'Medium'}
              </span>
              <span className="text-xs text-slate-400 ml-auto">
                Company: <span className="text-white font-medium">{codingData?.company || 'Industry standard'}</span>
              </span>
            </div>

            <h2 className="text-xl font-bold text-white mb-3">
              {codingData?.title || 'Two Sum Problem'}
            </h2>

            <div className="text-slate-300 text-sm leading-relaxed whitespace-pre-wrap flex-grow">
              {codingData?.description}
            </div>

            {/* Hidden & Sample Test Cases */}
            {codingData?.test_cases && (
              <div className="my-4 space-y-2">
                <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider block">
                  Test Cases Verification:
                </span>
                <div className="grid grid-cols-1 gap-2">
                  {codingData.test_cases.map((tc: any) => (
                    <div
                      key={tc.id}
                      className="p-2.5 rounded-lg bg-slate-900/80 border border-white/5 flex items-center justify-between text-xs font-mono"
                    >
                      <div className="flex items-center gap-2">
                        <span className={tc.hidden ? 'text-amber-400' : 'text-blue-400'}>
                          {tc.hidden ? '🔒' : '👁️'} {tc.label}
                        </span>
                        {!tc.hidden && (
                          <span className="text-slate-400 text-[11px]">({tc.input})</span>
                        )}
                      </div>
                      <span className="text-slate-400 text-[11px]">
                        {tc.hidden ? 'Hidden test case' : `Expected: ${tc.expected}`}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Company-Specific LeetCode Problems */}
            {companyProblems.length > 0 && (
              <div className="my-4 space-y-2 border-t border-white/10 pt-4">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-semibold text-cyan-400 uppercase tracking-wider">
                    🏢 {targetCompany || codingData?.company} — Top LeetCode Problems
                  </span>
                  {companyStats && (
                    <span className="text-[11px] text-slate-400">
                      {companyStats.total} total ({companyStats.easy}E / {companyStats.medium}M / {companyStats.hard}H)
                    </span>
                  )}
                </div>
                <div className="grid grid-cols-1 gap-1.5">
                  {companyProblems.map((p: any, idx: number) => (
                    <a
                      key={idx}
                      href={p.link}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="p-2 rounded-lg bg-slate-900/60 border border-white/5 flex items-center justify-between text-xs hover:bg-white/5 transition-colors"
                    >
                      <div className="flex items-center gap-2">
                        <span className={`px-1.5 py-0.5 rounded text-[10px] font-bold ${
                          p.difficulty === 'EASY' ? 'bg-emerald-500/20 text-emerald-400' :
                          p.difficulty === 'HARD' ? 'bg-rose-500/20 text-rose-400' :
                          'bg-amber-500/20 text-amber-400'
                        }`}>
                          {p.difficulty}
                        </span>
                        <span className="text-slate-300">{p.title}</span>
                      </div>
                      <span className="text-slate-500 text-[10px]">{p.topics?.slice(0, 3).join(', ')}</span>
                    </a>
                  ))}
                </div>
              </div>
            )}

            {/* Execution Result Box */}
            {executionResult && (
              <div
                className={`mt-4 p-4 rounded-xl border text-xs font-mono space-y-1 ${
                  executionResult.success
                    ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-300'
                    : 'bg-rose-500/10 border-rose-500/30 text-rose-300'
                }`}
              >
                <div className="font-bold flex items-center justify-between">
                  <span>Status: {executionResult.status}</span>
                  {executionResult.time && <span>Time: {executionResult.time}</span>}
                </div>
                {executionResult.stdout && (
                  <pre className="p-2 bg-black/40 rounded mt-1 overflow-x-auto text-[11px]">
                    {executionResult.stdout}
                  </pre>
                )}
                {executionResult.stderr && (
                  <pre className="p-2 bg-rose-950/40 rounded mt-1 overflow-x-auto text-[11px]">
                    {executionResult.stderr}
                  </pre>
                )}
              </div>
            )}
          </div>

          {/* Code Editor Panel */}
          <div className="glass-card rounded-2xl border border-white/10 overflow-hidden flex flex-col h-[620px]">
            {/* Language Selector Toolbar */}
            <div className="bg-slate-900/90 px-4 py-2.5 border-b border-white/10 flex justify-between items-center">
              <div className="flex items-center gap-2">
                <span className="text-xs text-slate-400">Language:</span>
                <select
                  value={selectedLanguage}
                  onChange={(e) => {
                    const newLang = e.target.value;
                    setSelectedLanguage(newLang);
                    setCode(LANGUAGE_MAP[newLang]?.starter || '');
                  }}
                  className="bg-slate-800 text-white text-xs px-2.5 py-1 rounded border border-white/10 outline-none cursor-pointer"
                >
                  <option value="Python">Python 3 (Judge0)</option>
                  <option value="JavaScript">JavaScript (Node.js)</option>
                  <option value="Java">Java (OpenJDK)</option>
                  <option value="C++">C++ (GCC 9.2)</option>
                </select>
              </div>

              <span className="text-[11px] text-slate-500 font-mono">Sandbox: Judge0 CE</span>
            </div>

            {/* Monaco Editor */}
            <div className="flex-grow">
              <Editor
                height="100%"
                language={LANGUAGE_MAP[selectedLanguage]?.monaco || 'python'}
                theme="vs-dark"
                value={code}
                onChange={(val) => setCode(val || '')}
                options={{
                  minimap: { enabled: false },
                  fontSize: 13,
                  padding: { top: 12 },
                  scrollBeyondLastLine: false
                }}
              />
            </div>

            {/* Action Buttons */}
            <div className="p-3 bg-slate-900/90 border-t border-white/10 flex justify-between items-center gap-2">
              <button
                onClick={() => handleFinalSubmit(true)}
                className="px-3 py-1.5 text-xs text-slate-400 hover:text-white transition-colors"
              >
                Skip Coding
              </button>

              <div className="flex gap-2">
                <button
                  onClick={() => handleRunCode('run')}
                  disabled={isExecutingCode}
                  className="px-4 py-2 rounded-lg bg-white/10 hover:bg-white/20 text-white text-xs font-semibold border border-white/10 transition-all"
                >
                  {isExecutingCode ? 'Running in Sandbox...' : 'Run Code (Judge0)'}
                </button>

                <button
                  onClick={() => handleFinalSubmit(false)}
                  disabled={isExecutingCode || !sessionId}
                  className="px-5 py-2 rounded-lg bg-gradient-to-r from-emerald-500 to-cyan-500 hover:from-emerald-400 hover:to-cyan-400 text-white text-xs font-bold transition-all shadow-lg shadow-emerald-500/20"
                >
                  Submit & Finish Assessment
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
