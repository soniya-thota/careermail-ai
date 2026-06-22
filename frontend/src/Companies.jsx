import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "./api";

function Companies() {
  const [companies, setCompanies] = useState({});

  useEffect(() => {
    api.get("/companies").then((res) => setCompanies(res.data)).catch(console.error);
  }, []);

  return (
    <div className="page-stack">
      <div className="section-heading">
        <h2>Top Responding Companies</h2>
        <p>Companies ranked by recruiting email activity and categorized communication history.</p>
      </div>

      <table>
        <thead><tr><th>Company</th><th>Total Emails</th><th>Category Breakdown</th></tr></thead>
        <tbody>
          {Object.entries(companies).map(([name, data]) => (
            <tr key={name}>
              <td><Link to={`/companies/${encodeURIComponent(name)}`}>{name}</Link></td>
              <td>{data.total}</td>
              <td>
                <div className="tags">
                  {Object.entries(data.categories || {}).map(([category, count]) => <span key={category}>{category}: {count}</span>)}
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Companies;
