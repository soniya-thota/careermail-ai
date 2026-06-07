# CareerMail AI

CareerMail AI is a full-stack AI-powered job application email management platform that helps job seekers organize, analyze, and track recruiting communications directly from Gmail.

The platform integrates with Gmail using Google OAuth 2.0, automatically classifies recruiting emails, provides analytics dashboards, and helps users monitor their job search progress through a centralized interface.

---

## Live Demo
**Backend:** https://careermail-ai-backend.onrender.com

**Frontend:** https://careermail-ai.vercel.app



---

## GitHub Repository

https://github.com/soniya-thota/careermail-ai

---

## Features

### Gmail Integration

* Secure Google OAuth 2.0 authentication
* Gmail API integration
* Reads Gmail inbox messages
* Retrieves full email content
* Extracts sender, subject, date, and email previews
* Provides access to detailed email views

### Smart Email Classification

Automatically categorizes emails into:

* Application Submitted
* Recruiter Message
* Interview
* Offer
* Rejection
* Online Assessment
* Incomplete Application
* General Job Email
* Not Job Related

### Analytics Dashboard

* Displays email category statistics
* Tracks recruiting activity across applications
* Visualizes job search communication trends
* Supports category-based drilldowns

### Category Drilldowns

Users can click dashboard categories to view:

* Interview emails
* Recruiter messages
* Rejections
* Offers
* Online assessments
* Application confirmations

### Company Analytics

Groups recruiting communications by company and provides:

* Total email count
* Recruiting activity tracking
* Category breakdowns
* Company-specific insights

### Email Detail View

Displays:

* Company name
* Sender information
* Email subject
* Date received
* Classification category
* Email body preview

---

## API Endpoints

### Authentication

#### Login

```http
GET /login
```

Initiates Google OAuth authentication.

#### OAuth Callback

```http
GET /auth/callback
```

Handles Google OAuth response and creates user session.

#### User Session

```http
GET /me
```

Returns current authentication status.

#### Logout

```http
GET /logout
```

Clears session and logs user out.

---

### Gmail Emails

#### Recent Emails

```http
GET /gmail/emails
```

Returns:

* Company
* Sender
* Subject
* Category
* Date
* Preview

---

### Analytics

#### Dashboard Statistics

```http
GET /analytics
```

Returns category counts for classified emails.

Example:

```json
{
  "Application Submitted": 12,
  "Interview": 4,
  "Recruiter Message": 8,
  "Rejection": 3
}
```

---

### Company Analytics

#### Company Insights

```http
GET /companies
```

Returns recruiting activity grouped by company.

---

### Full Email Details

#### Email Detail

```http
GET /gmail/full-email/{message_id}
```

Returns:

* Company
* Sender
* Subject
* Date
* Category
* Cleaned email body preview

---

## Technology Stack

### Frontend

* React
* JavaScript
* Vite
* React Router
* Axios
* CSS

### Backend

* FastAPI
* Python
* Gmail API
* Google OAuth 2.0
* Authlib
* BeautifulSoup

### Deployment

* Vercel
* Render

### Version Control

* Git
* GitHub

---

## System Architecture

```text
React Frontend (Vercel)
           |
           |
           v
FastAPI Backend (Render)
           |
           |
           v
Google OAuth 2.0
           |
           |
           v
Gmail API
```

---

## Project Highlights

* Built a full-stack cloud-hosted application from scratch
* Implemented Google OAuth authentication
* Integrated directly with Gmail APIs
* Developed automated email classification workflows
* Created analytics dashboards for recruiting insights
* Built category drilldowns and detailed email views
* Deployed production services using Vercel and Render
* Implemented REST APIs for email retrieval and analytics

---

## Future Enhancements

### AI Features

* OpenAI-powered email analysis
* AI-generated email summaries
* Intelligent recruiter interaction insights
* Job search recommendations

### Product Features

* Job application tracking database
* Search and filtering
* Company-specific recruiting timelines
* Recruiter relationship management
* Resume tracking
* Interview preparation insights
* Mobile-first experience

### Platform Improvements

* Token-based authentication
* Improved mobile support
* Enhanced analytics
* Exportable reports

---

## Resume Impact

This project demonstrates experience with:

* Full-Stack Development
* Software Engineering
* REST API Design
* OAuth Authentication
* Cloud Deployment
* Frontend Development
* Backend Development
* API Integration
* Data Processing
* Production Debugging
* Git and GitHub Workflows

---

## Author

### Soniya Thota

Master of Science in Computer Science

University at Buffalo

Focused on:

* Software Engineering
* Artificial Intelligence Applications
* Cloud Systems
* Full-Stack Development
* Scalable Web Applications

---

## License

This project is intended for educational, portfolio, and demonstration purposes.
