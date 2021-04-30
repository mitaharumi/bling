import time
import glob
import shutil
import os
import csv

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from adhibition.suport.delay import delayS, delayM
from access.access import downloadFolderPath, backupSheetLinkMarket, applicationFolderPath, productFileCsvPath

def login(driver, userBling, passBling):
    url = 'https://www.bling.com.br/login'
    driver.get(url)
    try:
        userField = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="username"]')))
        userField.send_keys(userBling)

        passField = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="senha"]')))
        passField.send_keys(passBling)

        button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="form-login"]/div/div[3]/button')))
        button.click()

        delayM()
    except:
        raise ValueError('ERROR - LOGIN')
        driver.quit()

# option = 'Exportar planilha de produtos selecionados para vínculo multiloja'
# select products linked -> download csv of each market -> for each page product
def backupSheet(driver, nameCustomer):
    print('backup sheet link multimarket')
    url = 'https://www.bling.com.br/produtos.php#list'
    driver.get(url)

    filter = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="open-filter"]')))
    filter.click()

    filterLinkMarket = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="filtro-lojas"]/option[3]')))
    filterLinkMarket.click()

    try:
        filterLinkMarket = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, f'//*[@id="lojasVinculadas"]/option[1]')))
        filterLinkMarket.click()
        delayM()
        filterButton = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="filter-button-area"]/button')))
        filterButton.click()
        delayM()
    except:
        print('ERROR - BACKUPSHEETS')
        print('can not select linked market')
    else:
        page = 1
        while True:
            print('page: ' + str(page))
            try:
                # max products select = 200 (2 pages)
                # clear selected products previous so get 100 products
                # for optimize this later: download 200 products per time, be careful with stop, ideas: count max 2 try get next if reset count and next, if dont except try get one if get ok and end backup if dont end backup...
                clearFilter = WebDriverWait(driver, 30).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="search-tag"]/span[3]/span[2]/span[2]/i')))
                clearFilter.click()
                print('clear filter selected products')
                delayM()
            except:
                pass
            print('select products')
            checkbox = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="datatable"]/table/thead/tr[1]/th[1]/div/label')))
            checkbox.click()
            delayM()
            try:
                exportSheet = WebDriverWait(driver, 30).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, '//*[@id="container"]/div[10]/div/div[2]/div[7]/div/ul/li[3]')))
                exportSheet.click()
                delayM()
            except:
                moreOption = WebDriverWait(driver, 30).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="container"]/div[10]/div/div[2]/div[7]/span[1]')))
                moreOption.click()
                delayS()
                exportSheet = WebDriverWait(driver, 30).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, '//*[@id="container"]/div[10]/div/div[2]/div[7]/div/ul/li[3]')))
                exportSheet.click()
                delayM()

            indexMarket = 2
            while True:
                print('select market to export')
                # try:
                #     warning = WebDriverWait(driver, 30).until(
                #         EC.element_to_be_clickable((By.XPATH, '/html/body/div[13]/div[3]/div/button/span')))
                #     warning.click()
                # except:
                #     pass
                try:
                    market = WebDriverWait(driver, 30).until(
                        EC.element_to_be_clickable(
                            (By.XPATH, f'//*[@id="listaLojasAtivasGeneral"]/option[{indexMarket}]')))
                    market.click()
                    print(indexMarket)
                    indexMarket += 1
                    delayS()
                except:
                    closeDownload = WebDriverWait(driver, 30).until(
                        EC.element_to_be_clickable((By.XPATH, '/html/body/div[11]/div[3]/div/button[2]/span')))
                    closeDownload.click()
                    print(indexMarket)
                    break
                else:
                    generate = WebDriverWait(driver, 30).until(
                        EC.element_to_be_clickable((By.XPATH, '//*[@id="btnGerarArquivoPrecosMultiloja"]/span')))
                    generate.click()
                    delayS()
                    download = WebDriverWait(driver, 30).until(
                        EC.element_to_be_clickable((By.XPATH, '//*[@id="linkDownloadPrecosMultiloja"]/p/a')))
                    download.click()
                    shutil.move(
                        ((max((glob.glob(downloadFolderPath() + '*.zip')), key=os.path.getctime)).replace('\\', '/')),
                        backupSheetLinkMarket(max((glob.glob(downloadFolderPath() + '*.zip')), key=os.path.getctime),
                                              nameCustomer))
                    print('.csv downloaded!')
            try:
                nextPage = WebDriverWait(driver, 30).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="pagination"]/ul/li[4]/span/span[1]')))
                nextPage.click()
                delayM()
                page += 1
            except:
                break

