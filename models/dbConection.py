import pandas as pd

from sqlalchemy import create_engine, exc # handle error

# Abre conexão com o Banco de Dados
def openConectionBD():
    #numero maximo de conexiones permanates.
    pool_size = 16

    # Temporarily exceeds the set pool_size if no connections are available.
    max_overflow = -1

    # Duração da conexão 
    pool_recycle = 1800  # 1800 = 30 minutes

    # Tempo limite de conexão 
    pool_timeout = 120,  # 120 seconds

    # conexao ao banco
    try:
        sqlEngine = create_engine("mysql+pymysql://{user}:{pw}@{server}/{db}".format(user='dbviewer',  
                                                                                     pw='BhegPuXW2b7DpLd3', 
                                                                                     server='192.168.0.140:3307', 
                                                                                     db='sac'),
                                                                                     pool_size=pool_size,
                                                                                     max_overflow=max_overflow,
                                                                                     pool_recycle=pool_recycle)


        # Check if anything at all is returned
        if sqlEngine:
            sqlEngine.execute("set session wait_timeout = {};".format(pool_recycle*pool_size))
            print('Conectando ao bd...')
            dbConnection = sqlEngine.connect()
            return dbConnection
        else:
            print('erro de connexion ao bd...') 
            return False
        
    except exc.SQLAlchemyError as e:
        print("-- ERROR IN CONNECTION --")
        print(type(e))
        error = str(e.__dict__['orig'])
        print(error)
        return False

#Busca no Banco de Dados
def execQuery(query):
# define quantidade máxima de linhas por arquivo
    chunk_size = 100000

    #Conexão com o BD
    dbConnection = openConectionBD()

    if type(dbConnection) != bool:
        print('Conexão com BD Estabelecida!')
        ## run query into mysql
        print('Consultando ...')
        try:
            i=0
            dfl = []
            # create empty datafarame
            dfs = pd.DataFrame()

            for chunk_dataframe in pd.read_sql(query, dbConnection, chunksize=chunk_size):
                i=i+1
                print(f"Got dataframe w/{len(chunk_dataframe)} rows")
                dfl.append(chunk_dataframe)

            # Start appending data from list to dataframe
            if len(dfl) > 0:
                dfs = pd.concat(dfl, ignore_index=True)
            else:
                print('Não se encontaram dados para as datas inseridas!')
            dbConnection.close()
            return dfs

        except exc.SQLAlchemyError as e:
            print("-- ERROR IN CONNECTION --")
            print(type(e))
            error = str(e.__dict__)
            print(error)
            print('Não foi possível concluir a consulta')
            return False

        # close conection
        dbConnection.close()
    else : 
        print('Não foi possível obter uma conexão com o Banco')
        return False