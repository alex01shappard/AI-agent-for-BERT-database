from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import agent
from database import init_db

app = FastAPI()

@app.get('/')
def read_root():
    return {"message": "Welcome to the FastAPI app! Use the /check_prompt endpoint."}
