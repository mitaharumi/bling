# remove R$
# remove %
# remove space
# replace , to .
def formatAdjustmentPrice(value):
    value = value.replace('%', '')
    value = value.replace('R$', '')
    value = value.replace('%', '')
    value = value.replace(' ', '')
    value = value.replace('.', '')
    value = value.replace(',', '.')
    return value
