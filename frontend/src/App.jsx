import { useEffect, useState } from "react";
import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import { api, API_BASE_URL } from "./api";
import Dashboard from "./Dashboard";
import Applications from "./Applications";
import Companies from "./Companies";
import Emails from "./Emails";
import EmailDetail from "./EmailDetail";
import CompanyDetail from "./CompanyDetail";
import CategoryEmails from "./CategoryEmails";
import Recruiters from "./Recruiters";
import FollowUps from "./FollowUps";
import AiCopilot from "./AiCopilot";
import CareerAgent from "./CareerAgent";
import Privacy from "./Privacy";
import "./App.css";

function Landing({ onTryDemo, onConnectGmail, backendDemoEnabled, authError }) {
  return (
    <div className="login-page">
      <div className="hero-card landing-card">
        <span className="eyebrow">AI Job Search Operating System</span>
        <h1>CareerMail AI</h1>
        <p>
          Turn messy recruiting emails into structured application tracking, recruiter follow-ups,
          resume-job matching, and AI career next actions.
        </p>

        {authError && (
          <div className="error-banner">
            Google login could not complete. You can still use Try Demo, or retry Connect Gmail after clearing browser cookies.
          </div>
        )}

        <div className="landing-actions">
          <button className="login-btn demo-btn" onClick={onTryDemo} disabled={!backendDemoEnabled}>
            Try Demo
          </button>
          <button className="login-btn" onClick={onConnectGmail}>
            Connect Gmail
          </button>
        </div>

        <div className="feature-strip">
          <span>Gmail Intelligence</span>
          <span>Application Tracker</span>
          <span>AI Resume Match</span>
          <span>Privacy-first Workspace</span>
        </div>

        {!backendDemoEnabled && (
          <p className="helper-text">
            Demo mode is disabled on this backend. Set DEMO_MODE=true to let recruiters explore without Gmail access.
          </p>
        )}
        <p className="helper-text">
          Recruiters can use Try Demo instantly. Real users can connect Gmail to analyze their own recruiting emails.
        </p>
      </div>
    </div>
  );
}

function App() {
  const [loggedIn, setLoggedIn] = useState(null);
  const [demoMode, setDemoMode] = useState(false);
  const [backendDemoEnabled, setBackendDemoEnabled] = useState(false);
  const [authError, setAuthError] = useState(false);

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const token = params.get("token");
    const error = params.get("auth_error");

    if (error) {
      setAuthError(true);
      window.history.replaceState({}, document.title, "/");
    }

    if (token) {
      localStorage.removeItem("careermail_demo");
      localStorage.setItem("gmail_token", token);
      window.history.replaceState({}, document.title, "/");
      setDemoMode(false);
      setLoggedIn(true);
      return;
    }

    const demoSelected = localStorage.getItem("careermail_demo") === "true";
    if (demoSelected) {
      setDemoMode(true);
      setLoggedIn(true);
      return;
    }

    const savedToken = localStorage.getItem("gmail_token");
    if (savedToken) {
      setDemoMode(false);
      setLoggedIn(true);
      return;
    }

    api
      .get("/me")
      .then((res) => {
        setBackendDemoEnabled(Boolean(res.data.demo_mode));
        setLoggedIn(Boolean(res.data.logged_in));
        setDemoMode(false);
      })
      .catch(() => {
        setLoggedIn(false);
        setDemoMode(false);
      });
  }, []);

  function handleTryDemo() {
    localStorage.removeItem("gmail_token");
    localStorage.setItem("careermail_demo", "true");
    setDemoMode(true);
    setLoggedIn(true);
  }

  function handleConnectGmail() {
    localStorage.removeItem("careermail_demo");
    localStorage.removeItem("gmail_token");
    window.location.href = `${API_BASE_URL}/login`;
  }

  async function handleLogout() {
    localStorage.removeItem("gmail_token");
    localStorage.removeItem("careermail_demo");
    try {
      await fetch(`${API_BASE_URL}/logout`, { credentials: "include" });
    } catch (error) {
      console.error("Logout failed:", error);
    }
    window.location.href = window.location.origin;
  }

  if (loggedIn === null) {
    return (
      <div className="loading-page">
        <h2>Loading CareerMail AI...</h2>
      </div>
    );
  }

  if (!loggedIn) {
    return (
      <Landing
        onTryDemo={handleTryDemo}
        onConnectGmail={handleConnectGmail}
        backendDemoEnabled={backendDemoEnabled}
        authError={authError}
      />
    );
  }

  return (
    <BrowserRouter>
      <div className="app">
        <header className="header">
          <div>
            <span className="eyebrow">AI Job Search Intelligence</span>
            <h1>CareerMail AI</h1>
            <p>Recruiter analytics, application tracking, follow-up detection, and resume-job matching.</p>
            {demoMode && <div className="demo-banner">Demo mode is active. This uses realistic sample recruiting emails.</div>}
          </div>

          <nav className="nav">
            <Link to="/">Dashboard</Link>
            <Link to="/applications">Applications</Link>
            <Link to="/follow-ups">Follow-Ups</Link>
            <Link to="/recruiters">Recruiters</Link>
            <Link to="/companies">Companies</Link>
            <Link to="/emails">Emails</Link>
            <Link to="/ai-copilot">AI Copilot</Link>
            <Link to="/career-agent">Career Agent</Link>
            <Link to="/privacy">Privacy</Link>
            <button className="logout-btn" onClick={handleLogout}>{demoMode ? "Exit Demo" : "Logout"}</button>
          </nav>
        </header>

        <main>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/applications" element={<Applications />} />
            <Route path="/follow-ups" element={<FollowUps />} />
            <Route path="/recruiters" element={<Recruiters />} />
            <Route path="/companies" element={<Companies />} />
            <Route path="/companies/:companyName" element={<CompanyDetail />} />
            <Route path="/emails" element={<Emails />} />
            <Route path="/emails/:id" element={<EmailDetail />} />
            <Route path="/category/:categoryName" element={<CategoryEmails />} />
            <Route path="/ai-copilot" element={<AiCopilot />} />
            <Route path="/career-agent" element={<CareerAgent />} />
            <Route path="/privacy" element={<Privacy />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;
