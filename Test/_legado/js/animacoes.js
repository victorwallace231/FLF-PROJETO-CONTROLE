// Animação dos números do dashboard (contagem de 0 até o valor real).
// Melhoria progressiva: o valor final já vem escrito no HTML pelo Flask;
// se este arquivo falhar ou o usuário preferir menos movimento, nada quebra.

(function () {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

    const DURACAO = 900; // ms

    document.querySelectorAll('.ballons-all h2').forEach((el) => {
        const alvo = parseInt(el.textContent.trim(), 10);
        if (Number.isNaN(alvo) || alvo === 0) return;

        const inicio = performance.now();

        function passo(agora) {
            const progresso = Math.min((agora - inicio) / DURACAO, 1);
            const suavizado = 1 - Math.pow(1 - progresso, 3); // easeOutCubic: começa rápido, termina devagar
            el.textContent = Math.round(alvo * suavizado);
            if (progresso < 1) requestAnimationFrame(passo);
        }

        el.textContent = '0';
        requestAnimationFrame(passo);
    });
})();
