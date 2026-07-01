# ⚙️ AI Resume Analyzer — Backend
 
A FastAPI backend that processes uploaded resumes and returns AI-powered analysis using Google Gemini 2.5 Flash
 
---
 
## ✨ Features
 
- PDF resume upload and parsing
- AI analysis via Google Gemini 2.5 Flash returning:
  - ATS Score
  - Strengths
  - Weaknesses
  - Suggestions
  - Missing Keywords
  - Recommended Roles
- Rate limiting (3 requests/minute per IP)
- CORS restricted to frontend origin
- API key authentication via request headers
---
 
## 🛠️ Tech Stack
 
| Layer | Technology |
|---|---|
| Framework | FastAPI |
| AI Model | Google Gemini 2.5 Flash |
| Rate Limiting | SlowAPI |
| Server | Uvicorn |
| Deployment | Render (free tier) |
 
---
 
## 📁 Project Structure
 
```
backend/
├── main.py               # FastAPI app entry point
├── requirements.txt      # Python dependencies
├── .env                  # Local env variables (gitignored)
├── ai/                   # Gemini AI integration
├── api/
│   └── resume.py         # /upload endpoint
├── models/               # Pydantic models
├── services/
│   └── parser.py         # PDF parsing logic
└── utils/                # Utility functions
```
 
---
 
## 🚀 Run Locally
 
**1. Clone the repo**
```bash
git clone https://github.com/Sridhar-9/ai-resume-analyzer-backend.git
cd ai-resume-analyzer-backend
```
 
**2. Install dependencies**
```bash
pip install -r backend/requirements.txt
```
 
**3. Create a `.env` file inside `backend/`**
```env
GEMINI_API_KEY=your_gemini_api_key
API_SECRET_KEY=your_secret_key
```
 
**4. Run the server**
```bash
uvicorn backend.main:app --reload
```
 
API will be available at `http://localhost:8000`  
Swagger docs at `http://localhost:8000/docs`
 
---
 
## 📮 API Endpoints
 
| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Health check |
| POST | `/upload` | Upload PDF and get analysis |
 
### POST `/upload`
 
**Headers:**
```
X-API-Key: your_secret_key
```
 
**Request:** `multipart/form-data` with a `file` field (PDF only)
 
**Response:**
```json
{
  "analysis": {
    "ats_score": 78,
    "strengths": ["..."],
    "weaknesses": ["..."],
    "suggestions": ["..."],
    "missing_keywords": ["..."],
    "recommended_roles": ["..."]
  }
}
```
 
---
 
## 🔐 Environment Variables
 
| Variable | Description |
|---|---|
| `GEMINI_API_KEY` | Google Gemini API key |
| `API_SECRET_KEY` | Shared secret for frontend authentication |
 
For Render deployment, add these under **Environment** in the Render dashboard.
 
---
 
## 🌐 Deployment
 
Deployed on [Render] free tier.  
Auto-deploys on every push to the `main` branch.
 
> Note: Free tier spins down after 15 minutes of inactivity. First request after sleep may take 30–50 seconds.
 
---
 
## 🤝 Related
 
- [Frontend Repo](https://github.com/Sridhar-9/ai-resume-analyzer-frontend) — Streamlit frontend deployed on Streamlit Community Cloud
 
