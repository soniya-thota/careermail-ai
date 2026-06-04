import { useEffect, useState } from "react";
import axios from "axios";

function Emails() {
  const [emails, setEmails] = useState([]);

  useEffect(() => {
    axios
      .get("http://localhost:8000/gmail/emails", {
        withCredentials: true,
      })
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
              <td>{email.subject}</td>
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