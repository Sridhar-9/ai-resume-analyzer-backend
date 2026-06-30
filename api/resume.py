from fastapi import APIRouter, UploadFile, File, HTTPException, status, Header, Request
from fastapi.responses import JSONResponse
import os
from backend.services.parser import extract_text, save_local, file_type
from backend.services.cleaner import clean_text
from backend.services.analyzer import analyze_resume_with_ai  
from backend.utils.helper import verify_api_key
from datetime import datetime
from slowapi import Limiter
from slowapi.util import get_remote_address

router = APIRouter()

limiter = Limiter(key_func=get_remote_address)
request_log = {}

@router.post("/upload")
@limiter.limit("3/minute")
async def analyse_resume(request: Request,file: UploadFile = File(...), x_api_key: str = Header(...)):


    verify_api_key(x_api_key)

    today = datetime.now().date()
    if today not in request_log:
        request_log.clear()
        request_log[today] = 0
    if request_log[today] >= 15 :
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Daily limit reached")
    request_log[today] += 1 

    detected_mime = await file_type(file)

    if detected_mime != 'application/pdf':
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Wrong file format {detected_mime}. Only PDF allowed."
        )
    
    if file.size and file.size > 2 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File too large")
    
    filename = os.path.basename(file.filename)
    file_content = await file.read()

    save_local(filename, file_content)

    raw_text = extract_text(filename)

    if not raw_text:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not extract text from PDF"
        )

    cleaned_text = clean_text(raw_text)


    try:
        ai_result = analyze_resume_with_ai(cleaned_text)
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "message": "AI processing failed",
                
            }
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "Resume analyzed successfully",
            "analysis": ai_result
        }
    )
