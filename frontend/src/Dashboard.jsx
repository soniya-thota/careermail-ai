import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "./api";

function Dashboard() {
  const [stats, setStats] = useState(null);

  useEffect(() => {
    api
      .get("/job-insights")
      .then((res) => setStats(res.data))
      .catch((err) => console.error(err));
  }, []);

  if (!stats) return <h2>Loading analytics...</h2>;

  return (
    <div>
      <h2>Job Search Intelligence Dashboard</h2>

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