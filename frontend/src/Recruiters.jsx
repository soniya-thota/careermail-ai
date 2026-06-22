import { useEffect, useState } from "react";
import { api } from "./api";

function Recruiters() {
  const [rows, setRows] = useState([]);

  useEffect(() => {
    api.get("/recruiters").then((res) => setRows(res.data.recruiters || [])).catch(console.error);
  }, []);

  return (
    <div className="page-stack">
      <div className="section-heading">
        <h2>Active Recruiters</h2>
        <p>Recruiter, interview, assessment, and offer-related messages extracted from Gmail.</p>
      </div>
      <table>
        <thead>
          <tr><th>Company</th><th>Sender</th><th>Subject</th><th>Category</th><th>Next Action</th></tr>
        </thead>
        <tbody>
          {rows.map((row, index) => (
            <tr key={`${row.subject}-${index}`}>
              <td>{row.company}</td><td>{row.sender}</td><td>{row.subject}</td><td>{row.category}</td><td>{row.next_action}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Recruiters;
