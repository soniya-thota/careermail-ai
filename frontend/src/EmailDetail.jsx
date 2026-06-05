import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import axios from "axios";

function EmailDetail() {
  const { id } = useParams();
  const [email, setEmail] = useState(null);

  useEffect(() => {
    axios
      .get(`http://localhost:8000/gmail/full-email/${id}`, {
        withCredentials: true,
      })
      .then((res) => setEmail(res.data))
      .catch((err) => console.error(err));
  }, [id]);

  if (!email) {
    return <h2>Loading email...</h2>;
  }

  return (
    <div className="email-detail">
      <Link to="/emails">← Back to Emails</Link>

      <div className="card" style={{ marginTop: "20px", width: "100%" }}>
        <h2>{email.subject}</h2>

        <p><strong>Company:</strong> {email.company}</p>
        <p><strong>From:</strong> {email.from}</p>
        <p><strong>Date:</strong> {email.date}</p>
        <p><strong>Category:</strong> {email.category}</p>

        <hr />

        <h3>Email Body</h3>
        <div className="email-body">
          {email.body_preview || email.snippet || "Preview unavailable"}
        </div>
      </div>
    </div>
  );
}

export default EmailDetail;