import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "./api";

function FollowUps() {
  const [items, setItems] = useState([]);

  useEffect(() => {
    api.get("/follow-ups").then((res) => setItems(res.data.follow_ups || [])).catch(console.error);
  }, []);

  return (
    <div className="page-stack">
      <div className="section-heading">
        <h2>Follow-Ups Needed</h2>
        <p>Companies that need action based on recruiter replies, interviews, assessments, or incomplete applications.</p>
      </div>
      <table>
        <thead><tr><th>Company</th><th>Status</th><th>Next Action</th><th>Summary</th></tr></thead>
        <tbody>
          {items.map((item) => (
            <tr key={item.company}>
              <td><Link to={`/companies/${encodeURIComponent(item.company)}`}>{item.company}</Link></td>
              <td>{item.status}</td><td>{item.next_action}</td><td>{item.summary}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default FollowUps;
