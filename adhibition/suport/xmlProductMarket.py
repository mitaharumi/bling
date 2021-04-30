from dict2xml import dict2xml
'''
POST /produtoLoja/{idLoja}/{codigo
https://ajuda.bling.com.br/hc/pt-br/articles/360047062813-POST-produtoLoja-idLoja-codigo-

PUT /produtoLoja/{idLoja}/{codigo}
https://ajuda.bling.com.br/hc/pt-br/articles/360046422594-PUT-produtoLoja-idLoja-codigo-

table xml fields:
-------------------------------------------------------------------------------------------------------------------------
- Grupo	          Campo	                Informação	                                    Tipo                Estrutura   -
-------------------------------------------------------------------------------------------------------------------------
- raiz        	    produtosLoja                                                                            Obrigatório -
- produtosLoja	    produtoLoja                                                                             Obrigatório -
- produtoLoja	    idLojaVirtual       Identificador do Produto na Loja Virtual        String(45)          Obrigatório -
- produtoLoja 	    preco                                                                                   Obrigatório -
- preco       	    preco               Preço de venda na Loja Virtual                  Decimal(17,10)      Obrigatório -
- preco	            precoPromocional    Preço promocional na Loja Virtual               Decimal(17,10)      Opcional    -
- produtoLoja	    idFornecedor        Identificador do Fornecedor na Loja Virtual	    Integer(11)         Opcional    -
- produtoLoja	    idMarca             Preço promocional na Loja Virtual	            Integer(11)         Opcional    -
- categoriasLoja    categoriaLoja                                                                           Opcional    -
- categoriaLoja	    idCategoria         ID da Categoria no Bling 	                    Integer(11)         Opcional    -
-------------------------------------------------------------------------------------------------------------------------
'''
## construction: only optional is precoPromocional
### search smart way to add option elements to the dictionary

def xmlProductMarket(idProdutoLoja, price, priceSale):
    #### fix to do not need this coditional
    if idProdutoLoja == '0' or idProdutoLoja == 0 or idProdutoLoja == '':
        idProdutoLoja = ' 0'
    if priceSale is None:
        productMarket = {
            'produtoLoja': {
                'idLojaVirtual': f'{idProdutoLoja}',
                'preco': {
                    'preco': float(f'{price}')
                }
            }
        }
    else:
        productMarket = {
            'produtoLoja': {
                'idLojaVirtual': f'{idProdutoLoja}',
                'preco': {
                    'preco': float(f'{price}'),
                    'precoPromocional': float(f'{priceSale}')
                }
            }
        }
    xmlString = dict2xml(productMarket, wrap='produtoLoja', indent='   ')
    return xmlString