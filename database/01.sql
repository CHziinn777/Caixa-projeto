USE mercado_database;

CREATE table categoria (
    id INT PRIMARY KEY AUTO_INCREMENT
    nome VARCHAR(50) NOT NULL UNIQUE
);

CREATE table produtos (
    id INT PRIMARY KEY AUTO_INCREMENT
    nome VARCHAR(100) NOT NULL
    preco DECIMAL(10,2) NOT NULL
    quantidade INT NOT NULL
    categoria_id INT
);

SELECT * 
FROM produtos;

INSERT into produtos (nome, preco, quantidade)
VALUES (%s, %s, %s);

DELETE
FROM produtos
WHERE nome = %s

UPDATE produtos
SET preco = %s
SET nome = %s
WHERE nome = %s

CREATE TABLE vendas(
    id INT PRIMARY KEY AUTO_INCREMENT
    data_hora DATETIME NOT NULL
    total DECIMAL(10,2) NOT NULL
)

create table itens_vendidos (
    id INT PRIMARY KEY AUTO_INCREMENT
    venda_id INT NOT NULL
    produto_id INT NOT NULL
    quantidade INT NOT NULL
    preco_unitario DECIMAL(10,2) NOT NULL
)

SELECT produtos.nome, itens_vendidos.quantidade
FROM produtos
INNER JOIN itens_vendidos
ON produtos.id = itens_vendidos.id