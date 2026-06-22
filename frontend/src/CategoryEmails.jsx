import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { api } from "./api";

function CategoryEmails() {
  const { categoryName } = useParams();
  const category = decodeURIComponent(categoryName);
  const [emails, setEmails] = useState([]);

  useEffect(() => {
    api.get("/gmail/emails").then((res) => {
      const filtered = (res.data.emails || []).filter((email) => email.category === category);
      setEmails(filtered);
    }).catch(console.error);
  }, [category]);

  return (
    <div className="page-stack">
      <Link to="/">← Back to Dashboard</Link>
      <div className="section-heading"><h2>{category} Emails</h2></div>
      <table>
        <thead><tr><th>Company</th><th>Subject</th><th>Date</th></tr></thead>
        <tbody>
          {emails.map((email) => (
            <tr key={email.id}>
              <td>{email.company}</td><td><Link to={`/emails/${email.id}`}>{email.subject}</Link></td><td>{email.date}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default CategoryEmails;
