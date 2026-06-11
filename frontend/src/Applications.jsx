import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "./api";

function Applications() {
  const [applications, setApplications] = useState([]);

  useEffect(() => {
    api
      .get("/applications")
      .then((res) => setApplications(res.data.applications || []))
      .catch((err) => console.error(err));
  }, []);

  return (
    <div>
      <h2>Application Tracker</h2>

      {applications.length === 0 ? (
        <p>No tracked applications found yet.</p>
      ) : (
        <table>
          <thead>
            <tr>
              <th>Company</th>
              <th>Status</th>
              <th>Last Email</th>
              <th>Next Action</th>
              <th>Summary</th>
            </tr>
          </thead>

          <tbody>
            {applications.map((app) => (
              <tr key={app.company}>
                <td>
                  <Link to={`/companies/${encodeURIComponent(app.company)}`}>
                    {app.company}
                  </Link>
                </td>
                <td>{app.status}</td>
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