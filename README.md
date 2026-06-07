# AI Resume Screener

An AI-powered REST API + web app that screens resumes against job descriptions using Claude (Anthropic API).

## Features
- Upload PDF or DOCX resume
- Paste any job description
- Get ATS score (0-100), matched skills, missing skills, strengths, and improvement tips
- Saves all results to MySQL
- Deploy-ready for Railway

## Tech Stack
- **Backend**: Python, FastAPI
- **AI**: Claude API (Anthropic)
- **File Parsing**: PyPDF2, python-docx
- **Database**: MySQL
- **Deploy**: Railway

## Project Structure
```
ai-resume-screener/
├── app/
│   ├── parser.py       # PDF/DOCX text extraction
│   ├── screener.py     # Claude AI screening logic
│   └── database.py     # MySQL operations
├── static/
│   └── index.html      # Frontend UI
├── main.py             # FastAPI app entry point
├── requirements.txt
├── Procfile            # Railway deployment
└── .env.example
```

## Local Setup

1. Clone the repo
2. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy `.env.example` to `.env` and fill in your keys:
   ```
   ANTHROPIC_API_KEY=your_key_here
   DB_HOST=localhost
   DB_USER=root
   DB_PASSWORD=your_password
   DB_NAME=resume_screener
   ```
5. Create MySQL database:
   ```sql
   CREATE DATABASE resume_screener;
   ```
6. Run the app:
   ```bash
   uvicorn main:app --reload
   ```
7. Open http://localhost:8000

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/screen` | Screen a resume |
| GET | `/history` | Get past screening results |
| GET | `/health` | Health check |

### POST /screen
```bash
curl -X POST http://localhost:8000/screen \
  -F "resume=@resume.pdf" \
  -F "job_description=We are looking for a Java developer..."
```

Response:
```json
{
  "score": 72,
  "matched_skills": ["Java", "REST API", "MySQL"],
  "missing_skills": ["Spring Boot", "Docker"],
  "strengths": ["Strong backend foundation"],
  "improvements": ["Add Spring Boot projects", "Learn Docker basics"],
  "summary": "Good match for backend roles but missing cloud/DevOps skills."
}
```

## Deploy on Railway

1. Push code to GitHub
2. Go to [railway.app](https://railway.app) → New Project → Deploy from GitHub
3. Add environment variables in Railway dashboard
4. Add a MySQL plugin in Railway
5. Done — live URL ready

## Built by
Rohan Hosamane — MCA, Presidency University Bangalore
