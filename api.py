from fastapi import FastAPI
from pydantic import BaseModel
from code_assistant import CodeAssistant
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
assistant = CodeAssistant()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    context: str
    prompt: str

@app.post("/generate")
async def generate(query: Query):
    res = assistant.generate_code(query.context, query.prompt)
    
    print(f"response: {res}")
    print(f"code: {assistant.parse_code('json', res)}")
    
    return {
        "response": res, 
        "code": assistant.parse_code('json', res)
    }
