/* ==========================================================================
   SELETOR DE ÍCONES — permite adicionar novos ícones do Bootstrap Icons
   (https://icons.getbootstrap.com). O ícone digitado é conferido no próprio navegador
   e, se existir, é salvo pela rota /create_icone (sem recarregar a página).
   ========================================================================== */
(() => {
    const bloco = document.getElementById('icone-novo');
    if (!bloco) return;

    const campoClasse = document.getElementById('icone-novo-classe');
    const campoNome = document.getElementById('icone-novo-nome');
    const previa = document.getElementById('icone-novo-previa');
    const botao = document.getElementById('icone-novo-botao');
    const erro = document.getElementById('icone-novo-erro');
    const grade = document.getElementById('grade-icones');

    // "mouse2", "bi-mouse2" ou "bi bi-mouse2" -> "bi-mouse2"
    function normalizar(texto) {
        let classe = texto.trim().toLowerCase().replace(/^bi bi-/, 'bi-');
        if (classe && !classe.startsWith('bi-')) classe = `bi-${classe}`;
        return classe;
    }

    // A fonte de ícones só desenha o glifo se a classe existir: dá pra descobrir lendo o ::before
    function iconeExiste(classe) {
        if (!/^bi-[a-z0-9]+(-[a-z0-9]+)*$/.test(classe)) return false;
        const teste = document.createElement('i');
        teste.className = `bi ${classe}`;
        teste.style.cssText = 'position:absolute;visibility:hidden';
        document.body.append(teste);
        const conteudo = getComputedStyle(teste, '::before').content;
        teste.remove();
        return Boolean(conteudo) && conteudo !== 'none' && conteudo !== 'normal' && conteudo !== '""';
    }

    function mostrarErro(texto) {
        erro.textContent = texto;
        erro.classList.remove('d-none');
        campoClasse.classList.add('is-invalid');
        campoClasse.parentElement.classList.remove('campo-erro');
        void campoClasse.offsetWidth;
        campoClasse.parentElement.classList.add('campo-erro');
    }

    function limparErro() {
        erro.classList.add('d-none');
        campoClasse.classList.remove('is-invalid');
    }

    campoClasse.addEventListener('input', () => {
        limparErro();
        const classe = normalizar(campoClasse.value);
        previa.innerHTML = '';
        if (iconeExiste(classe)) {
            const i = document.createElement('i');
            i.className = `bi ${classe}`;
            previa.append(i);
        }
    });

    botao.addEventListener('click', async () => {
        const classe = normalizar(campoClasse.value);

        if (!classe) return mostrarErro('Digite o nome do ícone (ex.: bi-mouse2).');
        if (!iconeExiste(classe)) return mostrarErro('Esse ícone não existe no Bootstrap Icons. Confira o nome no site oficial.');
        limparErro();

        const dados = new FormData();
        dados.append('classe', classe);
        dados.append('nome', campoNome.value);

        botao.disabled = true;
        try {
            const resposta = await fetch('/create_icone', { method: 'POST', body: dados });
            const resultado = await resposta.json();
            if (!resultado.ok) return mostrarErro(resultado.erro);

            // Coloca o ícone novo na grade, já marcado
            const id = `icone-${classe}`;
            const radio = document.createElement('input');
            radio.type = 'radio';
            radio.className = 'btn-check';
            radio.name = 'icone';
            radio.id = id;
            radio.value = resultado.classe;
            radio.autocomplete = 'off';
            radio.checked = true;

            const rotulo = document.createElement('label');
            rotulo.className = 'btn btn-outline-primary seletor-icones__item';
            rotulo.htmlFor = id;
            rotulo.title = resultado.nome;
            const i = document.createElement('i');
            i.className = `bi ${resultado.classe}`;
            const nome = document.createElement('span');
            nome.textContent = resultado.nome;
            rotulo.append(i, nome);

            grade.append(radio, rotulo);
            rotulo.scrollIntoView({ block: 'nearest' });

            campoClasse.value = '';
            campoNome.value = '';
            previa.innerHTML = '';
            window.mostrarToast(`Ícone "${resultado.nome}" adicionado e selecionado!`, 'success');
        } catch (e) {
            mostrarErro('Não foi possível salvar o ícone. Tente novamente.');
        } finally {
            botao.disabled = false;
        }
    });
})();
