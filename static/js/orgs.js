// Getting City Name
var selectRegion = document.querySelector('#regiao');
var selectCity = document.querySelector('#cidade');

// Define input de cidade OFF.
selectCity.disabled = true;

// Pegar a informação.
let uf = selectRegion.options[selectRegion.selectedIndex].text;
selectRegion.addEventListener('change', ()=>{
    
    uf = selectRegion.options[selectRegion.selectedIndex].text;
    selectCity.options.length = 0;

    // Chamar função que puxa dados da API do IBGE.
    get(uf)
})

async function get(uf){
    
    let dados = `https://servicodados.ibge.gov.br/api/v1/localidades/estados/${selectRegion.value}/distritos`
    await fetch(dados)
    .then(res=>{res.json()
        .then(
            data=>{

                    // Habilitar select de cidade.
                    selectCity.disabled = false;
                    if(uf == 'Selecione um estado.'){
                        selectCity.disabled = true;
                    }
                    // Salvar dados em uma lista de cidades.
                    var citys = [];
                    data.forEach(item => {
                        if(!citys.includes(item.municipio.nome)){
                            citys.push(item.municipio.nome)
                        }
                    });
                    inserirOption(citys)
                }
            )
        }
    )    
}

function inserirOption(citys){
    document.querySelector('.text-city').textContent = citys[0];
    citys.forEach(item => {
        let option = new Option(item, item);
        selectCity.add(option);
    })
}

// Tratar informações de cidade selecionada.
selectCity.addEventListener('change', ()=>{
    let cidade = selectCity.options[selectCity.selectedIndex].text;
    document.querySelector('.text-city').textContent = cidade;
})


