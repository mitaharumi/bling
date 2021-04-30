# page start in 0
# access costumer (rows) and column in 1

from adhibition.suport.delay import delayS, delayM

# index column page 0 (ACCESS)
PAGEACCESS = 0
PAGEFIRSTCUSTOMER = 2
COLCUSTOMERNAME = 2
COLLOGIN = 3
COLPASS = 4
COLAPI = 5
COLEMAIL = 6

COLMARKETNAME = 1
COLMARKETCODE = 2
def getValue(sheet, indexPage, row, column):
    page = sheet.get_worksheet(indexPage)
    return page.cell(row, column).value

def insertValue(sheet, indexPage, row, column, value):
    page = sheet.get_worksheet(indexPage)
    page.update_cell(row, column, value)

def findByName(sheet, index, name):
    cell = sheet.get_worksheet(index)
    cell = cell.find(name)
    return cell.row, cell.col

def loginBling(sheet, indexAccess):  # access in page 0
    return getValue(sheet, PAGEACCESS, indexAccess, COLLOGIN), getValue(sheet, PAGEACCESS, indexAccess, COLPASS)

def apikey(sheet, indexAccess):
    return getValue(sheet, PAGEACCESS, indexAccess, COLAPI)

def emailCustomer(sheet, index):
    return getValue(sheet, PAGEACCESS, index, COLEMAIL)

# return names page list
def namesPages(sheet):
    names = []
    index = PAGEACCESS + 1
    while True:
        try:
            delayS()
            page = sheet.get_worksheet(index)
            names.append(page.__getattribute__('title'))
            index = index + 1
        except:
            print('names pages: ' + str(names))
            return names

def pageIndex(sheet, name):
    index = PAGEFIRSTCUSTOMER
    while True:
        try:
            delayS()
            page = sheet.get_worksheet(index)
            namePage = page.__getattribute__('title')
            print(namePage)
            if namePage == name:
                print('page index: ' + str(index))
                return index
        except:
            print('page name not found')
            break
        index += 2

# put names pages on PAGEACCESS
def inputPagesName(sheet):
    pageAccess = sheet.get_worksheet(PAGEACCESS)
    indexRow = 2
    indexName = 0
    names = namesPages(sheet)
    while True:
        try:
            delayM()
            pageAccess.update(f'b{indexRow}', names[indexName])
            indexRow += 1
            indexName += 1
        except:
            break

def inputCodeNameMarket(sheet, indexPage, dataMarket):
    row = 2  # index row start
    for data in dataMarket:
        delayM()
        insertValue(sheet, indexPage, row, COLMARKETNAME, data['name'])
        delayM()
        insertValue(sheet, indexPage, row, COLMARKETCODE, data['code'])
        row += 1

def worksheetRecords(sheet, index):
    worksheet = sheet.get_worksheet(index)
    record = worksheet.get_all_records()
    return record

def inputRow(sheet, index, row):
    worksheet = sheet.get_worksheet(index)
    worksheet.append_row(row)
