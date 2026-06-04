# CareerMail AI

CareerMail AI is an AI-powered job application email management platform that helps job seekers organize, analyze, and track their recruiting communications directly from Gmail.

## Features

### Gmail Integration

* Secure Google OAuth authentication
* Read Gmail inbox messages
* Retrieve full email content
* Analyze job-related communications

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

### Company Analytics

Groups emails by company and provides:

* Total email count per company
* Category breakdown
* Recruiting activity insights

### Email Dashboard APIs

#### Get Emails

GET /gmail/emails

Returns recent Gmail messages with:

* Company
* Sender
* Subject
* Category
* Date
* Email preview

#### Analytics

GET /analytics

Provides overall statistics for all classified emails.

#### Company Analytics

GET /companies

Displays recruiting activity grouped by company.

#### Full Email View

GET /gmail/full-email/{message_id}

Retrieves full email content and classification.

## Tech Stack

Backend:

* FastAPI
* Python
* Gmail API
* Google OAuth

Authentication:

* Authlib
* OAuth 2.0

Data Processing:

* Email Classification Engine
* Company Extraction Engine

Version Control:

* Git
* GitHub

## Project Goals

CareerMail AI aims to become an intelligent career assistant capable of:

* Tracking job applications
* Monitoring recruiter communications
* Identifying interviews and offers
* Generating AI-powered summaries
* Providing actionable job search analytics

## Future Enhancements

* OpenAI-powered email analysis
* Job application tracking database
* Recruiter relationship management
* AI-generated email summaries
* Personalized job search dashboard
* Resume and interview insights

## Author

Soniya Thota

Master of Science in Computer Science

University at Buffalo

Focused on Software Engineering, AI Applications, Cloud Systems, and Full-Stack Development.
