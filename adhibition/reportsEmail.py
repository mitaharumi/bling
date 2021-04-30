# but not soo pretty kkk
import smtplib
import ssl
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase  # "where input attachment"

import pandas as pd

from adhibition.suport.prettyHtmlTable.purpleTable import purpleTable

def priceUpdateEmail(generalPath, productsPath, recipients, email, password):  # general, products, name customer market):
    print('setup tables for email report')
    # load data
    general = pd.read_csv(generalPath, index_col=False)
    products = pd.read_csv(productsPath, index_col=False)

    generalTableNameColumns = ['Marketplace', 'Produtos', 'Formato', 'Ajuste']
    generalTable = pd.DataFrame(columns=generalTableNameColumns)
    generalTable['Marketplace'] = general['name market']
    generalTable['Produtos'] = general['amount']
    generalTable['Formato'] = general['format']

    # add + or -
    index = 0
    for value in general['value']:
        if value != 'Regra de mercado':
            price = round((float(value)), 2)
            if price > 0:
                value = '+ ' + str(value)
                general.loc[index, 'value'] = value
            else:
                value = '- ' + str(value)
                general.loc[index, 'value'] = value
        index += 1

    generalTable['Ajuste'] = general['value']

    productsTableNameColumns = ['Código', 'Nome', 'Marketplace', 'Preço Atualizado', 'Preço Anterior']
    productsTable = pd.DataFrame(columns=productsTableNameColumns)
    productsTable['Código'] = products['code product']
    productsTable['Nome'] = products['description']
    productsTable['Marketplace'] = products['name market']
    productsTable['Preço Atualizado'] = products['price adjusted']
    productsTable['Preço Anterior'] = products['price previous']

    print('general table')
    print(generalTable)
    print('products table')
    print(productsTable.head(15))

    productsTableHtml = purpleTable(productsTable)
    generalTableHtml = purpleTable(generalTable)

    title = '''<div style="font-family: Roboto, Arial">
	<h2 style="color: #666699;">Relat&oacute;rio de atualiza&ccedil;&atilde;o de pre&ccedil;os dos produtos</h2>
	<h3 style="color: #666699;">Ag&ecirc;ncia </span><span style="color: #800080;">Tribo Urbana</h3>
</div>
'''
    greeting = '''<div style="font-family: Roboto, Arial">
	<h4 style="color: #666699;">Ol&aacute;! Tudo bem?</span></h4>
	<h4 style="color: #666699;">Realizamos alterações no preço dos produtos </span></h4>
</div>
'''
    generalText = '''<div style="font-family: Roboto, Arial">
	<h4 style="color: #666699;">Esta &eacute; a <span style="color: #800080;">tabela geral:</span></h4>
</div>
'''
    productsText = '''<div style="font-family: Roboto, Arial">
	<h4 style="color: #666699;">Aqui est&atilde;o mais alguns<span style="color: #800080;"> detalhes de cada produto</span> alterado:</h4>
</div>
'''
    if (productsTable.shape[0] > 100):
        productsTable = productsTable.head(100)
        productsText = '''<div style="font-family: Roboto, Arial">
    	<h4 style="color: #666699;">Aqui est&atilde;o mais alguns<span style="color: #800080;"> detalhes 100 primeiros produtos</span> atualizados, para visualizar o restante acesse o arquivo em anexo</h4>
    </div>
    '''
    contact = '''<div style="color: #666699; font-family: Roboto, Arial; font-size: small; font-weight: bold;">
	<p>--</p>
	<p>Enviamos em anexo as tabelas acima no formato .csv</p>
	<p>Por favor não responda esse email!</p>
	<p>Caso tenha alguma d&uacute;vida, entre em contato:</p>
	<p>&ensp; <a href="https://api.whatsapp.com/send?phone=5543998202531&text=Fale%20com%20a%20Tribo%20Urbana" style="color: #49c95a; text-decoration-line: none">Whatsapp: <u>(43) 9 9820-2531</u></a></p>
	<p>&ensp; Email: sac@agenciatribourbana.br</p>
</div>'''
    # send mail
    smtpServer = 'smtp.gmail.com'
    port = 465

    message = MIMEMultipart()
    message['Subject'] = 'Atualização de Preço dos Produtos | Agência Tribo Urbana | No Reply'
    message['From'] = 'Relatório Tribo Urbana'
    message['To'] = ", ".join(recipients)

    # attachment
    with open(productsPath, 'rb') as attachment:
        productsAttachment = MIMEBase('application', 'octet-stream')
        productsAttachment.set_payload(attachment.read())
    encoders.encode_base64(productsAttachment)
    productsAttachment.add_header(
        'Content-Disposition',
        f'attachment; filename=tabelaProdutos'
    )

    with open(generalPath, 'rb') as attachment:
        generalAttachment = MIMEBase('application', 'octet-stream')
        generalAttachment.set_payload(attachment.read())
    encoders.encode_base64(generalAttachment)
    generalAttachment.add_header(
        'Content-Disposition',
        f'attachment; filename=tabelaGeral'
    )

    message.attach(MIMEText(title, 'html'))
    message.attach(MIMEText(greeting, 'html'))
    message.attach(MIMEText(generalText, 'html'))
    message.attach(MIMEText(generalTableHtml, 'html'))
    message.attach(MIMEText(productsText, 'html'))
    message.attach(MIMEText(productsTableHtml, 'html'))
    message.attach(MIMEText(contact, 'html'))
    message.attach(productsAttachment)
    message.attach(generalAttachment)

    context = ssl.create_default_context()
    # config msg secondary plain text

    with smtplib.SMTP_SSL(smtpServer, port, context=context) as server:
        server.login(email, password)
        server.sendmail(email, recipients, message.as_string())
        print('report products price update email sent!')