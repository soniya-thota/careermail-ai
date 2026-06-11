import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { api } from "./api";

function EmailDetail() {
  const { id } = useParams();
  const [email, setEmail] = useState(null);

  useEffect(() => {
    api
      .get(`/gmail/full-email/${id}`)
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
        <p><strong>Status:</strong> {email.status}</p>
        <p><strong>Next Action:</strong> {email.next_action}</p>
        <p><strong>Summary:</strong> {email.summary}</p>

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