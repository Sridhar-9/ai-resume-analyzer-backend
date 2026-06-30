from fastapi import Header, HTTPException, status
import os 
from dotenv import load_dotenv
from datetime import datetime
load_dotenv()

APP_API_KEY = os.getenv("BACKEND_API_KEY")

def verify_api_key(x_api_key:str = Header(...)):
    if x_api_key != APP_API_KEY :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")



    

