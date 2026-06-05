import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import Dashboard from "./Dashboard";
import Companies from "./Companies";
import Emails from "./Emails";
import EmailDetail from "./EmailDetail";
import "./App.css";

function App() {
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
            <Route path="/emails" element={<Emails />} />
            <Route path="/emails/:id" element={<EmailDetail />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;