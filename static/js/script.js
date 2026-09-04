const btnIcon = document.getElementById('btn-icon');
const modal = document.getElementById('modal-suspensao');

btnIcon.addEventListener('click', (event) => {
    event.stopPropagation();
    modal.classList.toggle('active');
});

document.addEventListener('click', (event) => {
    if (!modal.contains(event.target) && event.target !== btnIcon) {
      modal.classList.remove('active');
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

  dropdown.style.top = `${rect.bottom + window.scrollY + 4}px`;
  dropdown.style.left = `${rect.right - 150}px`;

  dropdown.classList.toggle('show');
}


window.addEventListener('click', closeMenus);
window.addEventListener('scroll', closeMenus, true);

function closeMenus() {
  document.querySelectorAll('.dropdown-menu').forEach(menu => {
    menu.classList.remove('show');
  });
}