def seeUsersBling(driver):
    url = 'https://www.bling.com.br/b/usuarios.php#list'
    driver.get(url)


def generateApiKey(driver):
    url = 'https://www.bling.com.br/usuarios.php#add'
    driver.get(url)
    try:
        userApi = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="detalhe"]/div[3]/div/input[2]')))
        userApi.click()

        name = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="nome"]')))
        name.send_keys('Tribo Urbana API')

        email = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="email"]')))
        email.send_keys('relatorioagenciatribourbana@gmail.com')

        generateKey = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="userForm"]/div[4]/div[1]/div[2]/input')))
        generateKey.click()

        time.sleep(1)
        apikey = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="apikey"]')))
        blingApikey = apikey.get_attribute('value')

        # select permissions
        time.sleep(1)
        registerPermission = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="userForm"]/div[6]/div/div/label')))
        registerPermission.click()

        supply = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="aba_2"]/a')))
        supply.click()
        time.sleep(1)
        supplyPermission = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="userForm"]/div[6]/div/div/label')))
        supplyPermission.click()

        sale = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="aba_3"]')))
        sale.click()
        time.sleep(1)
        salePermission = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="userForm"]/div[6]/div/div/label')))
        salePermission.click()

        finance = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="aba_5"]')))
        finance.click()
        time.sleep(1)
        financePermission = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="userForm"]/div[6]/div/div/label')))
        financePermission.click()

        service = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="aba_6"]')))
        service.click()
        time.sleep(1)
        servicePermission = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="userForm"]/div[6]/div/div/label')))
        servicePermission.click()

        preference = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="aba_9"]')))
        preference.click()
        time.sleep(1)
        preferencePermission = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="userForm"]/div[6]/div/div/label')))
        preferencePermission.click()

        save = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="controls"]/input[1]')))
        save.click()

        driver.quit()
        return blingApikey

    except:
        driver.quit()
        raise ValueError('Error generate APIKEY')


# for access filters fields
def clickLeft(driver):
    try:
        leftArea = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="search-left-area"]')))
        leftArea.click()
    except:
        raise ValueError('can not click left area')
        driver.quit()


def clickTagField(driver):
    try:
        tagField = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="filtro-tags"]')))
        tagField.click()
    except:
        raise ValueError('can not click tag field')
        driver.quit()


def tagSelect(driver, xpath):
    try:
        tagSelect = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, xpath)))
        tagSelect.click()
    except:
        raise ValueError('tag select error')
        driver.quit()


def tag(driver, option):
    #### fix xpath of tags, put tag that are used by the company
    xpaths = {
        'tag1': '//*[@id="filtro-tags"]/optgroup[3]/option[2]',
    }
    for key, value in xpaths.items():
        if key == option:
            tagSelect(driver, value)


def listProductCsv(driver):
    try:
        # click on export csv
        moreOption = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="container"]/div[10]/div/div[2]/div[7]/span[2]')))
        moreOption.click()
        exportOption = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="container"]/div[10]/div/div[2]/div[7]/div/ul/li[2]')))
        exportOption.click()

        # if download xls
        # fieldFormatXls = WebDriverWait(driver, 30).until(
        #     EC.element_to_be_clickable((By.XPATH, '//*[@id="formato"]/option[2]')))
        # fieldFormatXls.click()
        '''
            Bling message: 
                Atenção
                O formato XLS possui limite de trinta mil caracteres por célula de acordo com sua especificação.
                Recomenda-se o uso do formato CSV para exportação de produtos contendo maiores informações adicionais.
        '''
        # download csv
        fieldFormatCsv = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="formato"]/option[1]')))
        fieldFormatCsv.click()
        fieldTypeCustom = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="tipo_campos"]/option[2]')))
        fieldTypeCustom.click()
        # download items (more than one csv file)
        listProducts = []  # list of dictionary
        downloadIndex = 1
        while True:
            try:
                def fileLastDownload(oldPathFolder, extension):
                    filePathList = glob.glob(oldPathFolder + '*.' + extension)
                    print(max(filePathList, key=os.path.getctime).replace('\\', '/'))
                    return (max((glob.glob('download' + '*.csv')), key=os.path.getctime)).replace('\\', '/')

                def fileDelete(pathFile):
                    if os.path.exists(pathFile):
                        os.remove(pathFile)
                        return True
                    else:
                        return False

                # download file
                download = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, f'//*[@id="lista"]/tbody/tr[{downloadIndex}]/td/a')))
                download.click()
                print('download: ' + str(downloadIndex))
                downloadIndex = downloadIndex + 1
                #### implementation have to config folder
                # considering downloading in the download folder
                # rename and move file
                shutil.move(
                    ((max((glob.glob(downloadFolderPath() + '*.csv')), key=os.path.getctime)).replace('\\', '/')),
                    productFileCsvPath())
                with open(productFileCsvPath(), newline='', encoding='utf-8') as file:
                    reader = csv.reader(file, delimiter=';')
                    # without header
                    next(reader, None)
                    for row in reader:
                        product = {
                            'id': row[0],
                            'code': row[1].replace('\t', ''),
                            'description': row[2]
                        }
                        listProducts.append(product)
                fileDelete(applicationFolderPath() + 'product.xls')
            except:
                break
        return listProducts
    except:
        raise ValueError


