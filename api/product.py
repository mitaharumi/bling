import requests
import pprint

VER = 'v2'
PROTOCOL = 'https'
DOMAIN = 'bling.com.br'

'''
https://ajuda.bling.com.br/hc/pt-br/articles/360046422714-GET-produtos
    GET/produtos
    curl -X GET "https://bling.com.br/Api/v2/produtos/json/"
         -G
         -d "apikey={apikey}" 
'''
def getProducts(apikey, page):  # get json
    p = {
        'apikey': apikey
    }
    if page < 1:
        endpoint = f'{PROTOCOL}://{DOMAIN}/Api/{VER}/produtos/json/'
    else:
        endpoint = f'{PROTOCOL}://{DOMAIN}/Api/{VER}/produtos/page={page}/json/'

    r = requests.get(endpoint, params=p)
    print('get products json (status: ' + str(r.status_code) + ')')
    if (r.status_code >= 200 and r.status_code <300):
        return r
    else:
        print('ERROR - GET PRODUCTS')
        print('status code: ' + str(r.status_code))
        pprint.pprint(r.json())
'''
https://ajuda.bling.com.br/hc/pt-br/articles/360046422734-GET-produto-codigo-
    GET /produto/{codigo}
    curl -X GET "https://bling.com.br/Api/v2/produto/{codigo}/json/"
         -G
         -d "apikey={apikey}"
'''
def getProduct(productCode, apikey):
    p = {
        'apikey': apikey
    }
    endpoint = f'{PROTOCOL}://{DOMAIN}/Api/{VER}/produto/{productCode}/json'
    r = requests.get(endpoint, params=p)
    print('get product json (status: '+ str(r.status_code) + ')')
    if (r.status_code >= 200 and r.status_code < 300):
        return r
    else:
        print('ERROR - GET PRODUCTS')
        print('status code: ' + str(r.status_code))
        pprint.pprint(r.json())
'''
https://ajuda.bling.com.br/hc/pt-br/articles/360046422774-POST-produto
    POST /produto
    curl -X POST "https://bling.com.br/Api/v2/produto/json/"
         -d "apikey={apikey}"
         -d "xml={xml_do_produto}" 
'''
# ##### not tested
# def postProduct(xmlPath):
#     p = {
#         'apikey': APIKEY,
#         'xml': xmlPath
#     }
#     endpoint = f'{PROTOCOL}://{DOMAIN}/Api/{VER}/produto/json/'
#     r = requests.post(endpoint, params=p)
#     print('status code: '+str(r.status_code))
#     print(r.json())

def productPriceBling(json):
    products = json['retorno']
    products = products['produtos']
    for productItem in products:
        product = productItem['produto']
        productPrice = product['preco']
        return productPrice

def productCode(json):
    products = json['retorno']
    products = products['produtos']
    for productItem in products:
        product = productItem['produto']
        productCode = product['codigo']
        return productCode

def productsCodes(apikey):
    codes = []
    page = 1
    close = False
    while not close:
        json = getProducts(apikey, page)
        print('\nget codes page: ' + str(page))
        try:
            jsonReturn = json.json()['retorno']
            products = jsonReturn['produtos']
        except:
            try:
                jsonReturn = json.json()['retorno']
                jsonErrors = jsonReturn['erros']
                for jsonError in jsonErrors:
                    error = jsonError['erro']
                    cod = error['cod']
                    if cod == 14:
                        close = True
            except:
                raise ValueError
        else:
            for productItem in products:
                product = productItem['produto']
                codes.append(product['codigo'])
            page += 1
    return codes
