import pandas as pd
import numpy as np
from models.dbConection import execQuery

import warnings
from pandas.core.common import SettingWithCopyWarning
warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)


from string import punctuation
from nltk import tokenize
import html
import re
import numpy as np

import nltk
import unidecode 

class Modeling:

    df_raw = pd.DataFrame()
    df_modeled = pd.DataFrame()

    def  __init__(self, df= -1, days: list = None, table = "log_atendimentos" ): 
        """
        ### Formata dados da tabela log_atendimentos
        Caso não seja informado um df, é necessário informar uma
        lista com a data inicial e final para busca de dados diretamente no banco
        @property `df_raw`: Dataframe com os dados não processados
        @property `df_modeled`: Dataframe com os dados processados
        @parameter `df`: Dataframe com os dados a serem processados
        @parameter `days`: Lista com a data inicial e final para a busca de dados no banco
        @parameter `table`: String com nome da tabela a ser pesquisada
        """
        if type(df) == pd.DataFrame: self.df_raw = df.copy()
        else: 
            if days != None: 
                if (type(days) != list) | (len(days) != 2):  raise Exception("Informe uma lista com a data inicial e final. Ex. ['2022-08-08 00:00:00', '2022-08-08 23:59:59']")
                print("Buscando Dados...")
                self.df_raw = execQuery(f"SELECT * FROM {table} WHERE data_criado BETWEEN '{days[0]}' AND '{days[1]}'")
            else: raise Exception("Informe um conjunto de dados ou um período para consulta")


    # Formatações de dados
    def format_cols(self, df):
        """Formatações de dados"""

        # log_reply
        print("format_cols(log_reply)")
        df["log_reply"].fillna(0, inplace=True)
        df["reply"] = df["log_reply"].apply(int)

        # remoção de msgs do bot
        print("format_cols(bot_remove)")
        df = df.query("contato_id.notnull() | operador_id.notnull()")

        # remetentes
        print("format_cols(from_me)")
        df['from_me'] = np.where(df["contato_id"].isnull(), 1, 0)

        # formatando datas
        # print("format_cols(format_dates)")
        # df = self.format_dates(df)

        # removendo msgs vazias
        print("format_cols(log_texto)")
        df = df[df["log_texto"].notnull()]

        return df

    # Formatações de datas
    def format_dates(self, df):
        """Formatações de dados"""

        print("format_dates(set_type)")
        df.data_criado = df.data_criado.apply(pd.to_datetime)

        # month
        print("format_dates(get_month)")
        df['month'] = df.data_criado.dt.month

        # dayofweek: {0: segunda ~ 6: domingo}
        print("format_dates(get_dayofweek)")
        df['dayofweek'] = df.data_criado.dt.dayofweek

        # periods: {0: madrugada ~ 3: noite}
        print("format_dates(set_periods)")
        condictions = [df.data_criado.dt.hour.isin(range(0, 6)),
                    df.data_criado.dt.hour.isin(range(6, 12)),
                    df.data_criado.dt.hour.isin(range(12, 18)),
                    df.data_criado.dt.hour.isin(range(18, 24))]
        df['period'] = np.select(condictions, [0, 1, 2, 3])
        
        return df

    # remoção de cols desnecessárias
    def drop_cols(self, df):
        """remoção de cols desnecessárias"""

        colunas_pra_remover = ['log_id', 'log_msid', 'log_imagem', 'log_video', 'log_audio', 'log_localizacao', 'log_latitude', 'log_longitude', 
            'log_contato_nome', 'log_contato_numero', 'log_arquivo', 'enviado', 'recebido', 'lido', 'geo_lon',  'log_keyID', 'data_enviado', 
            'data_recebido_cliente', "data_recebido_servidor", "data_lido_operador", "data_criado", "operador_id", "contato_id", "log_reply"]

        return df.drop(columns= colunas_pra_remover, axis=1)

    # get_emojis
    def get_emojis(self, df, column="log_texto"):
        """ obtem emojis"""
        print(f"get_emojis(df) | len(df): {len(df)}")

        reg_caracters='\-|\!|\"|\#|\$|\%|\&|\|\'|\(|\)|\*|\+|\,|\.|\/|\n|\:|\;|\<|\=|\>|\?|\@|\[|\\|\]|\^|\_|\`|\{\|\}|\~|[0-9]*'

        token_space = tokenize.WhitespaceTokenizer()

        processed_emojis = list()

        for msg in df[column]:

            emojis = list()

            words = token_space.tokenize(msg)

            for word in words: 

                # identifica emojis e armazena-os
                if word != html.unescape(word): 
                    # regex p/ letras minus., maiusc, acentuadas e espaço
                    reg = "|[a-zA-ZÀ-ú\s]" 
                    # remove caracteres especiais proximos ao emoji
                    emoji = re.sub(reg_caracters+reg, '', html.unescape(word)) 
                    # add emoji à lista
                    emojis.append(emoji)
            
            if len(emojis) > 0: processed_emojis.append(''.join(emoji for emoji in emojis))
            else: processed_emojis.append(np.nan)

        return processed_emojis
    
    # Remove Palavras irrelevantes (stopwords)
    def remove_stopwords(self, df, column="log_texto"):
        """ remove Palavras irrelevantes (stopwords) e insere o resultado na coluna `process1`"""
        print("remove_stopwords(df) | len(df): %d" %len(df))

        reg_caracters='\!|\"|\#|\$|\%|\&|\|\'|\(|\)|\*|\+|\,|\.|\/|\n|\:|\;|\<|\=|\>|\?|\@|\[|\\|\]|\^|\_|\`|\{\|\}|\~|[0-9]*'

        df = df.copy()
        
        # transforma string de pontos em uma lista
        pontos, pontos[:0] =  [], punctuation 

        # stopwords - palavras indesejadas
        stopwords = list()
        try: stopwords = nltk.corpus.stopwords.words("portuguese")
        except: 
            nltk.download('stopwords')
            stopwords = nltk.corpus.stopwords.words("portuguese")

        saudacoes = ['oi', 'ola', 'opa', 'oie', 'oii', 'oiee', 'oin', 'só', 'so']
        stopwords += saudacoes
        stopwords += pontos

        # tokenize
        token_space = tokenize.WhitespaceTokenizer()

        # deixa todas palavras em minusculo
        df[column] = df[column].str.lower()

        processed_msgs = list()
        qtd_words = list() # quantidade de palavras em uma frase

        df = df.reset_index()

        for i, msg in enumerate(df[column]):

            if pd.isna(df.loc[i][column]): continue

            new_word = list()
            msg = msg.replace('\n\n', ' ').replace('\n', ' ')
            msg = re.sub(r'http\S+', '', msg) # remove link da msg
            msg = html.unescape(msg) # descodifica 
            msg = unidecode.unidecode(msg) # remove acentos/emojis das palavras
            msg = re.sub(reg_caracters, "", msg) # remove caracteres especiais dentro das palavras

            words = token_space.tokenize(msg)

            for i, word in enumerate(words): 

                try:
                    if (word in ['bom', 'boa']) and (words[i+1] in ['dia', 'tarde', 'noite']): continue
                    elif (word in ['dia', 'tarde', 'noite']) and (words[i-1] in ['bom', 'boa']): continue
                except: pass

                if (word not in stopwords) & (len(word)>0): new_word.append(word)

            if len(new_word)>0: processed_msgs.append(' '.join(txt for txt in new_word)) 
            else: processed_msgs.append(np.nan)
            
            qtd_words.append(len(new_word))

        return processed_msgs, qtd_words

    # transform_text_stemmer
    def transform_text_stemmer(self, df, column="text"):
        """ obtem palavras stemmizadas """
        print(f"transform_text_stemmer(df) | len(df): {len(df)}")

        token_space = tokenize.WhitespaceTokenizer()
        stemmer = nltk.RSLPStemmer()

        stemmed_words = list()

        for msg in df[column]:

            words = token_space.tokenize(msg)
            new_word = [stemmer.stem(word) for word in words]
            stemmed_words.append(' '.join(text for text in new_word))

        return stemmed_words

    # get_text_polarity
    def get_text_polarity(self, dictionary, column="text"):
        """ remove Palavras irrelevantes (stopwords) e insere o resultado na coluna `process1`"""

        df = self.df_modeled.copy()

        print("get_text_polarity(df) | len(df): %d" %len(df))

        # tokenize
        token_space = tokenize.WhitespaceTokenizer()

        # stem/truncar: redução de palavras (ex: corredor, corrida, corredores > corr)
        stemmer = None
        try: stemmer = nltk.RSLPStemmer()
        except: 
            nltk.download('rslp')
            stemmer = nltk.RSLPStemmer()

        # deixa todas palavras em minusculo
        df[column] = df[column].str.lower()

        # transforma df dictionary em dict
        dic = dictionary.set_index("term").to_dict()["polarity_value"]

        processed_polaritys = list()

        # Conjunções adversativas exprimem a ideia de oposição
        conj_adv = ['mas', 'porem', 'contudo', 'entretanto', 'entanto', 'todavia', 'não', 'obstante', 'nao', 'n', 'nem']
        peso = 1

        for msg in df[column]:

            pesos = list()

            words = token_space.tokenize(msg)

            for word in words: 
                                
                try: pesos.append(dic[word] * peso) # verifica a palavra completa no dicionario
                except: 
                    try: pesos.append(dic[word] * peso) # verifica a palavra completa no dicionario stemmado
                    except: 
                        try: pesos.append(dic[stemmer.stem(word)] * peso) # verifica a palavra stemmada no dicionario stemmado
                        except: pesos.append(np.nan) # se não existir a palavra em nenhuma forma add null

                if word in conj_adv: peso = -1
            

            if len(pesos)>0: processed_polaritys.append(pesos)
            else: processed_polaritys.append(np.nan)

        df['polaritys'] = processed_polaritys
        self.df_modeled = df
        
        return df

    def run(self):
        print("Tratando Dados...")
        df = self.format_cols(self.df_raw)
        df = self.drop_cols(df)
        df['emojis'] = self.get_emojis(df)
        result = self.remove_stopwords(df)
        df['text'] = result[0]
        df['qtd_words'] = result[1]
        df = df[(df['text'].notnull()) & (df['qtd_words'] <= 120)]
        df['stemmed_text'] = self.transform_text_stemmer(df)
        self.df_modeled = df
        return self