# return dictionary list with markets code and name
def marketsBling(driver):
    data = []
    time.sleep(5)
    index = 1
    while True:
        try:
            url = 'https://www.bling.com.br/configuracoes.integracoes.lojas.virtuais.php#list'
            driver.get(url)
            time.sleep(3)
            clickMarket = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, f'//*[@id="container-stores-enabled"]/tbody/tr[{index}]')))
            clickMarket.click()
            time.sleep(10)
            print(index)
            code = driver.find_element_by_id('codigoLoja')
            name = driver.find_element_by_id('nomeLoja')
            market = {
                'code': code.get_attribute('value'),
                'name': name.get_attribute('value')
            }
            print(market)
            data.append(market)
            time.sleep(5)
            print('market list: ' + str(data))
            index = index + 1
        except:
            break
    return data

# FIX: sync do not stop (page next do not reaches)
def syncPricesMarketplaces(driver):
    print('synchronize prices products in marketplaces')
    url = 'https://www.bling.com.br/produtos.php#list'
    driver.get(url)

    filter = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="open-filter"]')))
    filter.click()

    filterLinkMarket = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="filtro-lojas"]/option[3]')))
    filterLinkMarket.click()

    page = 1
    try:
        print('select only linked products')
        filterLinkMarket = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, f'//*[@id="lojasVinculadas"]/option[1]')))
        filterLinkMarket.click()
        delayM()
        filterButton = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="filter-button-area"]/button')))
        filterButton.click()
        delayM()

    except:
        print('error select only linked products')
    else:
        page = 1
        while True:
            print('page: ' + str(page))
            try:
                clearFilter = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="search-tag"]/span[3]/span[2]/span[2]/i')))
                clearFilter.click()
                print('clear filter selected products')
                delayM()
            except:
                pass
            print('select products')
            checkbox = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="datatable"]/table/thead/tr[1]/th[1]/div/label')))
            checkbox.click()
            delayM()

            indexMarket = 2
            while True:
                print('select market')
                # try:
                #     warning = WebDriverWait(driver, 30).until(
                #         EC.element_to_be_clickable((By.XPATH, '/html/body/div[13]/div[3]/div/button/span')))
                #     warning.click()
                # except:
                #     pass
                try:
                    syncPriceOption = WebDriverWait(driver, 30).until(
                        EC.element_to_be_clickable(
                            (By.XPATH, '//*[@id="sincPrecosLojasVirtuais"]/span[2]')))
                    syncPriceOption.click()
                    delayM()
                    market = WebDriverWait(driver, 30).until(
                        EC.element_to_be_clickable(
                            (By.XPATH, f'//*[@id="listaLojasAtivasGeneralPrice"]/option[{indexMarket}]')))
                    market.click()
                    indexMarket += 1
                    delayS()
                except:
                    syncClose = WebDriverWait(driver, 30).until(
                        EC.element_to_be_clickable((By.XPATH, '/html/body/div[11]/div[1]/button/span[1]')))
                    syncClose.click()
                    break
                else:
                    syncPrices = WebDriverWait(driver, 30).until(
                        EC.element_to_be_clickable((By.XPATH, '/html/body/div[11]/div[3]/div/button[1]/span')))
                    syncPrices.click()
                    delayS()
                    syncConfirm = WebDriverWait(driver, 15).until(
                        EC.element_to_be_clickable((By.XPATH, '/html/body/div[11]/div[3]/div/button[1]/span')))
                    syncConfirm.click()
                    delayS()
                    print('prices synchronized')
            try:
                nextPage = WebDriverWait(driver, 30).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="pagination"]/ul/li[4]/span/span[1]')))
                nextPage.click()
                delayM()
                page += 1
            except:
                print('no page next')
                stop = True