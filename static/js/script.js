// Função para alternar entre as telas da SPA
function navegarPara(paginaId) {
  // Remove a classe 'active' de todas as páginas
  const paginas = document.querySelectorAll('.page');
  paginas.forEach(p => p.classList.remove('active'));

  // Adiciona a classe 'active' apenas na página clicada
  document.getElementById(paginaId).classList.add('active');
}

// Funções para abrir e fechar o modal de Check-out
function abrirModal() {
  document.getElementById('modal-checkout').classList.add('open');
}

function fecharModal() {
  document.getElementById('modal-checkout').classList.remove('open');
}