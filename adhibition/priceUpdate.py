from datetime import datetime
import pandas as pd
import pprint

from access.access import backupPriceUpdatePath, backupCodesUpdatePricePath, emailTriboUpdatePrice, senderMail, senderPass
from adhibition.sheet import worksheetRecords, insertValue, findByName, emailCustomer, inputRow
from adhibition.suport.xmlProductMarket import xmlProductMarket
from adhibition.suport.dataProcessing import formatAdjustmentPrice
from adhibition.reportsEmail import priceUpdateEmail
from api.market import getMarket, putMarket

from adhibition.suport.delay import delayS, delayM, delayL

# columns from sheets
COLMARKETNAME = 'Nome\nMarket'
COLMARKETCODE = 'Codigo\nMarket'
COLRELATIONPRICE = 'Relação Preço'
COLTYPEADJUSTMENT = 'Tipo Ajuste'
COLFORMAT = 'Formato'
COLPRICE = 'Ajuste Preço'
COLPRICESALE = 'Ajuste Preço\nPromocional'
COLPRICEDATA = 'Ultimo Ajuste\nPreço'
COLPRICENUM = 'Quantidade de\nPreços Produtos\nAlterados por Ultimo'
COLACTION = 'Ação de ajuste'
COLLINK = 'Vincular\nTodos\nProdutos\nna Loja'
COLLINKDATA = 'Ultima Vinculação'
COLLINKNUM = 'Quantidade de\nNovos Produtos\nVinculados por Ultimo'
CODEB2W = [203366666]  # [203332897, 203158617]
CODEMERCADOLIVRE = [203462220]  # [203422130, 203137948]

def marketRules(marketCode, priceOriginal):
    price = float(priceOriginal)
    if marketCode in CODEMERCADOLIVRE:
        print('apply MERCADO LIVRE rule')
        if price <= 73.99:
            price += 5
        elif price > 73.99:
            price += 25
    elif marketCode in CODEB2W:
        print('apply B2W rule')
        if price <= 93.99:
            price += 5
        elif price > 93.99:
            price += 25
    return round(price, 2)

