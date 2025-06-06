from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import agent
from database import init_db

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def form_get(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/check_prompt", response_class=HTMLResponse)
async def handle_form(request: Request, prompt_input: str = Form(...)):
    answer = agent.main_with_prompt(prompt_input)  # Добавим отдельную функцию
    return templates.TemplateResponse("index.html", {
        "request": request,
        "prompt_input": prompt_input,
        "answer": answer
    })
