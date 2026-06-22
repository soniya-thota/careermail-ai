import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "./api";

function Applications() {
  const [applications, setApplications] = useState([]);

  useEffect(() => {
    api.get("/applications").then((res) => setApplications(res.data.applications || [])).catch(console.error);
  }, []);

  return (
    <div className="page-stack">
      <div className="section-heading">
        <h2>Application Tracker</h2>
        <p>Company-level status tracker built from categorized Gmail recruiting communication.</p>
      </div>

      {applications.length === 0 ? (
        <p>No tracked applications found yet.</p>
      ) : (
        <table>
          <thead>
            <tr><th>Company</th><th>Status</th><th>Last Email</th><th>Next Action</th><th>Summary</th></tr>
          </thead>
          <tbody>
            {applications.map((app) => (
              <tr key={app.company}>
                <td><Link to={`/companies/${encodeURIComponent(app.company)}`}>{app.company}</Link></td>
                <td><span className="status-pill">{app.status}</span></td>
                <td>{app.last_email_date}</td>
                <td>{app.next_action}</td>
                <td>{app.summary}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default Applications;
