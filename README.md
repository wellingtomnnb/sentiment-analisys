## nlp-api

API de Processamento de Linguagem Natural (NLP)

VERSÃO 1 -  Análise de Sentimentos utilizando léxicos

#### Folders

* `Dados` - Datasets e léxicos
* `Models` - Arquivos base para execução de tarefas;
* `Training` - Arquivos de Treinamentos (Regressão, Classificação, etc)

##### External Files
* `sentiment`: Testes de pré classificações;

#### Installations
Descomentar célula e executa-la, para efeturar as instalações
> ./models/installs.ipynb

#### API

Inicialização:

`python3 -m  uvicorn api:app --host [IP_ADDRESS] --port [PORT] --reload`

*Necessário estar na pasta raiz do projeto ao executar o comando acima.

chaves de retorno:
* `event`: *String* que representa o Nome do evento de obtenção da polaridade
* `sucess`: *Boleano* que indica se o processamento da sentença foi bem sucedido
* `polarity`: *Float* que indica a Polaridade da sentença ou da lista de sentenças
* `describe`: *String* com Descrição da polaridade numérica
* `sentences`: *List* com polaridades da lista de sentenças (apenas para multi polarity)
* `error`: *String* com mensagem de erro em caso de falha


##### Routes
* Testes: `host`:`porta`/tests
* Documentação: `host`:`porta`/docs

**Polarity Requests**

Obtem a polaridade da/das sentenças

* Unique Sentence: `/v1/polarity/unique/`

    curl request example:

    >curl -X 'GET' \
    'http://192.168.0.41:8560/v1/polarity/unique/?sentence=eu%20gosto%20de%20comer%20pao' \
    -H 'accept: application/json'

    return  (status code 200):
    
    ```
    {
        "event": "unit_polarity",
        "sucess": true,
        "polarity": 0.743,
        "describe": "positivo"
    }
    ```

* Multi Sentences: `/v1/polarity/list/`
    curl request example:
    
    >curl -X 'POST' \
    'http://192.168.0.41:8560/v1/polarity/list/' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '[
    {"sentence":"eu gosto de comer pao"},
    {"sentence":"the book on the table"},
    {"sentence":"odeio pensar que o terei que te ver mais uma vez"}
    ]'

    return  (status code 200):

    ```
    {
        "event": "multi_polarity",
        "sucess": true,
        "polarity": -0.5994,
        "describe": "negativo",
        "sentences": [
            {"event": "unit_polarity", "sucess": true, "polarity": 0.743, "describe": "positivo"},
            {"event": "unit_polarity", "sucess": true, "polarity": 0, "describe": "neutro"},
            {"event": "unit_polarity", "sucess": true, "polarity": -0.8807, "describe": "negativo"},
        ]
    } 
    ```


#### Implementações Futuras
* Remoção de logs de testes
* Testes Unitários para funções de pesquisa de polaridade
* Segmentação de Logs por rota/status
* Persistencia de logs em cloud
* Análise de similaridade de palavras
* Lematização de palavras