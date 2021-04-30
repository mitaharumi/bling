from datetime import datetime
import pandas as pd
import pprint

from access.access import backupCodesLinkMarketPath
from adhibition.sheet import worksheetRecords, insertValue, findByName
from adhibition.suport.xmlProductMarket import xmlProductMarket
from api.market import getMarket, postMarket
from api.product import productsCodes


# columns from sheets
COLMARKETNAME = 'Nome\nMarket'
COLMARKETCODE = 'Codigo\nMarket'
COLPRICETYPEGET = 'Preço Vinculado\n+ Ajuste'
COLPRICEVALUE = 'Ajuste Preço\n(valor)'
COLPRICESALEVALUE = 'Ajuste Preço\nPromocional\n(valor)'
COLPRICEPERCENTAGE = 'Ajuste Preço\n(porcentagem)'
COLPRICESALEPERCENTAGE = 'Ajuste Preço\nPromocional\n(porcentagem)'
COLPRICEDATA = 'Ultimo Ajuste\nPreço'
COLPRICENUM = 'Quantidade de\nPreços Produtos\nAlterados por Ultimo'
COLLINK = 'Vincular\nTodos\nProdutos\nna Loja'
COLLINKDATA = 'Ultima Vinculação'
COLLINKNUM = 'Quantidade de\nNovos Produtos\nVinculados por Ultimo'

# standard: first link the price will be price in bling
def linkMarkets (sheet, indexCustomerPage, customerName, apikey):
    indexCOLLINK = findByName(sheet, indexCustomerPage, COLLINK)[1]
    indexCOLLINKDATA = findByName(sheet, indexCustomerPage, COLLINKDATA)[1]
    indexCOLLINKNUM = findByName(sheet, indexCustomerPage, COLLINKNUM)[1]
    records = worksheetRecords(sheet, indexCustomerPage)
    records = pd.DataFrame(records)
    codes = productsCodes(apikey)
    print('codes: ' + str(codes))
    codesLog = []

    for indexRow, row in records.iterrows():
        amount = 0
        if row[COLLINK] == 'TRUE':
            for productCode in codes:
                try:
                   products = getMarket(productCode, row[COLMARKETCODE], apikey).json()['retorno']
                except:
                    print('ERROR GET MARKET')
                else:
                    products = products['produtos']
                    for productItem in products:
                        product = productItem['produto']
                        productDescription = product['descricao']
                    try:
                        productMarket = product['produtoLoja']
                    except:
                        # link market
                        productPrice = product['preco']
                        xml = xmlProductMarket('0', productPrice, None)
                        response = postMarket(productCode, row[COLMARKETCODE], xml, apikey)
                        if response:
                            try:
                                responseReturn = response.json()['retorno']
                            except:
                                pass
                            else:
                                print('SUCCESS! product ' + str(productCode) + ' link market ' + str(row[COLMARKETCODE]))
                                codesLog.append(productCode)
                                amount += 1
                        else:
                            print('ERROR - POST MARKET PRODUCTS')
                            print('status code: ' + str(response.status_code))
                            pprint.pprint(response.json())
                    else:
                        print('product ' + str(productCode) +' already linked in market ' + str(row[COLMARKETCODE]))

            # update even if request is not successful
            insertValue(sheet, indexCustomerPage, indexRow + 2, indexCOLLINK, False)
            insertValue(sheet, indexCustomerPage, indexRow + 2, indexCOLLINKDATA, datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
            insertValue(sheet, indexCustomerPage, indexRow + 2, indexCOLLINKNUM, str(amount))
    codesPath = backupCodesLinkMarketPath() + customerName + datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
    pd.DataFrame(codesLog).to_csv(codesPath + '.csv', index=False)