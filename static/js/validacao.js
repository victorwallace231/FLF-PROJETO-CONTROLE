/* ==========================================================================
   VALIDAÇÃO DE FORMULÁRIOS
   --------------------------------------------------------------------------
   Como usar: coloque  data-validar  no <form> e  required  nos campos obrigatórios.
   Ao enviar com campos vazios/inválidos:
     - cada campo ganha borda vermelha, tremidinha e uma mensagem individual;
     - aparece um alerta geral no topo do formulário ("todos os itens não foram preenchidos"...).
   Extras opcionais nos campos:
     data-msg="..."          mensagem individual personalizada (campo vazio)
     data-rotulo="..."       nome do campo usado no alerta geral (padrão: texto do <label>)
     data-somente-numeros    só aceita dígitos (telefones)
     data-sem-validacao      o campo é ignorado pela validação (ex.: campos auxiliares)
   ========================================================================== */
(() => {
    const SELETOR_CAMPOS = 'input:not([type=hidden]):not([type=radio]):not([type=checkbox]):not([type=submit]):not([type=button]), select, textarea';

    const camposDe = (form) => [...form.querySelectorAll(SELETOR_CAMPOS)].filter((c) => !c.disabled && !c.hasAttribute('data-sem-validacao'));

    const alvoDaMensagem = (campo) => campo.closest('.input-group') || campo;

    function rotulo(campo) {
        const label = campo.id ? document.querySelector(`label[for="${campo.id}"]`) : null;
        return campo.dataset.rotulo || (label ? label.textContent.trim() : campo.name);
    }

    function mensagem(campo) {
        const v = campo.validity;
        if (v.valueMissing) return campo.dataset.msg || (campo.tagName === 'SELECT' ? 'Selecione uma opção.' : 'Preencha este campo.');
        if (v.typeMismatch) return 'Digite um e-mail válido.';
        if (v.patternMismatch || v.tooShort) return campo.title || 'O valor digitado está em um formato inválido.';
        return campo.validationMessage;
    }

    // Reinicia a animação mesmo que a classe já estivesse no elemento
    function tremer(el) {
        el.classList.remove('campo-erro');
        void el.offsetWidth;
        el.classList.add('campo-erro');
    }

    function limparCampo(campo) {
        campo.classList.remove('is-invalid');
        const alvo = alvoDaMensagem(campo);
        alvo.classList.remove('campo-erro');
        const msg = alvo.nextElementSibling;
        if (msg && msg.classList.contains('mensagem-campo')) msg.remove();
    }

    function marcarErro(campo) {
        limparCampo(campo);
        campo.classList.add('is-invalid');
        const alvo = alvoDaMensagem(campo);
        const msg = document.createElement('div');
        msg.className = 'mensagem-campo';
        msg.setAttribute('role', 'alert');
        msg.textContent = mensagem(campo);
        alvo.after(msg);
        tremer(alvo);
    }

    // Alerta geral: some quando não há mais nenhum campo com erro
    function atualizarAlertaGeral(form, animar) {
        const campos = camposDe(form);
        const invalidos = campos.filter((c) => c.classList.contains('is-invalid'));
        let alerta = form.querySelector('.alerta-geral');

        if (invalidos.length === 0) {
            if (alerta) alerta.remove();
            return;
        }

        if (!alerta) {
            alerta = document.createElement('div');
            alerta.className = 'alert alert-danger alerta-geral';
            alerta.setAttribute('role', 'alert');
            // Dentro de janelas (modais) o alerta vai para o corpo, abaixo do título
            (form.querySelector('.modal-body') || form).prepend(alerta);
        }

        const obrigatorios = campos.filter((c) => c.required);
        const todosVazios = obrigatorios.length > 1 && obrigatorios.every((c) => c.classList.contains('is-invalid'));
        const nomes = invalidos.map(rotulo).filter(Boolean).join(', ');

        alerta.innerHTML = '<i class="bi bi-exclamation-triangle-fill me-2"></i>';
        const texto = document.createElement('span');
        texto.textContent = todosVazios
            ? 'Todos os itens estão vazios. Preencha os campos para continuar.'
            : `${invalidos.length === 1 ? 'Um item não foi preenchido corretamente' : invalidos.length + ' itens não foram preenchidos corretamente'}: ${nomes}.`;
        alerta.append(texto);

        if (animar) tremer(alerta);
    }

    function limparFormulario(form) {
        camposDe(form).forEach(limparCampo);
        const alerta = form.querySelector('.alerta-geral');
        if (alerta) alerta.remove();
    }

    // Desliga o balãozinho padrão do navegador: quem mostra os erros é este arquivo
    document.querySelectorAll('form[data-validar]').forEach((f) => { f.noValidate = true; });

    document.addEventListener('submit', (e) => {
        const form = e.target;
        if (!form.matches('form[data-validar]')) return;

        const invalidos = camposDe(form).filter((c) => !c.checkValidity());
        camposDe(form).forEach(limparCampo);

        if (invalidos.length) {
            e.preventDefault();
            invalidos.forEach(marcarErro);
            atualizarAlertaGeral(form, true);
            invalidos[0].focus();
        } else {
            atualizarAlertaGeral(form, false);
        }
    });

    // Corrigiu o campo? O erro daquele campo some na hora (e o alerta geral se ajusta)
    const aoEditar = (e) => {
        const campo = e.target;

        if (campo.matches && campo.matches('[data-somente-numeros]')) {
            campo.value = campo.value.replace(/\D/g, '');
        }

        if (campo.classList && campo.classList.contains('is-invalid') && campo.checkValidity()) {
            limparCampo(campo);
            const form = campo.closest('form');
            if (form) atualizarAlertaGeral(form, false);
        }
    };
    document.addEventListener('input', aoEditar);
    document.addEventListener('change', aoEditar);

    // Fechou uma janela (modal)? Limpa os campos e os erros dos formulários dela
    document.addEventListener('hidden.bs.modal', (e) => {
        e.target.querySelectorAll('form[data-validar]').forEach((form) => {
            // Formulário que fechou a janela só para pedir confirmação ainda precisa dos valores
            if (form.dataset.aguardandoConfirmacao) return;
            form.reset();
            limparFormulario(form);
        });
    });
})();
