# Created by Wellington Braga
# on 2022-09-27 11:40:58


## starta serviço ##
# python3 -m  uvicorn api:app --host 192.168.0.41 --port 8560 --reload
## Mata o serviço ##
# kill -9 $(ps -A | grep python | awk '{print $1}')

from routes.unit_polarity import SucessResponse, ValidationErrorResponse, ServerErrorResponse, get_unity
from routes.multi_polarity import SucessResponse, ValidationErrorResponse, ServerErrorResponse, post_multi

from models.custom_vader import SentimentIntensityAnalyzer
from fastapi.openapi.utils import get_openapi
from fastapi import FastAPI, Request

# Análise de Sentimentos com custom_vader
sia = SentimentIntensityAnalyzer()
condictions = lambda pol: [pol is None, pol < -.45, -.45 <= pol < -.2, -.2 <= pol < .2, .2 <= pol < .45, pol > .45]
describes = {"indefinido": "😵", 'negativo': "😡", 'irrazoavel': "🙁", 'neutro': "😐", 'razoavel': "🙂", 'positivo': "🤩"}

# RestAPI
app = FastAPI(docs_url="/tests", redoc_url="/docs")

def my_schema():
   openapi_schema = get_openapi(
       title="SentiTrack",
       description="A API Ideal para identificação de sentimentos em mensagens de texto.",
       version="0.1",
       routes=app.routes,
       contact = {
           "name": "AlerTrack",
           "url": "https://alertrack.com.br/",
           "email": "suporte@alertrack.com.br"
       },
   )
   
   app.openapi_schema = openapi_schema
   return app.openapi_schema

app.openapi = my_schema

@app.get(
    path ="/v1/polarity/unique/", 
    tags=["Obter Polaridade de uma  Frase"], 
    description="Entre com uma frase e descubra o sentimento por de trás dela.",
    responses={200: {"model": SucessResponse}, 422: {"model": ValidationErrorResponse}, 500: {"model": ServerErrorResponse}}
)
def unit_polarity(request: Request, sentence: str): 
    return get_unity(request, sentence, sia, condictions, describes)

from typing import List
from pydantic import BaseModel
from fastapi import FastAPI, Body
class GraphList(BaseModel):
    data: List[dict]
@app.post(
    path ="/v1/polarity/list/", 
    tags=["Obter Polaridade de uma lista de Frases"], 
    description="Entre com uma lista de frases e descubra o sentimento por de trás dela.",
    responses={200: {"model": SucessResponse}, 422: {"model": ValidationErrorResponse}, 500: {"model": ServerErrorResponse}}
)
def multi_polarity(request: Request, sentences: list[dict]): 
    return post_multi(request, sentences, sia, condictions, describes)

