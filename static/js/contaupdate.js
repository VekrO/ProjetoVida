document.addEventListener('load', getValues())

function getValues(){

    let name = document.querySelector('input[name=nome]');
    let cnpj = document.querySelector('input[name=CNPJ]');
    let telefone = document.querySelector('input[name=telefone]');
    let descricao = document.querySelector('textarea[name=descricao]');

    descricao.textContent = descricao.value.trim();


}