from fastapi import FastAPI
from pydantic import BaseModel
from interpreter import execute_line, get_variables, get_tokens, get_tree


app = FastAPI()

class CodeLine(BaseModel):
    line: str

@app.post("/")
async def root(codeline: CodeLine):
    return {
        "output": execute_line(codeline.line),
        "tokens": get_tokens(codeline.line),
        "tree": get_tree(codeline.line)
    }

@app.get("/variables")
def memory():
    return get_variables()
