import pprint
import requests

VER = 'v2'
PROTOCOL = 'https'
DOMAIN = 'bling.com.br'

'''
https://ajuda.bling.com.br/hc/pt-br/articles/360047062813-POST-produtoLoja-idLoja-codigo-
    POST /produtoLoja/{idLoja}/{codigo}
    curl -X POST "https://bling.com.br/Api/v2/produtoLoja/{idLoja}/{codigo}/json/"
         -d "apikey={apikey}"
         -d "xml={xml_do_produto_loja}" 
error message:
- 121	O campo idLojavirtual é obrigatório
- 122	O campo Preco é obrigatório
- 123	O produto com este código não foi encontrado no sistema
- 124	A loja com este Id não foi encontrada no sistema
'''
def postMarket(productCode, marketCode, xml, apikey):
    p = {
        'apikey': apikey,
        'xml': xml
    }
    endpoint = f'{PROTOCOL}://{DOMAIN}/Api/{VER}/produtoLoja/{marketCode}/{productCode}/json/'
    print(endpoint)
    r = requests.post(endpoint, params=p)
    print('post market (status: ' + str(r.status_code) + ')')
    if (r.status_code >= 200 and r.status_code < 300):
        return r
    else:
        print('ERROR - GET MARKET')
        print('status code: ' + str(r.status_code))
        pprint.pprint(r.json())
        return False
'''
https://ajuda.bling.com.br/hc/pt-br/articles/360046422594-PUT-produtoLoja-idLoja-codigo-
    PUT /produtoLoja/{idLoja}/{codigo}
    curl -X PUT "https://bling.com.br/Api/v2/produtoLoja/{idLoja}/{codigo}/json/"
         -d "apikey={apikey}"
         -d "xml={xml_do_produto_loja}"
error message:
- 121	O campo idLojavirtual é obrigatório
- 122	O campo Preco é obrigatório
- 123	O produto com este código não foi encontrado no sistema
- 124	A loja com este Id não foi encontrada no sistema
'''
def putMarket(productCode, marketCode, xml, apikey):
    p = {
        'apikey': apikey,
        'xml': xml
    }
    endpoint = f'{PROTOCOL}://{DOMAIN}/Api/{VER}/produtoLoja/{marketCode}/{productCode}/json/'
    print(endpoint)
    r = requests.put(endpoint, params=p)
    print('put market (status: '+str(r.status_code)+')')
    if (r.status_code >= 200 and r.status_code < 300):
        return r
    else:
        print('ERROR - GET MARKET')
        print('status code: ' + str(r.status_code))
        pprint.pprint(r.json())
        return False

def getMarket(productCode, marketCodeBling, apikey):
    p = {
        'apikey': apikey,
        'loja': marketCodeBling
    }
    endpoint = f'{PROTOCOL}://{DOMAIN}/Api/{VER}/produto/{productCode}/json/'
    r = requests.get(endpoint, params=p)
    return r
    # if (r.status_code >= 200 and r.status_code < 300):
    #     return r
    # else:
    #     print('ERROR - GET MARKET')
    #     print('status code: ' + str(r.status_code))
    #     pprint.pprint(r.json())
    #     return False

# return idprodutoloja type: str
# if has already export:
# it has element: produtoLoja
# if not:
# does not show this field in xml
## so id ' 0'
# return string market code