def priceUpdate(sheet, apikey, indexCustomerPage, indexCustomerAccess, customerName):
    print('price update')
    print('set index columns')
    indexCOLRELATIONPRICE = findByName(sheet, indexCustomerPage, COLRELATIONPRICE)[1]
    indexCOLTYPEADJUSTMENT = findByName(sheet, indexCustomerPage, COLTYPEADJUSTMENT)[1]
    indexCOLFORMAT = findByName(sheet, indexCustomerPage, COLFORMAT)[1]
    delayL()
    indexCOLPRICE = findByName(sheet, indexCustomerPage, COLPRICE)[1]
    indexCOLPRICESALE = findByName(sheet, indexCustomerPage, COLPRICESALE)[1]
    delayL()
    indexCOLACTION = findByName(sheet, indexCustomerPage, COLACTION)[1]
    indexCOLPRICEDATA = findByName(sheet, indexCustomerPage, COLPRICEDATA)[1]
    indexCOLPRICENUM = findByName(sheet, indexCustomerPage, COLPRICENUM)[1]

    delayL()
    records = worksheetRecords(sheet, indexCustomerPage)
    # codes = productsCodes(apikey)
    # print('all product codes: ')
    # print(codes)
    # codesPath = backupCodesUpdatePricePath() + 'geralCodes' + customerName + datetime.now().strftime("%d-%m-%Y")
    # pd.DataFrame(codes).to_csv(codesPath + '.csv', index=False)

    # codes = ['5Z5RN5FZD', 'KRHSRQQGP', 'MGB49X4SVPBK', 'MGBVX2ZKWS2J', 'MGBB7X555GNC', 'MGBEVY5SZDY6', 'MGB7599A69W8-7753HTDE6', 'MGB5L4CVRL7U', 'MGBTUVB7FLH9', 'MGBQNGWAN7DE', 'MGBV7EQF5BRA', 'MGBMYSJQK5C2', 'MGB2XJ94TRDY', 'MGB5RCJTUVNX', 'MGBSXL7R2R55', 'MGB725QS6E38', 'MGBQK44QV6AS', 'MGB46WEF5LPL-P89ZRGHOC', 'MGBKVJHYG29F-0U79PSSDK', 'MGBEEPQ5GD3J', 'MGBBLUS30805L', 'MGB6GTYPTPW8-MD0N9CPR4', 'MGBNFYTUSSJP', 'MGBCH3MAN3ZM', 'MGBEZD6REYXD', 'MGB3JKMJ7QT4', 'MGBF7W5GG5Q6', 'MGBN7SUQF7CY', 'MGBJ3HW2BRJ3', 'MGBJ3HW2BRJ3-Z1S61A7DU', 'MGBDFCRSWCN6', 'MGBJPV3Y3R3T', 'MGBKD6WHV9KX', 'MGBGY7DRVRWJ', 'MGBCCJ765GH5', 'MGBJT5XHV6RJ', 'MGBWKKX2NDYV', 'MGBDDXRTE229', 'MGBDDXRTE229-1NQ5Z077E', 'MGB575PWJPWA', 'MGBR8SEB42ZS', 'MGBNUSC5US49', 'MGBJV6HS2FNG', 'MGBWAGKLQFA4', 'MGBN6QQ6MK35', 'MGB9MXZE8RXW', 'MGB5XA73BRQ2', 'MGBSBSDNLD65', 'MGB28SEB5PN3', 'MGB3CBD2759R', 'MGBTK2QUEXV5', 'MGBZYEMVTCPA', 'MGBFBASFRD2U', 'MGBN34DYFA4Z', 'MGBZ7X39JSSR', 'MGBNH2NMW864', 'MGB3JKMJ7QT4-2YKHAORLD', 'MGB6QPZMQMHT', 'MGB3LL29USPW', 'MGBPCLPZGQ2Q', 'MGB32R65KTJR', 'MGB7ZL4TY7YE', 'MGB866PQU9MX', 'MGBFG6GXYL57', 'MGBP64TC4TLU', 'MGBHC9EC48NX', 'MGBDUCFVBQSG', 'MGB2FH63BS7Y', 'MGBCRK6MXVZ2', 'MGBA9QQMCHUM', 'MGB25X776E4F', 'MGBSF5X89YAR', 'MGBCEL3DE6UR', 'MGB3YPXRQTX6', 'MGB2UR84PJZQ', 'MGBHMMTXL7C5', 'MGB57UCG9GW3', 'MGBZN5AJPN22', 'MGBSHW52WJD6', 'MGB7J33KMFJS', 'MGBLLDNMFLTG', 'MGBWDMZFZBCX', 'MGBQFVLJBMHU', 'MGB6GTYPTPW8', 'MGBJ57J72SZL', 'MGBYAC9KBKXZ', 'MGBRLY25BJZY', 'MGBJHB4H8EEB', 'MGBND8L52ZM7', 'MGBGWPQKPA6W', 'MGBUUV8MHBY3', 'MGBNVQL7GKLW', 'MGBVBY6P9SYV', 'MGBM4100122', 'MGBABSLD783X', 'MGBAAF5FTFVB', 'MGBBR7CUDJL9', 'MGB7NNNVNHQ2', 'MGB3BNYL2APQ', 'MGBYDL4AHNTD']

    codes = ['HB8073L1', 'HB8073L2', 'HB8073L3', 'codigo torto']  # bases ricardo
    # codes = ['87448']
    # codes = ['MGB3YPXRQTX6', 'MGB2UR84PJZQ', 'MGBHMMTXL7C5', 'MGB57UCG9GW3', 'MGBZN5AJPN22']

    codesSuccess = []
    codesError = []

    updatePriceLog = []
    generalReport = []

    updated = False  # houver update
    for row in records:
        amount = 0
        if row[COLACTION] == 'Ajustar':
            print('\n\n---')
            print('adjustment in market: ' + str(row[COLMARKETCODE]))
            for productCode in codes:
                priceOriginal = 0
                priceSaleOriginal = 0
                priceAdjustment = 0
                priceSaleAdjustment = 0

                delayS()
                print('\n-')
                print('product code: ' + str(productCode))
                # get product data
                link = getMarket(productCode, row[COLMARKETCODE], apikey)
                try:
                    products = link.json()['retorno']
                    products = products['produtos']
                except:
                    print('ERROR GET MARKET')
                    print('status code: ' + str(link.status_code))
                    pprint.pprint(link.json())
                else:
                    for productItem in products:
                        product = productItem['produto']
                        productPriceBling = round(float(product['preco']), 2)
                        productDescription = product['descricao']

                        # if product have link with market:
                        try:
                            productMarket = product['produtoLoja']
                            idProductMarket = productMarket['idProdutoLoja']
                            productMarketPriceTuple = productMarket['preco']
                            productPriceMarket = round(float(productMarketPriceTuple['preco']), 2)
                            productPriceSaleMarket = round(float(productMarketPriceTuple['precoPromocional']), 2)
                        except:
                            print(f'there no link between product {productCode} and market {row[COLMARKETCODE]}')
                        else:
                            # reference price
                            if 'preço bling' in row[COLRELATIONPRICE]:
                                print('selected price bling option')
                                priceOriginal = productPriceBling
                            elif 'preço vínculo na loja' in row[COLRELATIONPRICE]:
                                print('selected price link option')
                                priceOriginal = productPriceMarket
                            print('price initial: ' + str(priceOriginal))

                            # priceSaleOriginal = priceOriginal
                            # if productPriceSaleMarket is not None:  #### verifies
                            #     priceSaleOriginal = productPriceSaleMarket
                            # else:
                            #     priceSaleOriginal = None  # if None but has adjustment ????????
                            # readjust price

                            if 'inserir valor' in row[COLTYPEADJUSTMENT]:
                                if '(%) porcentagem' in row[COLFORMAT]:
                                    if row[COLPRICE] != '':
                                        priceAdjustment = ((float(formatAdjustmentPrice(row[COLPRICE])) * priceOriginal) / 100) + priceOriginal  # diferente de nulo
                                        print(f'option: insert value, format: %, original price: {priceOriginal}, adjustment price {priceAdjustment}')
                                        format = '%'
                                    if row[COLPRICESALE] != '':
                                        pass
                                        # priceSaleAdjustment = (float(formatAdjustmentPrice(row[COLPRICESALE])) / 100) * priceOriginal
                                elif '(R$) valor' in row[COLFORMAT]:
                                    if row[COLPRICE] != '':
                                        priceAdjustment = priceOriginal + float(formatAdjustmentPrice(row[COLPRICE]))
                                        print(f'option: insert value, format: R$, original price: {priceOriginal}, adjustment price {priceAdjustment}')
                                        format = 'R$'
                                    if row[COLPRICESALE] != '':
                                        # priceSaleAdjustment = priceSaleOriginal + float(formatAdjustmentPrice(row[COLPRICESALE]))  #### fix this cuz get price already updated
                                        pass
                            elif 'regra mercado' in row[COLTYPEADJUSTMENT]:
                                priceAdjustment = marketRules(row[COLMARKETCODE], priceOriginal)
                                print(f'option: market rule, format: R$, original price: {priceOriginal}, adjustment price {priceAdjustment}')
                                format = 'R$'

                            status = 'erro'
                            if priceOriginal > 0 and priceAdjustment > 0 and priceOriginal != priceAdjustment:
                                priceSaleAdjustment = priceAdjustment
                                xml = xmlProductMarket(idProductMarket, round(priceAdjustment, 2), priceSaleAdjustment)
                                response = putMarket(productCode, row[COLMARKETCODE], xml, apikey)
                                if response.status_code == 200:
                                    try:
                                        responseReturn = response.json()['retorno']
                                        productsMarket = responseReturn['produtosLoja']
                                    except:
                                        codesError.append(productCode)
                                        print('ERROR! put market')
                                        print('status code: ' + str(response.status_code))
                                        pprint.pprint(response.json())
                                    else:
                                        codesSuccess.append(productCode)
                                        print('SUCCESS! price updated')
                                        status = 'sucesso'
                                        amount += 1
                                        updated = True

                            # # when new product - reuse function
                            # try:
                            #     if productPriceMarket is not None:
                            #         pass
                            # except:
                            #     productMarketPrice = 'sem valores anteriormente'
                            else:
                                print('ERROR! invalid price')

                            print('\n-\ndetails')
                            print(f'status: {status} product: {productCode} market: {row[COLMARKETCODE]} type: {row[COLTYPEADJUSTMENT]} price in: {row[COLRELATIONPRICE]}')
                            print(f'previous price: {priceOriginal} final price: {priceAdjustment}')

                            log = {
                                'status': status,
                                'code product': productCode,
                                'code market': row[COLMARKETCODE],
                                'name market': row[COLMARKETNAME],
                                'description': productDescription,
                                'price previous': priceOriginal,
                                'price sale previous': priceSaleOriginal,
                                'price adjusted': priceAdjustment,
                                'price sale adjusted': priceSaleAdjustment, #### fix
                                'price format adjustment': row[COLFORMAT],
                                'value price adjustment': formatAdjustmentPrice(row[COLPRICE]),
                                'value price sale adjustment': formatAdjustmentPrice(row[COLPRICESALE]),
                                'price bling': productPriceBling,
                                'price link': productPriceMarket,
                                'data': datetime.now().strftime('%d/%m/%Y %H:%M:%S')
                            }
                            updatePriceLog.append(log)
                            # inputRow(sheet, index, row):
                            inputRow(sheet, indexCustomerPage + 1, list([status, datetime.now().strftime('%d/%m/%Y %H:%M:%S'), productCode, row[COLMARKETCODE], productDescription, priceAdjustment, productPriceMarket, productPriceBling]))
            try:
                if 'inserir valor' in row[COLTYPEADJUSTMENT]:
                    value = formatAdjustmentPrice(row[COLPRICE])
                elif 'regra mercado' in row[COLTYPEADJUSTMENT]:
                    format = '-'
                    value = 'Regra de mercado'

                marketReport = {
                    'name market': row[COLMARKETNAME],
                    'code market': row[COLMARKETCODE],
                    'format': format,
                    'value': str(value),
                    'amount': amount,
                }
                generalReport.append(marketReport)
            except:
                print('no market to add to report')

            # removing values from google sheet
            print('updating values in google sheets')
            insertValue(sheet, indexCustomerPage, records.index(row) + 2, indexCOLRELATIONPRICE, '')
            insertValue(sheet, indexCustomerPage, records.index(row) + 2, indexCOLTYPEADJUSTMENT, '')
            delayL()
            insertValue(sheet, indexCustomerPage, records.index(row) + 2, indexCOLFORMAT, '')
            insertValue(sheet, indexCustomerPage, records.index(row) + 2, indexCOLPRICE, '')
            insertValue(sheet, indexCustomerPage, records.index(row) + 2, indexCOLPRICESALE, '')
            delayM()
            # ajustar -> ajustado
            insertValue(sheet, indexCustomerPage, records.index(row) + 2, indexCOLACTION, f"Ajustado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
            insertValue(sheet, indexCustomerPage, records.index(row) + 2, indexCOLPRICEDATA, datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
            # num products
            delayL()
            insertValue(sheet, indexCustomerPage, records.index(row) + 2, indexCOLPRICENUM, str(amount))
    if updated:
        print('download csv files')

        # just for fast research
        codesPath = backupCodesUpdatePricePath() + 'successCodes' + customerName + datetime.now().strftime("%d-%m-%Y")
        pd.DataFrame(codes).to_csv(codesPath + '.csv', index=False)
        codesPath = backupCodesUpdatePricePath() + 'errorCodes' + customerName + datetime.now().strftime("%d-%m-%Y")
        pd.DataFrame(codes).to_csv(codesPath + '.csv', index=False)

        generalReportPath = backupPriceUpdatePath() + f'generalReport{datetime.now().strftime("%d-%m-%Y-%H-%M-%S")}'
        updatePriceLogPath = backupPriceUpdatePath() + f'productLog{datetime.now().strftime("%d-%m-%Y-%H-%M-%S")}'
        pd.DataFrame(generalReport).to_csv(generalReportPath, index=False)
        pd.DataFrame(updatePriceLog).to_csv(updatePriceLogPath, index=False)
        recipients = emailTriboUpdatePrice()
        recipients.append(emailCustomer(sheet, indexCustomerAccess))
        priceUpdateEmail(generalReportPath, updatePriceLogPath, recipients, senderMail(), senderPass())
