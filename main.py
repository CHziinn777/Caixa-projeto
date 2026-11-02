import os
import mysql.connector
from dotenv import load_dotenv
from decimal import Decimal, InvalidOperation

load_dotenv()

conexao = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_DATABASE")
)

ferramenta = conexao.cursor()

ferramenta.execute("SELECT * FROM produtos")

resultado = ferramenta.fetchall()


def seletor():
    while True:
        print('1 - Caixa')
        print('2 - Controle Financeiro')
        print('3 - Mercadorias')
        print('4 - Visualizar produtos')
        print('0 - Sair')

        menu = input('Escolha a função desejada: ').strip()

        if menu == '1':
            caixa()

        elif menu == '2':
            print('Controle financeiro ainda não implementado.')

        elif menu == '3':
            gestao_produtos()

        elif menu == '4':
            infos()

        elif menu == '0':
            print('Encerrando o sistema...')
            break

        else:
            print('Escolha uma opção válida!')


def ler_inteiro(mensagem, minimo=0):
    while True:
        try:
            valor = int(input(mensagem).strip())

            if valor < minimo:
                print(f'Digite um número maior ou igual a {minimo}!')
                continue

            return valor

        except ValueError:
            print('Digite um número inteiro válido!')


def ler_preco(mensagem):
    while True:
        try:
            preco = Decimal(
                input(mensagem).strip().replace(',', '.')
            )

            if not preco.is_finite() or preco < 0:
                print('Digite um preço válido e não negativo!')
                continue

            return preco

        except InvalidOperation:
            print('Valor inválido! Digite um preço numérico.')


def caixa():
    conjunto_total = []

    while True:
        print('1 - Adicionar produto')
        print('2 - Finalizar venda')
        print('3 - Voltar ao menu')

        opcao = input('Escolha uma opção: ').strip()

        if opcao == '1':
            nome = input('Digite o nome do produto: ').strip()

            if not nome:
                print('O nome não pode ficar vazio!')
                continue

            try:
                ferramenta.execute(
                    'SELECT preco FROM produtos WHERE nome = %s',
                    (nome,)
                )
                resultado = ferramenta.fetchone()

            except mysql.connector.Error as erro:
                print(f'Erro ao consultar o banco: {erro}')
                continue

            if resultado is None:
                print('Produto não encontrado!')
                continue

            preco = resultado[0]
            quantia = ler_inteiro(
                'Digite a quantidade desejada: ',
                minimo=1
            )

            sub_total = quantia * preco

            print(f'Subtotal: R$ {sub_total:.2f}')
            conjunto_total.append(sub_total)

        elif opcao == '2':
            if not conjunto_total:
                print('Nenhum produto foi adicionado!')
                continue

            total = sum(conjunto_total, Decimal('0.00'))

            print(f'Total da compra: R$ {total:.2f}')

            while True:
                try:
                    dinheiro = Decimal(
                        input('Digite o dinheiro recebido: ')
                        .strip()
                        .replace(',', '.')
                    )

                    if not dinheiro.is_finite() or dinheiro < 0:
                        print('Digite um valor válido!')
                        continue

                except InvalidOperation:
                    print('Valor inválido!')
                    continue

                if dinheiro < total:
                    print('Dinheiro insuficiente!')
                    continue

                break

            troco = dinheiro - total

            print(f'Troco: R$ {troco:.2f}')
            print('Venda finalizada!')

            return

        elif opcao == '3':
            if conjunto_total:
                confirmacao = input(
                    'Existem produtos na venda. Deseja descartar? (sim/não): '
                ).strip().lower()

                if confirmacao not in ('sim', 's'):
                    continue

            return

        else:
            print('Escolha 1, 2 ou 3!')


