import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "./api";

function Dashboard() {
  const [stats, setStats] = useState(null);

  const categoryRoutes = {
    Interviews: "Interview",
    Offers: "Offer",
    Rejections: "Rejection",
    "Recruiter Responses": "Recruiter Message",
  };

  const applicationRoutes = [
    "Applications Tracked",
    "Active Applications",
    "Follow-Ups Needed",
  ];

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
        {Object.entries(stats).map(([key, value]) => {
          let linkTo = null;

          if (categoryRoutes[key]) {
            linkTo = `/category/${encodeURIComponent(categoryRoutes[key])}`;
          }

          if (applicationRoutes.includes(key)) {
            linkTo = "/applications";
          }

          const card = (
            <div className="card">
              <h3>{key}</h3>
              <h1>{value}</h1>
            </div>
          );

          return linkTo ? (
            <Link
              key={key}
              to={linkTo}
              style={{ textDecoration: "none", color: "inherit" }}
            >
              {card}
            </Link>
          ) : (
            <div key={key}>{card}</div>
          );
        })}
      </div>
    </div>
  );
}

export default Dashboard;