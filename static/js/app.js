'use strict';

const switcher = document.querySelector('.btn-acoes');

// 1. Apenas atualiza o texto do botão baseado na classe que o HTML já tem
if (switcher) {
    if (document.documentElement.classList.contains('pagina-black')) {
        switcher.innerHTML = "<i class=\"bi bi-cloud-moon-fill\"></i> Light";
    } else {
        switcher.innerHTML = "<i class=\"bi bi-cloud-sun-fill\"></i> Dark";
    }
}

// 2. Evento do clique com transição temporária
if (switcher) {
    switcher.addEventListener('click', function() {
        // Adiciona a animação no elemento raiz (HTML)
        document.documentElement.classList.add('animar-transicao');

        // Alterna as classes
        document.documentElement.classList.toggle('pagina-black');
        document.documentElement.classList.toggle('pagina-white');

        // Atualiza texto e LocalStorage
        if (document.documentElement.classList.contains('pagina-black')) {
            this.innerHTML = "<i class=\"bi bi-cloud-moon-fill\"></i> Light";
            localStorage.setItem('dark-mode', 'ativo');
        } else {
            this.innerHTML = "<i class=\"bi bi-cloud-sun-fill\"></i> Dark";
            localStorage.setItem('dark-mode', 'inativo');
        }
    });
}

// 3. Remove a classe de animação após o término
document.documentElement.addEventListener('transitionend', function(e) {
    if (e.target === document.body) {
        document.documentElement.classList.remove('animar-transicao');
    }
});