import os
import mysql.connector
from dotenv import load_dotenv
from flask import Flask, render_template, jsonify

load_dotenv()

app = Flask(__name__)

def conectar_banco():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_DATABASE")
    )

@app.route('/')
def inicio():
    return render_template('index2.html')

@app.route('/caixa')
def caixa():
    return render_template('index.html')

@app.route('/api/produtos', methods=['GET'])
def listar_produtos():
    conexao = None
    cursor = None

    try:
        conexao = conectar_banco()
        cursor = conexao.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                p.id,
                p.nome,
                p.preco,
                p.quantidade,
                c.nome AS categoria
            FROM produtos AS p
            LEFT JOIN categorias AS c
                ON c.id = p.categoria_id
            ORDER BY p.nome
        """)

        produtos = cursor.fetchall()

        for produto in produtos:
            produto['preco'] = str(produto['preco'])

        return jsonify(produtos)

    except mysql.connector.Error:
        app.logger.exception("Erro ao consultar produtos")
        return jsonify({
            "erro": "Não foi possível carregar os produtos."
        }), 500

    finally:
        if cursor is not None:
            cursor.close()

        if conexao is not None:
            conexao.close()


if __name__ == '__main__':
    app.run(debug=True)
