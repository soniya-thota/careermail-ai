import { useEffect, useState } from "react";
import axios from "axios";

const API_BASE_URL = "https://careermail-ai-backend.onrender.com";

function Companies() {
  const [companies, setCompanies] = useState({});

  useEffect(() => {
    axios
      .get(`${API_BASE_URL}/companies`, {
        withCredentials: true,
      })
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
              <td>{name}</td>
              <td>{data.total}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Companies;