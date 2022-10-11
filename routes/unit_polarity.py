# Created by Wellington Braga
# on 2022-09-27 11:40:46


from models.custom_vader import SentimentIntensityAnalyzer
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from datetime import datetime
from fastapi import Request
import numpy as np
import json


class SucessResponse(BaseModel):  
    event = "unit_polarity"
    sucess = True
    polarity = 0
    describe = "neutro"

class ValidationErrorResponse(BaseModel):  
    event = "unit_polarity"
    describe = "indefinido"
    sucess = False

class ServerErrorResponse(BaseModel):  
    event = "unit_polarity"
    describe = "O servidor encontrou uma situação com a qual não sabe lidar."
    sucess = False

def __log(sentence: str, polarity: float, describe: str, request: Request, mult: bool):
    """armazena frases indefinidas, para análise posterior"""
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        log = json.dumps(
            {
                "event": "unit_polarity", 
                "date": date, 
                "describe": describe, 
                "polarity": polarity, 
                "sentence": sentence, 
                "client": request.client,
                "mult": mult
            }
        )
        with open('./dados/logs.json', 'a') as f: f.write(f'{log},\n')
    except Exception as e: 
        log = json.dumps({"event": "log_register", "date": date, "describe": str(e)})
        with open('./dados/logs.json', 'a') as f: f.write(f'{log},\n')

def get_unity(request: Request, sentence: str, sia: SentimentIntensityAnalyzer, condictions: list, describes: list, mult=False):
    """ ## Consulta Unitária de Polaridade de Sentença """

    response = {"event": "unit_polarity", "sucess": False}

    if sentence in [None, '', 'None', 'Null', 'NaN', 'nan', 'none', 'null']: 
        response["error"] = "É necessário informar uma sentença com algumas palavras!"
        return JSONResponse(status_code=400, content=response)
    elif sentence.isnumeric():
        response["error"] = "Não é possível extrair sentimento de NÚMEROS!"
        return JSONResponse(status_code=400, content=response)

    try: 
        polarity = sia.polarity_scores(sentence)[0]["compound"]

        if polarity is not None:
            describe = np.select(condictions(polarity), describes.keys()).item()
            response["polarity"] = polarity
            response["describe"] = describe
            response["sucess"] = True
            __log(sentence, polarity, describe, request, mult)
            return JSONResponse(status_code=200, content=response)
        
        else:
            # __log(sentence, polarity, "indefinido", request)
            return JSONResponse(status_code=422, content=ValidationErrorResponse().__dict__)

    except Exception as e: 
        response["error"] = str(e)
        # __log(sentence, None, e, request)
        return JSONResponse(status_code=500, content=response)
