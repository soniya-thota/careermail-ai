import { useState } from "react";
import { api } from "./api";

const sampleResume = `MS Computer Science graduate specializing in AI/ML. Built CareerMail AI, RAG Job Assistant, CDC Lakehouse Pipeline, Kafka streaming pipeline, Airflow/Spark ETL pipeline, TabNet house price prediction, and water quality ML research. Skills include Python, PyTorch, Scikit-learn, FastAPI, React, PostgreSQL, SQL, AWS, Spark, Kafka, Airflow, Docker.`;
const sampleJD = `AI Engineer role building LLM-powered products, RAG workflows, backend APIs, vector search, data pipelines, and production AI features. Requires Python, software engineering, ML fundamentals, cloud, SQL, and strong communication.`;

function CareerAgent() {
  const [targetRole, setTargetRole] = useState("AI/ML Engineer");
  const [resume, setResume] = useState(sampleResume);
  const [jobDescription, setJobDescription] = useState(sampleJD);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  async function runAgent() {
    setLoading(true);
    try {
      const res = await api.post("/ai/career-agent", { target_role: targetRole, resume, job_description: jobDescription });
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
        <span className="eyebrow">Agentic AI</span>
        <h2>Career Agent</h2>
        <p>A multi-step AI workflow that reads your profile, understands the role, finds gaps, and recommends next actions.</p>
      </div>

      <div className="copilot-grid">
        <label>Target Role
          <input className="input" value={targetRole} onChange={(e) => setTargetRole(e.target.value)} />
        </label>
        <label>Resume / Profile Summary
          <textarea value={resume} onChange={(e) => setResume(e.target.value)} />
        </label>
        <label>Job Description
          <textarea value={jobDescription} onChange={(e) => setJobDescription(e.target.value)} />
        </label>
      </div>
      <button className="primary-btn" onClick={runAgent} disabled={loading}>{loading ? "Thinking..." : "Run Career Agent"}</button>

      {result && (
        <div className="insight-panel">
          <div className="score-card">
            <span>Positioning</span>
            <strong>{result.match?.match_score || 0}%</strong>
            <p>{result.positioning}</p>
          </div>
          <div className="result-card wide">
            <h3>Portfolio Pitch</h3>
            <p>{result.portfolio_pitch}</p>
          </div>
          <div className="result-grid">
            {result.roadmap.map((item) => (
              <div className="result-card" key={`${item.step}-${item.title}`}>
                <h3>{item.step}. {item.title}</h3>
                <p>{item.action}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
export default CareerAgent;
