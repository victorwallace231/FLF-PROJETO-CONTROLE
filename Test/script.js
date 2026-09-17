//Janelinha da Conta de usuário no Menu Principal

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