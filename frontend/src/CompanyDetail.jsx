import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import axios from "axios";

const API_BASE_URL = "https://careermail-ai-backend.onrender.com";

function CompanyDetail() {
  const { companyName } = useParams();
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
            email.company?.toLowerCase() ===
            decodeURIComponent(companyName).toLowerCase()
        );

        setEmails(filtered);
      })
      .catch((err) => console.error(err));
  }, [companyName]);

  return (
    <div>
      <Link to="/companies">← Back to Companies</Link>

      <h2>{decodeURIComponent(companyName)} Emails</h2>

      <table>
        <thead>
          <tr>
            <th>Subject</th>
            <th>Category</th>
            <th>Date</th>
          </tr>
        </thead>

        <tbody>
          {emails.map((email) => (
            <tr key={email.id}>
              <td>
                <Link to={`/emails/${email.id}`}>{email.subject}</Link>
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

export default CompanyDetail;