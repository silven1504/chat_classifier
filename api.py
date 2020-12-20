import json
import base64
import numpy as np

from fastapi import FastAPI

import model

model = model.Model()
app = FastAPI()


@app.get('/predict')
async def predict(input: str = ""):
    json_input = json.loads(decode(input))
    return json.dumps(model.predict(json_input).reshape(-1).tolist())


@app.get('/predict_proba')
async def prediction_proba(input: str = ""):
    json_input = json.loads(decode(input))
    return json.dumps(model.predict_proba(json_input).reshape(-1).tolist())


def decode(input: str):
    decodedBytes = base64.b64decode(input)
    decodedStr = str(decodedBytes, "utf-8")
    return decodedStr
