import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { api } from "./api";

function CategoryDetail() {
  const { category } = useParams();
  const [emails, setEmails] = useState([]);

  useEffect(() => {
    api
      .get("/gmail/emails")
      .then((res) => {
        const allEmails = res.data.emails || [];
        const decodedCategory = decodeURIComponent(category).toLowerCase();

        const filtered = allEmails.filter(
          (email) => email.category?.toLowerCase() === decodedCategory
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