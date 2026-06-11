import { useEffect, useState } from "react";
import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import { api, API_BASE_URL } from "./api";
import Dashboard from "./Dashboard";
import Applications from "./Applications";
import Companies from "./Companies";
import Emails from "./Emails";
import EmailDetail from "./EmailDetail";
import CompanyDetail from "./CompanyDetail";
import CategoryDetail from "./CategoryDetail";
import "./App.css";

function App() {
  const [loggedIn, setLoggedIn] = useState(null);

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const token = params.get("token");

    if (token) {
      localStorage.setItem("gmail_token", token);
      window.history.replaceState({}, document.title, "/");
      setLoggedIn(true);
      return;
    }

    const savedToken = localStorage.getItem("gmail_token");

    if (savedToken) {
      setLoggedIn(true);
      return;
    }

    api
      .get("/me")
      .then((res) => setLoggedIn(res.data.logged_in))
      .catch(() => setLoggedIn(false));
  }, []);

  function handleLogout() {
    localStorage.removeItem("gmail_token");
    window.location.href = `${API_BASE_URL}/logout`;
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
      <div className="login-page">
        <h1>CareerMail AI</h1>
        <p>
          Track job applications, recruiter messages, interviews, rejections,
          and follow-ups from Gmail.
        </p>

        <a className="login-btn" href={`${API_BASE_URL}/login`}>
          Login with Google
        </a>
      </div>
    );
  }

  return (
    <BrowserRouter>
      <div className="app">
        <header className="header">
          <h1>CareerMail AI</h1>
          <p>AI-powered job search intelligence dashboard</p>

          <nav className="nav">
            <Link to="/">Dashboard</Link>
            <Link to="/applications">Applications</Link>
            <Link to="/companies">Companies</Link>
            <Link to="/emails">Emails</Link>
            <button className="logout-btn" onClick={handleLogout}>
              Logout
            </button>
          </nav>
        </header>

        <main>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/applications" element={<Applications />} />
            <Route path="/companies" element={<Companies />} />
            <Route path="/companies/:companyName" element={<CompanyDetail />} />
            <Route path="/category/:category" element={<CategoryDetail />} />
            <Route path="/emails" element={<Emails />} />
            <Route path="/emails/:id" element={<EmailDetail />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;