import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import axios from "axios";

const API_BASE_URL = "https://careermail-ai-backend.onrender.com";

function CategoryDetail() {
  const { category } = useParams();
  const [emails, setEmails] = useState([]);

  useEffect(() => {
    axios
      .get(`${API_BASE_URL}/gmail/emails`, {
        withCredentials: true,
      })
      .then((res) => {
        const allEmails = res.data.emails || [];

        const filtered = allEmails.filter(
          (email) =>
            email.category?.toLowerCase() ===
            decodeURIComponent(category).toLowerCase()
        );

        setEmails(filtered);
      })
      .catch((err) => console.error(err));
  }, [category]);

  return (
    <div>
      <Link to="/">← Back to Dashboard</Link>

      <h2>{decodeURIComponent(category)} Emails</h2>

      {emails.length === 0 ? (
        <p>No emails found for this category in the latest emails.</p>
      ) : (
        <table>
          <thead>
            <tr>
              <th>Company</th>
              <th>Subject</th>
              <th>Date</th>
            </tr>
          </thead>

          <tbody>
            {emails.map((email) => (
              <tr key={email.id}>
                <td>{email.company}</td>
                <td>
                  <Link to={`/emails/${email.id}`}>{email.subject}</Link>
                </td>
                <td>{email.date}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default CategoryDetail;