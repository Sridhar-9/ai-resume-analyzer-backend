from fastapi import FastAPI
from backend.api.resume import router, limiter
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello! Upload your resume as a pdf and analyze it."}

@app.get("/about")
def about():
    return {"message": "This API analyzes resumes using AI."}

app.state.limiter = limiter

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request, exc):
    return JSONResponse(
        status_code=429,
        content={"error": "Too many requests. Try again later."},
    )


app.add_middleware(

    CORSMiddleware,
    allow_origins=["https://ai-resume-analyzer-bv2s755bacrazfmrpzbuf2.streamlit.app"],  # Streamlit
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)


app.include_router(router)

