Use mercado_database;

create table produtos (
    id int primary key auto_increment,
    nome varchar(100) not null,
    preco decimal(10,2) not null,
    quantidade int not null
);

select * 
from produtos;

insert into produtos (nome, preco, quantidade);
values (%s, %s, %s)

delete
from produtos
where nome = %s

UPDATE produtos
set preco = %s
set nome = %s
set quantidade
where nome = %s