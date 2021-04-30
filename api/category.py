import requests
import pprint

VER = 'v2'
PROTOCOL = 'https'
DOMAIN = 'bling.com.br'


def getCategories(apikey):
    p = {
        'apikey': apikey
    }

    endpoint = f'{PROTOCOL}://{DOMAIN}/Api/{VER}/categorias/json/'
    r = requests.get(endpoint, params=p)
    print('get categories json (status: ' + str(r.status_code) + ')')

    if (r.status_code >= 200 and r.status_code < 300):
        return r
    else:
        print('ERROR - GET CATEGORY')
        print('status code: ' + str(r.status_code))
        pprint.pprint(r.json())
        return False

def postCategory(apikey, xml):
    p = {
        'apikey': apikey,
        'xml': xml
    }
    # https://bling.com.br/Api/v2/categoria/json/
    endpoint = f'{PROTOCOL}://{DOMAIN}/Api/{VER}/categoria/json/'
    r = requests.post(endpoint, params=p)
    print('post category json (status: ' + str(r.status_code) + ')')
    return r.json()

def putCategory(apikey, idCategory, xml):
    p = {
        'apikey': apikey,
        'xml': xml
    }

    endpoint = f'{PROTOCOL}://{DOMAIN}/Api/{VER}/categoria/{idCategory}/json/'
    r = requests.put(endpoint, params=p)
    print('put category json (status: ' + str(r.status_code) + ')')
    return r.json()
