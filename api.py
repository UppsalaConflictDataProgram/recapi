import os
from typing import List, Literal, Union
from fastapi import FastAPI
from pydantic import BaseModel

import math

import numpy as np
from operator import add,mul

SIZE = os.getenv("API_TEST_SIZE",4)
ax = int(math.pow(10,int(SIZE)))
ext = (ax,ax)

class Step(BaseModel):
    type: Literal["transform","base"]
    value: Union[int,float,str]
    name: str

class Query(BaseModel):
    steps: List[Step]
    base: int 

transforms = {
    "add": add,
    "multiply": mul
}

app = FastAPI()

def recurseResolve(query)->np.ndarray:
    try:
        step = query.steps.pop()
        return transforms[step.name](
                recurseResolve(query),
                step.value
            )
    except IndexError:
        return np.full(ext,query.base)

@app.post("/")
def resolve(query: Query)->str:
    return str(recurseResolve(query))
