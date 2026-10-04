USE mercado_database;

CREATE table produtos (
    id int primary key auto_increment,
    nome varchar(100) not null,
    preco decimal(10,2) not null,
    quantidade int not null
);

SELECT * 
FROM produtos;

INSERT into produtos (nome, preco, quantidade);
VALUES (%s, %s, %s)

DELETE
FROM produtos
WHERE nome = %s

UPDATE produtos
SET preco = %s
SET nome = %s
WHERE nome = %s