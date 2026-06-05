import { useEffect, useState } from "react";
import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import axios from "axios";
import Dashboard from "./Dashboard";
import Companies from "./Companies";
import Emails from "./Emails";
import EmailDetail from "./EmailDetail";
import CompanyDetail from "./CompanyDetail";
import "./App.css";

const API_BASE_URL = "https://careermail-ai-backend.onrender.com";

function App() {
  const [loggedIn, setLoggedIn] = useState(null);

  useEffect(() => {
    axios
      .get(`${API_BASE_URL}/me`, {
        withCredentials: true,
      })
      .then((res) => setLoggedIn(res.data.logged_in))
      .catch(() => setLoggedIn(false));
  }, []);

  if (loggedIn === null) {
    return <h2>Loading...</h2>;
  }

  if (!loggedIn) {
    return (
      <div className="login-page">
        <h1>CareerMail AI</h1>
        <p>Your AI-powered job application email dashboard</p>

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
          <p>Your AI-powered job application email dashboard</p>

          <nav className="nav">
            <Link to="/">Dashboard</Link>
            <Link to="/companies">Companies</Link>
            <Link to="/emails">Emails</Link>
          </nav>
        </header>

        <main>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/companies" element={<Companies />} />
            <Route path="/companies/:companyName" element={<CompanyDetail />} />
            <Route path="/emails" element={<Emails />} />
            <Route path="/emails/:id" element={<EmailDetail />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;