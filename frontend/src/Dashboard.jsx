import { useEffect, useState } from "react";
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
          <div className="card" key={key}>
            <h3>{key}</h3>
            <h1>{value}</h1>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Dashboard;