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

  const applicationRoutes = ["Applications Tracked", "Active Applications"];

  useEffect(() => {
    api
      .get("/analytics")
      .then((res) => {
        const data = res.data || {};

        const applications =
          (data["Application Submitted"] || 0) +
          (data["Online Assessment"] || 0) +
          (data["Recruiter Message"] || 0) +
          (data["Interview"] || 0) +
          (data["Offer"] || 0) +
          (data["Rejection"] || 0);

        const recruiterResponses =
          (data["Recruiter Message"] || 0) +
          (data["Interview"] || 0) +
          (data["Online Assessment"] || 0) +
          (data["Offer"] || 0);

        const interviews = data["Interview"] || 0;
        const offers = data["Offer"] || 0;
        const rejections = data["Rejection"] || 0;

        setStats({
          "Applications Tracked": applications,
          "Recruiter Responses": recruiterResponses,
          "Response Rate": applications
            ? `${((recruiterResponses / applications) * 100).toFixed(2)}%`
            : "0%",
          Interviews: interviews,
          "Interview Rate": applications
            ? `${((interviews / applications) * 100).toFixed(2)}%`
            : "0%",
          Offers: offers,
          Rejections: rejections,
          "Active Applications": Math.max(applications - offers - rejections, 0),
          "Follow-Ups Needed": 0,
        });
      })
      .catch((error) => {
        console.error("Failed to load dashboard analytics:", error);
        setStats({});
      });
  }, []);

  if (!stats) return <h2>Loading analytics...</h2>;

  return (
    <div className="page-stack">
      <div className="section-heading">
        <h2>Job Search Intelligence Dashboard</h2>
        <p>
          Track applications, recruiter responses, interview activity, response
          rate, and follow-up needs from recruiting emails.
        </p>
      </div>

      <div className="cards">
        {Object.entries(stats).map(([key, value]) => {
          let linkTo = null;

          if (categoryRoutes[key]) {
            linkTo = `/category/${encodeURIComponent(categoryRoutes[key])}`;
          }

          if (applicationRoutes.includes(key)) {
            linkTo = "/applications";
          }

          if (key === "Follow-Ups Needed") {
            linkTo = "/follow-ups";
          }

          const card = (
            <div className="card">
              <h3>{key}</h3>
              <h1>{value}</h1>
            </div>
          );

          return linkTo ? (
            <Link key={key} to={linkTo} className="card-link">
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