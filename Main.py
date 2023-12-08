from fastapi import FastAPI
from pydantic import BaseModel
from interpreter import execute_line, get_variables, get_tokens, get_tree
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import preprocessor

counter_lock = asyncio.Lock()
counter = 0

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_methods=["*"],
    allow_headers=["*"],
)

class CodeLine(BaseModel):
    line: str

@app.post("/")
async def root(codeline: CodeLine):
    global counter
    codeline.line = preprocessor.preprocess(codeline.line)

    async with counter_lock:
        counter += 1
    
    if codeline.line == "":
        return {
            "output": None,
            "isSuccess": True,
            "line": counter,
            "tokens": [],
            "tree": [],
        }
    
    try:
        return {
            "output": execute_line(codeline.line),
            "isSuccess": True,
            "line": counter,
            "tokens": get_tokens(codeline.line),
            "tree": get_tree(codeline.line),
        }
    except Exception:
        return {
            "output": "Illegal syntax",
            "isSuccess": False,
            "line": counter,
            "tokens": [],
            "tree": [],
        }

@app.get("/variables")
def memory():
    return get_variables()

@app.get("/reset")
def reset():
    global counter
    global variables
    counter = 0
    variables = {}
    return {
        "output": "Reset successful",
        "isSuccess": True,
        "line": counter,
        "tokens": [],
        "tree": [],
    }