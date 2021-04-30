def purpleTable(df):
    # general
    padding = "14px"
    textAlign = 'center'
    fontFamily = 'Roboto, Arial'

    # header
    headerBg = '#9DA0E4'
    headerColor = '#F6F7FC'
    headerFontSize = 'medium'
    headerFontWeight = 'bold'
    headerBottom = '5px solid #FFFFFF'

    # content
    oddBg = '#F9F9FF'
    evenBg = '#F2F3FF'
    fontColor = '#61638D'
    fontSize = 'small'
    fontWeight = 'lighter'
    
    # build html table
    body = ""
    index = 0
    while index != len(df):
        # header
        if index == 0:
            dfHtmlOutput = df.iloc[[index]].to_html(na_rep="", index=False, border=0)
            dfHtmlOutput = dfHtmlOutput.replace('<th>'
                                                    , '<th style = "background-color: ' + headerBg
                                                    + ';font-family: ' + fontFamily
                                                    + ';font-size: ' + headerFontSize
                                                    + ';color: ' + headerColor
                                                    + ';text-align: ' + textAlign
                                                    + ';font-weight: ' + headerFontWeight
                                                    + ';border-bottom: ' + headerBottom
                                                    + ';padding: ' + padding + '">')
                                                    # + ';border: 5px solid #55038C' +
            # change format of table
            dfHtmlOutput = dfHtmlOutput.replace('<td>'
                                                    , '<td style = "background-color: ' + oddBg
                                                    + ';font-family: ' + fontFamily
                                                    + ';font-size: ' + fontSize
                                                    + ';color: ' + fontColor
                                                    + ';text-align: ' + textAlign
                                                    + ';font-weight: ' + fontWeight
                                                    + ';padding: ' + padding + '">')
                                                    # + ';border: 5px solid green' + '">')
            body = """<p>""" + format(dfHtmlOutput)
            index = 1

        # even
        elif index % 2 == 0:
            dfHtmlOutput = df.iloc[[index]].to_html(na_rep="", index=False, header=False)
            # change format of table
            dfHtmlOutput = dfHtmlOutput.replace('<td>'
                                                    , '<td style = "background-color: ' + oddBg
                                                    + ';font-family: ' + fontFamily
                                                    + ';font-size: ' + fontSize
                                                    + ';color: ' + fontColor
                                                    + ';text-align: ' + textAlign
                                                    + ';font-weight: ' + fontWeight
                                                    + ';padding: ' + padding + '">')
                                                    # + ';border: 5px solid red' + '">')
            body = body + format(dfHtmlOutput)
            index += 1

        # odd
        elif index % 2 != 0:
            dfHtmlOutput = df.iloc[[index]].to_html(na_rep="", index=False, header=False)
            dfHtmlOutput = dfHtmlOutput.replace('<td>'
                                                    , '<td style = "background-color: ' + evenBg
                                                    + ';font-family: ' + fontFamily
                                                    + ';font-size: ' + fontSize
                                                    + ';color: ' + fontColor
                                                    + ';text-align: ' + textAlign
                                                    + ';font-weight: ' + fontWeight
                                                    + ';padding: ' + padding +'">')
                                                    # + ';border: 5px solid blue' + '">')
            body = body + format(dfHtmlOutput)
            index += 1

    body = body + """</p>"""
    body = body.replace("""</td>
    </tr>
  </tbody>
</table>
            <table border="1" class="dataframe">
  <tbody>
    <tr>""", """</td>
    </tr>
    <tr>""").replace("""</td>
    </tr>
  </tbody>
</table><table border="1" class="dataframe">
  <tbody>
    <tr>""", """</td>
    </tr>
    <tr>""")
    return body