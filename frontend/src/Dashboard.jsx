import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import axios from "axios";

const API_BASE_URL = "https://careermail-ai-backend.onrender.com";

function Dashboard() {
  const [stats, setStats] = useState(null);

  useEffect(() => {
    axios
      .get(`${API_BASE_URL}/analytics`, {
        withCredentials: true,
      })
      .then((res) => setStats(res.data))
      .catch((err) => console.error(err));
  }, []);

  if (!stats) return <h2>Loading analytics...</h2>;

  return (
    <div>
      <h2>Analytics Dashboard</h2>

      <div className="cards">
        {Object.entries(stats).map(([key, value]) => (
          <Link
            key={key}
            to={`/category/${encodeURIComponent(key)}`}
            style={{ textDecoration: "none", color: "inherit" }}
          >
            <div className="card">
              <h3>{key}</h3>
              <h1>{value}</h1>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}

export default Dashboard;