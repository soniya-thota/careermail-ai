import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "./api";

function Companies() {
  const [companies, setCompanies] = useState({});

  useEffect(() => {
    api
      .get("/companies")
      .then((res) => setCompanies(res.data))
      .catch((err) => console.error(err));
  }, []);

  return (
    <div>
      <h2>Companies</h2>

      <table>
        <thead>
          <tr>
            <th>Company</th>
            <th>Total Emails</th>
          </tr>
        </thead>

        <tbody>
          {Object.entries(companies).map(([name, data]) => (
            <tr key={name}>
              <td>
                <Link to={`/companies/${encodeURIComponent(name)}`}>
                  {name}
                </Link>
              </td>
              <td>{data.total}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Companies;