def infos():
    visualizar = input(
        'Visualizar produtos? (sim/não): '
    ).strip().lower()

    if visualizar in ('não', 'nao', 'n'):
        return

    if visualizar not in ('sim', 's'):
        print('Resposta inválida!')
        return

    try:
        ferramenta.execute("""
            SELECT
                p.id,
                p.nome,
                p.preco,
                p.quantidade,
                c.nome AS categoria
            FROM produtos p
            LEFT JOIN categorias c
                ON p.categoria_id = c.id
            ORDER BY p.nome
        """)

        resultado = ferramenta.fetchall()

    except mysql.connector.Error as erro:
        print(f'Erro ao consultar produtos: {erro}')
        return

    if not resultado:
        print('Nenhum produto cadastrado.')
        return

    print('\n========= PRODUTOS =========')

    for produto in resultado:
        categoria = produto[4] or 'Sem categoria'

        print(
            f'ID: {produto[0]} | '
            f'Nome: {produto[1]} | '
            f'Preço: R$ {produto[2]:.2f} | '
            f'Estoque: {produto[3]} | '
            f'Categoria: {categoria}'
        )


def gestao_produtos():
    while True:
        print('1 - Adicionar produto')
        print('2 - Excluir produto')
        print('3 - Modificar produto')
        print('0 - Voltar')

        gestao = input('Selecione uma opção: ').strip()

        if gestao == '0':
            return

        elif gestao == '1':
            nome = input('Adicione o nome do produto: ').strip()

            if not nome:
                print('O nome não pode ficar vazio!')
                continue

            preco = ler_preco('Digite o preço: ')

            quantidade = ler_inteiro(
                'Digite a quantidade em estoque: ',
                minimo=0
            )

            categoria = input(
                'Categoria (Outros, Limpeza, Guloseimas, Bebidas): '
            ).strip()

            try:
                ferramenta.execute(
                    'SELECT id FROM categorias WHERE nome = %s',
                    (categoria,)
                )

                resultado = ferramenta.fetchone()

                if resultado is None:
                    print('Categoria não encontrada! Produto não cadastrado.')
                    continue

                categoria_id = resultado[0]

                ferramenta.execute(
                    """
                    INSERT INTO produtos
                    (nome, preco, quantidade, categoria_id)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (nome, preco, quantidade, categoria_id)
                )

                conexao.commit()
                print('Produto cadastrado com sucesso!')

            except mysql.connector.Error as erro:
                conexao.rollback()
                print(f'Erro ao cadastrar produto: {erro}')

        elif gestao == '2':
            produto_id = ler_inteiro(
                'Insira o ID do produto que deseja excluir: ',
                minimo=1
            )

            try:
                ferramenta.execute(
                    'SELECT id, nome FROM produtos WHERE id = %s',
                    (produto_id,)
                )

                resultado = ferramenta.fetchone()

                if resultado is None:
                    print('Produto não encontrado!')
                    continue

                confirmacao = input(
                    f'Confirma a exclusão de {resultado[1]}? (s/n): '
                ).strip().lower()

                if confirmacao == 's':
                    ferramenta.execute(
                        'DELETE FROM produtos WHERE id = %s',
                        (produto_id,)
                    )

                    conexao.commit()
                    print('Produto excluído com sucesso!')

                else:
                    print('Exclusão cancelada.')

            except mysql.connector.Error as erro:
                conexao.rollback()
                print(f'Erro ao excluir produto: {erro}')

        elif gestao == '3':
            produto_id = ler_inteiro(
                'Insira o ID do produto: ',
                minimo=1
            )

            try:
                ferramenta.execute(
                    'SELECT id, nome FROM produtos WHERE id = %s',
                    (produto_id,)
                )

                resultado = ferramenta.fetchone()

                if resultado is None:
                    print('Produto não encontrado!')
                    continue

                novo_nome = input('Insira o novo nome: ').strip()

                if not novo_nome:
                    print('O nome não pode ficar vazio!')
                    continue

                novo_preco = ler_preco('Digite o novo preço: ')

                ferramenta.execute(
                    """
                    UPDATE produtos
                    SET nome = %s, preco = %s
                    WHERE id = %s
                    """,
                    (novo_nome, novo_preco, produto_id)
                )

                conexao.commit()
                print('Produto modificado com sucesso!')

            except mysql.connector.Error as erro:
                conexao.rollback()
                print(f'Erro ao modificar produto: {erro}')

        else:
            print('Opção inválida!')


if __name__ == '__main__':
    seletor()