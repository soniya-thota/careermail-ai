import { useState } from "react";
import { api } from "./api";

const sampleResume = `MS Computer Science graduate with AI/ML track. Experience with Python, PyTorch, Scikit-learn, FastAPI, React, PostgreSQL, Spark, Kafka, Airflow, AWS, and data engineering pipelines. Built CareerMail AI, RAG Job Assistant, CDC Lakehouse Pipeline, and ML research projects.`;

const sampleJob = `We are hiring an AI Engineer to build LLM-powered applications, RAG workflows, APIs, and data-driven product features. The role requires Python, machine learning, vector databases, backend development, cloud deployment, and strong software engineering fundamentals.`;

function AiCopilot() {
  const [resume, setResume] = useState(sampleResume);
  const [jobDescription, setJobDescription] = useState(sampleJob);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  async function analyze() {
    setLoading(true);
    try {
      const res = await api.post("/ai/resume-match", {
        resume,
        job_description: jobDescription,
      });
      setResult(res.data);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="page-stack">
      <div className="section-heading">
        <h2>AI Resume & Job Match Copilot</h2>
        <p>Paste a resume summary and job description to generate a match score, missing skills, bullet improvements, and recruiter outreach.</p>
      </div>

      <div className="copilot-grid">
        <label>
          Resume / Profile Summary
          <textarea value={resume} onChange={(e) => setResume(e.target.value)} rows={12} />
        </label>
        <label>
          Job Description
          <textarea value={jobDescription} onChange={(e) => setJobDescription(e.target.value)} rows={12} />
        </label>
      </div>

      <button className="primary-btn" onClick={analyze} disabled={loading}>
        {loading ? "Analyzing..." : "Analyze Match"}
      </button>

      {result && (
        <div className="insight-panel">
          <div className="score-card">
            <span>Match Score</span>
            <strong>{result.match_score}%</strong>
            <p>{result.role_focus}</p>
          </div>

          <div className="result-grid">
            <div className="result-card">
              <h3>Matched Skills</h3>
              <div className="tags">{result.matched_skills.map((item) => <span key={item}>{item}</span>)}</div>
            </div>
            <div className="result-card">
              <h3>Missing Skills</h3>
              <div className="tags warn">{result.missing_skills.map((item) => <span key={item}>{item}</span>)}</div>
            </div>
            <div className="result-card wide">
              <h3>Recommended Resume Bullets</h3>
              <ul>{result.recommended_resume_bullets.map((item) => <li key={item}>{item}</li>)}</ul>
            </div>
            <div className="result-card wide">
              <h3>Recruiter Outreach Draft</h3>
              <p>{result.recruiter_outreach}</p>
            </div>
            <div className="result-card wide">
              <h3>Next Actions</h3>
              <ul>{result.next_actions.map((item) => <li key={item}>{item}</li>)}</ul>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default AiCopilot;
