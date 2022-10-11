import json
import pandas as pd
from fastapi import Request
from routes.unit_polarity import *


from fastapi.responses import JSONResponse


def __loop_searches(request: Request, sentences:list, sia, condictions, describes) -> list:
    """ ## obtem a polaridade para cada sentença
    @sentences: lista de sentenças;
    """
    # if "error" in list(response.keys()): return response

    result = []
    for s in sentences:
        response =  __check_body(s, {"event": "unit_polarity", "sucess": False}) 
        if 'error' not in response.keys():
            response = json.loads(get_unity(request, s['sentence'], sia, condictions, describes).body)

        result.append(response)

    return result

def __concat_sentences(sentences: list, results: list) -> list:
    """ 
    ## obtem a polaridade de todas sentenças juntas
    ### e retorna uma string concatenada
    @sentences: lista de sentenças;
    @results: lista de resultados da obtenção da polaridade das sentenças
    """

    df = pd.DataFrame(sentences).join(pd.DataFrame(results))
    conversation = ' '.join([s.sentence for i, s in df.iterrows() if s.sucess])
    return conversation

def __check_body(sentence: str, response: dict):

    if "sentence" not in sentence.keys(): 
        print(sentence.keys())
        response["error"] = "Parâmetro `sentence` não fornecido" 
    return response

def post_multi(request: Request, sentences: list, sia, condictions: list, describes: list):
    """ ## Consulta Multipla de Polaridade de Sentença """

    response = {"event": "multi_polarity", "sucess": False}

    try: 
        sentences_result = __loop_searches(request, sentences, sia, condictions, describes)
        
        if all([js['sucess'] is False for js in sentences_result]): 
            raise AttributeError("Nenhuma entrada válida!")

        sentence = __concat_sentences(sentences, sentences_result)
        result = get_unity(request, sentence, sia, condictions, describes, mult=True)

        response_body = json.loads(result.body)  
        response_body['event'] = "multi_polarity"  
        response_body['sentences'] = sentences_result  
        response_body = json.dumps(response_body)  

        result.body = str(response_body).encode()

        result.raw_headers[0] = (b'content-length', b'%d' %len(result.body))

        return result

    except KeyError as e:
        response["error"] = "Parâmetros Incorretos!" 
        return JSONResponse(status_code=422, content=response)

    except AttributeError as e: 
        response["error"] = str(e)
        return JSONResponse(status_code=406, content=response)

    except Exception as e: 
        response["error"] = str(e)
        return JSONResponse(status_code=500, content=response)
