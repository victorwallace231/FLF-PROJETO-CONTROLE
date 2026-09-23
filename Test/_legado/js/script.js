//Janelinha da Conta de usuário no Menu Principal

const btnIcon = document.getElementById('btn-icon');
const modal = document.getElementById('modal-suspensao');

btnIcon.addEventListener('click', (event) => {
    event.stopPropagation();
    const aberto = modal.classList.toggle('active');
    btnIcon.setAttribute('aria-expanded', aberto); // leitores de tela sabem se o menu está aberto
});

document.addEventListener('click', (event) => {
    if (!modal.contains(event.target) && event.target !== btnIcon) {
      modal.classList.remove('active');
      btnIcon.setAttribute('aria-expanded', 'false');
    }
});


// Janelinha de ações na tabela de equipamentos

function toggleMenu(event) {
  event.stopPropagation();
  
  const button = event.currentTarget;
  const dropdown = button.nextElementSibling;

  document.querySelectorAll('.dropdown-menu').forEach(menu => {
    if (menu !== dropdown) menu.classList.remove('show');
  });

  const rect = button.getBoundingClientRect();

  // .dropdown-menu é position:fixed => usa coordenadas da JANELA.
  // (Somar window.scrollY jogava o menu para longe do botão quando a página estava rolada.)
  const largura = 160;                      // mesma largura definida em class.css
  const altura = dropdown.offsetHeight || 170;
  const cabeEmbaixo = rect.bottom + 4 + altura <= window.innerHeight;

  dropdown.style.top = `${cabeEmbaixo ? rect.bottom + 4 : Math.max(8, rect.top - altura - 4)}px`;
  dropdown.style.left = `${Math.min(Math.max(8, rect.right - largura), window.innerWidth - largura - 8)}px`;

  dropdown.classList.toggle('show');
}


window.addEventListener('click', closeMenus);
window.addEventListener('scroll', closeMenus, true);

function closeMenus() {
  document.querySelectorAll('.dropdown-menu').forEach(menu => {
    menu.classList.remove('show');
  });
}