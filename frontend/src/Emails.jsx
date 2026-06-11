import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "./api";

function Emails() {
  const [emails, setEmails] = useState([]);

  useEffect(() => {
    api
      .get("/gmail/emails")
      .then((res) => setEmails(res.data.emails || []))
      .catch((err) => console.error(err));
  }, []);

  return (
    <div>
      <h2>Recent Emails</h2>

      <table>
        <thead>
          <tr>
            <th>Company</th>
            <th>Subject</th>
            <th>Category</th>
            <th>Date</th>
          </tr>
        </thead>

        <tbody>
          {emails.map((email) => (
            <tr key={email.id}>
              <td>{email.company}</td>
              <td>
                <Link to={`/emails/${email.id}`}>
                  {email.subject}
                </Link>
              </td>
              <td>{email.category}</td>
              <td>{email.date}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Emails;