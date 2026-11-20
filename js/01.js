const listaProdutos = document.querySelector('#lista-produtos');

let produtos = [];

function carregarProdutos() {
    fetch('/api/produtos')
        .then(function(resposta) {
            return resposta.json();
        })
        .then(function(dados) {
            produtos = dados;
            console.log(produtos);
        })
        .catch(function(erro) {
            console.log('Erro ao carregar produtos:', erro);
        });

        then(function(dados) {
            produtos = dados;

            console.log('Produtos recebidos:', produtos);
            console.log('Quantidade:', produtos.length);
        })
}

carregarProdutos();