// Verificar as senhas.
let form = document.querySelector('form')
form.addEventListener('submit', (e)=>{
    // Parar envio do formulário.
    e.preventDefault();

    // Verificar senhas.
    let nome = document.querySelector('input[name="nome"]');
    let email = document.querySelector('input[name="email"]');
    let password = document.querySelector('input[name="password"]');
    let passwordc = document.querySelector('input[name="passwordc"]');

    if(nome.value.length == 0){
        nome.style.border = "1px solid red";
    }
    if(email.value.length == 0){
        email.style.border = "1px solid red";
    }
    if(password.value.length == 0){
        password.style.border = "1px solid red";
    }
    if(passwordc.value.length == 0){
        passwordc.style.border = "1px solid red";
    }

    // Caso esteja tudo correto.
    if((password.value.length) >= 8 && (passwordc.value.length) >= 8){
        if(password.value.length === passwordc.value.length){
            form.submit();
        }
    }else{
        password.style.border = "1px solid red";
        passwordc.style.border = "1px solid red";
    }
})
