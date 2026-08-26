function efetuarLogin() {
    /*AQUI ABAIXO BANCO DE DADOS*/
    localStorage.setItem("usuarioLogado", "true");
  
    window.location.href = "index.html";
}

function fazerLogout() {

    /*BANCO DE DADOS NA LINHA ABAIXO*/
    localStorage.removeItem("usuarioLogado");
    window.location.href = "login.html";
}

/*CADASTRO*/

document.getElementById('form-cad').addEventListener('submit', function(e) {
    e.preventDefault();
    const nome = document.getElementbyId('cadNome').value;
    const email = document.getElementById('cadEmail').value;
    const senha = document.getElementById('cadSenha').value;
    const telefone = document.getElementById('cadTelefone').value;


    /*TESTE TESTE TESTE BANCO DE DADOS É AQUI!!!!*/
    localStorage.setItem('user_' + nome, email, senha, telefone);
    alert('Conta criada com sucesso!');
    this.reset();

    window.location.href = 'login.html';

});

/*LOGIN*/

document.getElementById('form-login').addEventListener('submit', function(e) {
    e.preventDefault();

    const email = document.getElementById('email').value;
    const senha = document.getElementById('senha').value;

    const senhaSalva = localStorage.getItem('user_' + email);

    if (senhaSalva && senhaSalva === senha) {

        localStorage.setitem('usuarioLogado', email);

        window.location.href = 'index.html';
    } else {
        alert('Usuário ou senha incorretos.');
    }

});