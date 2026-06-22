# CareerMail AI — AI Job Search Operating System

CareerMail AI is a multi-user, privacy-first AI job search intelligence platform. It connects to Gmail, filters job-search emails, classifies recruiting communication, tracks application status, analyzes resume-job fit, and generates next actions for job seekers.

This project is designed as a portfolio-ready AI/ML + Software Engineering + Data Engineering project.

## Live Demo

- Frontend: https://careermail-ai.vercel.app
- Backend: https://careermail-ai-backend.onrender.com
- Local frontend: http://localhost:5173
- Local backend docs: http://127.0.0.1:8000/docs

## Product Problem

Job seekers lose track of applications because important emails are mixed with newsletters, job alerts, rejections, recruiter replies, interviews, and offers.

CareerMail AI solves this by turning messy Gmail data into structured job-search intelligence.

## Final Features

### Dual Entry Mode

- Try Demo: recruiters can explore realistic sample data without connecting Gmail.
- Connect Gmail: real users can authenticate with Google OAuth and analyze their own recruiting emails.
- Demo mode is controlled by `DEMO_MODE=true` in `backend/.env`.


### Gmail Intelligence

- Google OAuth login
- Gmail API integration
- Reads recent Gmail messages
- Extracts sender, subject, date, snippet, and body
- Cleans HTML emails
- Ignores non-job emails such as newsletters, Quora Digest, shopping emails, alerts, and promotions

### AI Email Classification

Classifies messages into:

- Application Submitted
- Recruiter Message
- Interview
- Online Assessment
- Offer
- Rejection
- General Job Email
- Not Job Related

### Job Search Dashboard

Tracks:

- Applications tracked
- Recruiter responses
- Response rate
- Interviews
- Interview rate
- Offers
- Rejections
- Active applications
- Follow-ups needed

### Application Tracker

Groups emails by company and shows:

- Company
- Current status
- Last email
- Next action
- AI summary
- Full email history

### AI Resume & Job Match Copilot

Paste a resume/profile and a job description to get:

- Match score
- Role focus
- Matched skills
- Missing skills
- Recommended resume bullets
- Recruiter outreach draft
- Next actions

### Career Agent

Agentic AI workflow that:

1. Reads target role
2. Reads resume/profile
3. Reads job description
4. Evaluates match
5. Finds gaps
6. Recommends portfolio and interview next actions

### Privacy-First Design

Each user should have a private workspace. The production data model uses `user_id` on every sensitive table.

```text
users(id, email, name)
emails(id, user_id, sender, subject, category, summary)
applications(id, user_id, company, status, next_action)
resumes(id, user_id, extracted_text)
ai_outputs(id, user_id, type, result_json)
```

Privacy rules:

- Never store Google tokens in frontend code
- Fetch Gmail data only with the authenticated user's token
- Store user data with `user_id`
- Always query with `WHERE user_id = current_user.id`
- Add delete-data and disconnect-Gmail controls before public launch

## Architecture

```text
Landing Page
   ↓
Try Demo OR Connect Gmail
   ↓
Private User Workspace
   ↓
Gmail Import
   ↓
AI Relevance Filter
   ↓
Email Classifier
   ↓
Application Tracker
   ↓
Dashboard + Follow-ups
   ↓
Resume/JD Match Copilot
   ↓
Career Agent
```

## Tech Stack

### Frontend

- React
- Vite
- React Router
- Axios
- Responsive CSS

### Backend

- FastAPI
- Python
- Google OAuth
- Gmail API
- BeautifulSoup
- Pydantic

### AI Logic

- Rule-based AI-style classifier
- Resume/JD match engine
- Career agent workflow
- Production-ready design for LLM upgrade

## Run Locally

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backend runs at:

```text
http://127.0.0.1:8000
```

API docs:

```text
http://127.0.0.1:8000/docs
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at:

```text
http://localhost:5173
```

## Environment Variables

Create `backend/.env`:

```env
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
SECRET_KEY=change-this-secret
BACKEND_URL=http://localhost:8000
FRONTEND_URL=http://localhost:5173
DEMO_MODE=true
GMAIL_MAX_RESULTS=25
```

Create `frontend/.env`:

```env
VITE_API_BASE_URL=http://localhost:8000
```

## Portfolio Pitch

Built CareerMail AI, a multi-user AI job search intelligence platform that connects to Gmail, classifies recruiting emails, tracks applications, analyzes resume-job fit, and generates personalized next actions while keeping each user's data private.

## Future Improvements

- PostgreSQL database with user-level isolation
- Encrypted Google token storage
- Resume PDF upload and parsing
- RAG over resume, job descriptions, and email history
- LLM-based email classifier
- Calendar integration for interview reminders
- Email follow-up automation
- Stripe billing for SaaS launch

## Author

Soniya Thota

- GitHub: https://github.com/soniya-thota
- LinkedIn: https://www.linkedin.com/in/thotasoni/


## Demo vs Real Gmail

For portfolio sharing, keep:

```env
DEMO_MODE=true
```

This enables the **Try Demo** button so recruiters can use the app immediately.

For real Gmail testing, use:

```env
DEMO_MODE=false
```

Then make sure Google Cloud Console includes this authorized redirect URI:

```text
http://localhost:8000/auth/callback
```

If OAuth fails locally, clear browser cookies for localhost and make sure the frontend uses `http://localhost:5173` and the backend uses `http://localhost:8000`.
