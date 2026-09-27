import mysql.connector

conexao = mysql.connector.connect(
    host="localhost",
    user="root",
    password="gulugu777",
    database="mercado_database"
)

ferramenta = conexao.cursor()

ferramenta.execute("SELECT * FROM produtos")

resultado = ferramenta.fetchall()

def seletor():
    menu = input ('Escolha a função desejada: ')
    
    if menu not in opcoes:
        print ('Escolha 1, 2, 3 ou 4')
        return seletor()
    
    if menu == '1':
        print ('Caixa')
    
    elif menu == '2':
        print ('Controle financeiro')
            
    elif menu == '3':
        gestao_produtos()

    elif menu == '4':
        infos()

def infos():
    visualizar = input ('Visualizar produtos? ').lower()
    
    if visualizar == 'nao' or visualizar == 'não':
        seletor()
       
    elif visualizar == 'sim':
        print (resultado)

def gestao_produtos():
    print ('1 - Adicionar produto')
    print ('2 - Excluir Produto')
    print ('3 - Modificar Produto')

    gestao = input ('Selecione 0/1/2 ou 3: ')

    if gestao == '0':
        seletor()

    elif gestao == '1':
        nome = input ('Adicione o nome do produto: ')
        preco = float(input('Digite o preço: '))
        quantidade = int(input('Digite a quantidade em estoque: '))
                
        ferramenta.execute(
        "insert into produtos(nome, preco, quantidade) values (%s, %s, %s)",
        (nome, preco, quantidade)
        )
        conexao.commit()
        ferramenta.execute ('select * from produtos')
        resultado = ferramenta.fetchall()

    elif gestao == '2':
        nome = input ('Insira o nome do produto: ')
        
        ferramenta.execute (("delete from produtos where nome = %s"),
            (nome,)
        )
        conexao.commit()
        ferramenta.execute ('select * from produtos')
        resultado = ferramenta.fetchall()

    elif gestao == '3':
        nome = input ('Insira o nome do produto: ')
        novo_nome = input ('Insira o novo nome:')
        novo_preco = float(input('Digite o novo preco: '))
        
        ferramenta.execute (('update produtos set nome = %s, preco = %s where nome = %s'),
            (novo_nome, novo_preco, nome)
        )
        conexao.commit()
        ferramenta.execute ('select * from produtos')
        resultado = ferramenta.fetchall()

opcoes = ['1', '2', '3', '4']

while True:

    print ('1- Caixa')
    print ('2 - Controle Financeiro')
    print ('3 - Mercadorias')
    print ('4- Visualizar produtos')

    menu = seletor()

    visualizar = infos()
