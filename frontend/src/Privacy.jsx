function Privacy() {
  return (
    <div className="page-stack">
      <div className="section-heading">
        <span className="eyebrow">Privacy-first architecture</span>
        <h2>Private Workspaces for Every Job Seeker</h2>
        <p>CareerMail AI is designed so each user only sees their own Gmail emails, resumes, applications, analytics, and AI outputs.</p>
      </div>

      <div className="result-grid">
        <div className="result-card">
          <h3>🔐 User Isolation</h3>
          <p>Every future database table should include <strong>user_id</strong>. Every query must filter by the authenticated user.</p>
        </div>
        <div className="result-card">
          <h3>📨 Gmail Safety</h3>
          <p>Gmail data is fetched with the current user token only. Non-job emails are ignored before they reach the tracker.</p>
        </div>
        <div className="result-card">
          <h3>🧹 Data Controls</h3>
          <p>Before public launch, add delete-data, disconnect Gmail, token encryption, and clear privacy notice flows.</p>
        </div>
      </div>

      <div className="result-card wide">
        <h3>Production Data Model</h3>
        <pre className="code-block">{`users(id, email, name)
emails(id, user_id, sender, subject, category, summary)
applications(id, user_id, company, status, next_action)
resumes(id, user_id, extracted_text)
ai_outputs(id, user_id, type, result_json)`}</pre>
      </div>
    </div>
  );
}
export default Privacy;
