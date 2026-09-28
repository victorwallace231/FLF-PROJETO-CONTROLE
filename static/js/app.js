'use strict';

const switcher = document.querySelector('.btn');

switcher.addEventListener('click', function() {
    document.body.classList.toggle('pagina-light');
    document.body.classList.toggle('pagina-dark');

    const className = document.body.className;
    if(className == "pagina-light") {
        this.innerHTML = "<i class=\"bi bi-cloud-sun-fill\"></i> Dark";
    } else if(className == "pagina-dark") {
        this.innerHTML = "<i class=\"bi bi-cloud-moon-fill\"></i> Light";
    }

    console.log('current class name: ' + className);
});