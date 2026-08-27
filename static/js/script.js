function navegarPara(paginaId) {

  const paginas = document.querySelectorAll('.page');
  paginas.forEach(p => p.classList.remove('active'));

  document.getElementById(paginaId).classList.add('active');
}


function abrirModal() {
  document.getElementById('modal-checkout').classList.add('open');
}

function fecharModal() {
  document.getElementById('modal-checkout').classList.remove('open');
}