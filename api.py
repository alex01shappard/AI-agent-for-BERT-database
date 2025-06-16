from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import agent

app = FastAPI()


@app.get('/')
def read_root():
    return {"message": "Welcome to the FastAPI app!"
                       "Use the /check_prompt endpoint."}


app.add_middleware(
    CORSMiddleware,
    # или ["http://localhost:3000"] для большей безопасности
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic-модель для JSON-запроса


class PromptRequest(BaseModel):
    prompt: str

# POST-запрос от React


@app.post("/check_prompt")
async def handle_prompt(request: PromptRequest):
    answer = agent.main_with_prompt(request.prompt)
    return {"answer": answer}
