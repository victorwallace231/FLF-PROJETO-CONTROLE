'use strict';

const switcher = document.querySelector('.btn-acoes');


const modoEscuroSalvo = localStorage.getItem('dark-mode');

if (modoEscuroSalvo === 'ativo') {
    document.body.classList.add('pagina-black');
    document.body.classList.remove('pagina-white');

    if (switcher) switcher.innerHTML = "<i class=\"bi bi-cloud-moon-fill\"></i> Light";
} else {
    document.body.classList.add('pagina-white');
    document.body.classList.remove('pagina-black');

    if (switcher) switcher.innerHTML = "<i class=\"bi bi-cloud-sun-fill\"></i> Dark";
}

if (switcher) {
    switcher.addEventListener('click', function() {
        document.body.classList.toggle('pagina-black');
        document.body.classList.toggle('pagina-white');

        // Verifica se o modo escuro acabou de ser ativado com o clique
        if (document.body.classList.contains('pagina-black')) {
            this.innerHTML = "<i class=\"bi bi-cloud-moon-fill\"></i> Light";
            localStorage.setItem('dark-mode', 'ativo'); // Salva a escolha no navegador
        } else {
            this.innerHTML = "<i class=\"bi bi-cloud-sun-fill\"></i> Dark";
            localStorage.setItem('dark-mode', 'inativo'); // Salva que foi desativado
        }
    });
}