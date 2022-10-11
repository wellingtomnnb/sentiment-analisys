import grequests
import requests
import json

class PolarityRequestTests():
    """
    ### PolarityRequestTest
    Testes de requisição de list e unique
    """

    def __init__(self, ip_host: str = "192.168.0.41", port_host: int = 8560) -> None:
        self.ip_host = ip_host
        self.port_host = port_host
        self.headers = {'Content-type': 'application/json'}
    

    def __list_all_wrong_keys_test_negative(self, url):
        """ 
        ## __list_all_wrong_keys_test_negative
        Teste negativo - chaves inválidas

        """
        # MODELS
        all_invalid_keys= [
                {"wrong_key1": "Me orientaram a entrar em contato com vocês."},
                {"wrong_key2": "Adorei o atendimento daquele rapazinho"},
                {"wrong_key3": "Na verdade vou fazer o cancelamento do meu plano"},
        ]

        # REQUEST
        body = str(all_invalid_keys).replace("'", '"').encode()
        result = None
        try: result = requests.post(url , body, headers=self.headers, timeout=3)
        except Exception as e: raise AssertionError(f"High Wait Time: {e}")

        # TESTS
        ## test content
        content = {}
        try: content = json.loads(result.content)
        except Exception as e: raise AssertionError("Failed to load the content: %s" %e) 

        ## test status code
        assert result.status_code == 406, f"The request did not fail where it should have failed. Expected status code 406 but got {result.status_code}"

        ## test event name
        assert content['event'] == 'multi_polarity', f"Expected event ´multi_polarity´ but got {content['event']}"
        
        ## test content keys
        all_keys_is_valid = all([k in json.loads(result.content).keys() for k in ['event', 'sucess', 'error']])
        assert all_keys_is_valid, "Not all return keys are valids"

    def __list_any_wrong_key_test_negative(self, url):
        """ 
        ## __list_any_wrong_key_test_negative
        Teste negativo - algum valor inválido dentre valores válidos
        """

        # MODELS
        all_invalid_keys= [
                {"wrong_key1": "Me orientaram a entrar em contato com vocês."},
                {"wrong_key2": "Adorei o atendimento daquele rapazinho"},
                {"sentence": "Na verdade vou fazer o cancelamento do meu plano"},
        ]

        # REQUEST
        body = str(all_invalid_keys).replace("'", '"').encode()
        result = None
        try: result = requests.post(url , body, headers=self.headers, timeout=3)
        except Exception as e: raise AssertionError(f"High Wait Time: {e}")

        # TESTS
        ## test content
        content = {}
        try: content = json.loads(result.content)
        except Exception as e: raise AssertionError("Failed to load the content: %s" %e) 

        ## test status code
        assert result.status_code == 200, f"Undue Failure. Expected status code 200 but got {result.status_code}"

        ## test event name
        assert content['event'] == 'multi_polarity', f"Expected event ´multi_polarity´ but got {content['event']}"
        
        ## test content keys
        all_keys_is_valid = all([k in content.keys() for k in ['event', 'sucess', 'polarity', 'sentences']])
        assert all_keys_is_valid, "Not all return keys are valid"

        ## test len(sentences)
        assert len(content['sentences']) == 3, "Incorrect number of sentence returns"

        ## test individual state 
        any_sucess = any([i['sucess'] for i in content['sentences']])
        any_failed = any([i['sucess'] == False for i in content['sentences']])
        assert all([any_sucess, any_failed]), "Not all results must be sucess or failed" 

    def __list_test_negative(self, url) -> None:
        """ 
        ## __list_test_negative
        Teste negativo - entradas inválidas
        """

        #TESTS

        ## Test wrong body format
        possibles_invalids_inputs = [str(["string list"]).replace("'", '"').encode(), "string", "123456", None, '']
        for body in possibles_invalids_inputs:
            result = requests.post(url , body, headers=self.headers)
            
            assert result.status_code == 422, f"The request did not fail where it should have failed. Expected status code 422 but got {result.status_code}"


        ## Others tests
        self.__list_all_wrong_keys_test_negative(url)
        self.__list_any_wrong_key_test_negative(url)

        print(" * Negative List Test Sucess *")

    def __list_test_positive(self, url) -> None:
        """ 
        ## __list_test_positive
        Execute a chamada de API com parâmetros obrigatórios válidos
        """

        # MODEL
        multi_valid_sentences= [
            {"sentence": "Me orientaram a entrar em contato com vocês."},
            {"sentence": "Adorei o atendimento daquele rapazinho"},
            {"sentence": "Na verdade vou fazer o cancelamento do meu plano"},
        ] 

        # REQUEST
        body = str(multi_valid_sentences).replace("'", '"').encode()
        result = None
        try: result = requests.post(url , body, headers=self.headers, timeout=3)
        except Exception as e: raise AssertionError(f"High Wait Time: {e}")


        # TESTS
        ## test content
        content = {}
        try: content = json.loads(result.content)
        except Exception as e: raise AssertionError("Failed to load the content: %s" %e) 

        ## test status code
        assert result.status_code == 200, f"Undue Failure. Expected status code 200 but got {result.status_code}"

        ## test event name
        assert content['event'] == 'multi_polarity', f"Expected event ´multi_polarity´ but got {content['event']}"

        ## test content keys
        all_keys_is_valid = all([k in content.keys() for k in ['event', 'sucess', 'polarity', 'sentences']])
        assert all_keys_is_valid, "All return keys should be valid"

        ## test individual state 
        assert all([i['sucess'] for i in content['sentences']]), "All results should be true"

        print(" * Positive List Test Sucess *")

    def list_test(self, route: str = "v1/polarity/list"): 
        """
        ### list_test
        Testes de requisições de lista de sentenças
        """

        url = f'http://{self.ip_host}:{self.port_host}/{route if route[0] != "/" else route[1:]}'
        
        self.__list_test_positive(url)
        self.__list_test_negative(url)

    def __unique_test_negative(self, url):

        sentences = [None, '', 123, '123']

        # REQUEST
        results = None
        try: results = [requests.get(url + f'/?sentence={sentence}', timeout=3) for sentence in sentences]
        except Exception as e: raise AssertionError(f"High Wait Time: {e}")


        #  TESTS
        ## test status code & content
        contents = []
        for res in results:
            assert res.status_code == 400, f"Undue Failure. Expected status code 400 but got {res.status_code}"
            try: contents.append(json.loads(res.content))
            except Exception as e: raise AssertionError("Failed to load the content: %s" %e) 

        ## test event name
        for content in contents:
            assert content['event'] == 'unit_polarity', f"Expected event ´unit_polarity´ but got {content['event']}"

        ## test content keys
        for content in contents:
            all_keys_is_valid = all([k in content.keys() for k in ['event', 'sucess', 'error']])
            assert all_keys_is_valid, "All return keys should be valid"

        ## test state 
        for content in contents:
            assert content['sucess'] == False, "The return of the state should be true"

        print(" * Negative Unique Test Sucess *")
        
    def __unique_test_positive(self, url):
        """
        ### unique_test
        Testes de requisições de sentenças individuais
        """

        sentence = "Adorei o atendimento daquele rapazinho"

        # REQUEST
        result = None
        try: result = requests.get(url + f'/?sentence={sentence}', timeout=3)
        except Exception as e: raise AssertionError(f"High Wait Time: {e}")

        #  TESTS
        # test content
        content = {}
        try: content = json.loads(result.content)
        except Exception as e: raise AssertionError("Failed to load the content: %s" %e) 

        ## test status code
        assert result.status_code == 200, f"Undue Failure. Expected status code 200 but got {result.status_code}"

        ## test event name
        assert content['event'] == 'unit_polarity', f"Expected event ´unit_polarity´ but got {content['event']}"
    
        ## test content keys
        all_keys_is_valid = all([k in content.keys() for k in ['event', 'sucess', 'polarity', 'describe']])
        assert all_keys_is_valid, "All return keys should be valid"

        ## test state 
        assert content['sucess'], "The return of the state should be true"

        print(" * Positive Unique Test Sucess *")

    def unique_test(self, route: str = "v1/polarity/unique"):
        """
        ### unique_test
        Testes de requisições de sentenças individuais
        """

        url = f'http://{self.ip_host}:{self.port_host}/{route if route[0] != "/" else route[1:]}'

        self.__unique_test_positive(url)
        self.__unique_test_negative(url)

    def __list_overload_test(self, url):
        """
        ## overload_test
        Execução de testes multiplas vezes de forma assincrona,
        na rota de lista de sentenças
        """

        # MODEL
        multi_valid_sentences= [
            {"sentence": "Me orientaram a entrar em contato com vocês."},
            {"sentence": "Adorei o atendimento daquele rapazinho"},
            {"sentence": "Na verdade vou fazer o cancelamento do meu plano"},
        ] 

        multi_invalid_sentences= [
            {"sentence": "11111111111111"},
            {"sentence": "None"},
            {"sentence": ""},
        ] 

        multi_invalid_keys= [
            {"wrog_key1": "Me orientaram a entrar em contato com vocês."},
            {"wrog_key2": "Adorei o atendimento daquele rapazinho"},
            {"wrog_key3": "Na verdade vou fazer o cancelamento do meu plano"},
        ] 


        for i, body in enumerate([multi_valid_sentences, multi_invalid_sentences, multi_invalid_keys]):
            body = str(body).replace("'", '"').encode()
 
            rs = (grequests.post(link, data=body, headers=self.headers, timeout=3) for link in [url]*1500) 
            results = grequests.map(rs)

            assert not any([r is None for r in results]), "Some request failed"

            if i == 0: assert all([r.status_code == 200 for r in results]), "All state codes should be 200"
            if i in [1,2]: assert all([400 <= r.status_code <= 406 for r in results]), "All state codes should be between 400~499"

    def __unique_overload_test(self, url):
        """
        ## overload_test
        Execução de testes multiplas vezes de forma assincrona,
        na rota de sentença unica
        """
        # Sentences
        valids_sentences= [
            "1 Me orientaram a entrar em contato com vocês.",
            "2 Adorei o atendimento daquele rapazinho",
            "3 Na verdade vou fazer o cancelamento do meu plano"
        ]
        invalids_sentences = ["4", '', 'None']

        # URLs
        valids_urls = [f'{url}/?sentence={s}' for s in valids_sentences] * 1500
        invalids_urls = [f'{url}/?sentence={s}' for s in invalids_sentences] * 1500

        # Asynchronous Requests
        rs_valids = (grequests.get(u, timeout=3) for u in valids_urls)
        rs_invalids = (grequests.get(u, timeout=3) for u in invalids_urls)

        # Tests
        assert not any([r is None for r in rs_valids]), "Some request failed in valids requests"
        assert not any([r is None for r in rs_invalids]), "Some request failed in invalids requests"
        assert all([result.status_code == 200 for result in grequests.map(rs_valids)]), "Incorrect Results. Some `status_code` is different from 200"
        assert all([result.status_code == 400 for result in grequests.map(rs_invalids)]), "Incorrect Results. Some `status_code` is different from 400"

    def overload_test(self, route_uniq: str = "v1/polarity/unique", route_list= "v1/polarity/list"):
        
        url_uniq = f'http://{self.ip_host}:{self.port_host}/{route_uniq if route_uniq[0] != "/" else route_uniq[1:]}'
        url_list = f'http://{self.ip_host}:{self.port_host}/{route_list if route_list[0] != "/" else route_list[1:]}'

        self.__unique_overload_test(url_uniq)
        print(" * Unique Overload Test Sucess *")
        self.__list_overload_test(url_list)
        print(" * List Overload Test Sucess *")
        
PolarityRequestTests().list_test()
PolarityRequestTests().unique_test()
# PolarityRequestTests().overload_test()
        