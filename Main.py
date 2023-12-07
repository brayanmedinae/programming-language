from fastapi import FastAPI
from pydantic import BaseModel
from interpreter import execute_line, get_variables, get_tokens, get_tree
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_methods=["*"],
    allow_headers=["*"],
)


app = FastAPI()

class CodeLine(BaseModel):
    line: str

@app.post("/")
async def root(codeline: CodeLine):
    try:
        return {
            "output": execute_line(codeline.line),
            "tokens": get_tokens(codeline.line),
            "tree": get_tree(codeline.line)
        }
    except Exception as e:
        return {
            "output": "Illegal syntax",
            "tokens": [],
            "tree": []
        }

@app.get("/variables")
def memory():
    return get_variables()
