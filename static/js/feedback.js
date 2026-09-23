/* ==========================================================================
   FEEDBACK AO USUÁRIO (Bootstrap 5)
   - Toasts: mensagens de sucesso/erro que vêm do Flask (flash) ou do JS (mostrarToast)
   - Confirmação "Tem certeza?" para qualquer <form data-confirmar="mensagem">
   ========================================================================== */
(() => {
    const area = document.getElementById('toast-area');
    const ICONES = {
        success: 'bi-check-circle-fill',
        danger: 'bi-exclamation-octagon-fill',
        warning: 'bi-exclamation-triangle-fill',
        info: 'bi-info-circle-fill',
    };

    // Pop-up de mensagem. tipo: success | danger | warning | info
    window.mostrarToast = (mensagem, tipo = 'success') => {
        const toast = document.createElement('div');
        toast.className = `toast align-items-center text-bg-${tipo} border-0`;
        toast.setAttribute('role', 'alert');
        toast.setAttribute('aria-live', 'assertive');
        toast.setAttribute('aria-atomic', 'true');
        toast.innerHTML = `<div class="d-flex">
            <div class="toast-body d-flex align-items-center gap-2"><i class="bi ${ICONES[tipo] || ICONES.info}"></i><span></span></div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Fechar"></button>
        </div>`;
        toast.querySelector('span').textContent = mensagem;
        area.append(toast);
        toast.addEventListener('hidden.bs.toast', () => toast.remove());
        bootstrap.Toast.getOrCreateInstance(toast, { delay: 5000 }).show();
    };

    // Mensagens que o Flask deixou prontas no HTML (flash)
    area.querySelectorAll('.toast').forEach((toast) => {
        bootstrap.Toast.getOrCreateInstance(toast, { delay: 5000 }).show();
    });

    // ---------- Confirmação "Tem certeza?" ----------
    const elModal = document.getElementById('modalConfirmar');
    const modal = bootstrap.Modal.getOrCreateInstance(elModal);
    const botao = document.getElementById('confirmar-botao');
    let formPendente = null;

    function abrirConfirmacao(form) {
        document.getElementById('confirmar-titulo').textContent = form.dataset.confirmarTitulo || 'Tem certeza?';
        document.getElementById('confirmar-mensagem').textContent = form.dataset.confirmar;
        botao.textContent = form.dataset.confirmarBotao || 'Confirmar';
        botao.className = `btn btn-${form.dataset.confirmarCor || 'primary'}`;
        modal.show();
    }

    document.addEventListener('submit', (e) => {
        const form = e.target;
        // e.defaultPrevented: a validação (validacao.js) já barrou o envio, então não pergunta nada
        if (e.defaultPrevented || !form.dataset.confirmar || form.dataset.confirmado) return;

        e.preventDefault();
        formPendente = form;

        // Formulário dentro de outra janela? Fecha ela primeiro (o Bootstrap não empilha modais direito)
        const janelaAberta = form.closest('.modal.show');
        if (janelaAberta) {
            form.dataset.aguardandoConfirmacao = '1';
            janelaAberta.addEventListener('hidden.bs.modal', () => abrirConfirmacao(form), { once: true });
            bootstrap.Modal.getInstance(janelaAberta).hide();
        } else {
            abrirConfirmacao(form);
        }
    });

    botao.addEventListener('click', () => {
        const form = formPendente;
        formPendente = null;
        if (!form) return;
        form.dataset.confirmado = '1';
        modal.hide();
        form.requestSubmit();
    });

    // Cancelou a confirmação: limpa o formulário que estava esperando (ele estava dentro de outra janela)
    elModal.addEventListener('hidden.bs.modal', () => {
        if (formPendente && formPendente.dataset.aguardandoConfirmacao) {
            delete formPendente.dataset.aguardandoConfirmacao;
            formPendente.reset();
        }
        formPendente = null;
    });
})();
