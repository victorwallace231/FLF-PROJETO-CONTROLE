/* ==========================================================================
   UNIDADE -> SETOR
   Cada par de <select> criado pela macro `seletor_localizacao` funciona assim:
     - o <select> de setor guarda TODOS os setores em data-setores (JSON);
     - ao escolher a unidade, ele é refeito só com os setores daquela unidade
       (unidades diferentes podem ter setores com o mesmo nome).
   Nas janelas de edição, os ids atuais vêm dos data-* da linha clicada
   (nomes indicados em data-loc-chave-unidade / data-loc-chave-setor).
   ========================================================================== */
(() => {
    const setorDe = (selUnidade) => document.getElementById(`${selUnidade.dataset.locUnidade}-setor`);

    function preencherSetores(selSetor, idUnidade, idSetor) {
        if (!selSetor) return;
        const todos = JSON.parse(selSetor.dataset.setores || '[]');
        const doGrupo = todos.filter((s) => idUnidade && String(s.id_unidade) === String(idUnidade));
        const base = selSetor.dataset.locObrigatorio === '1';
        // Campo opcional: se escolheu a unidade, o setor passa a ser obrigatório
        const exige = base || Boolean(idUnidade);

        let texto = base ? 'Selecione primeiro a unidade' : (selSetor.dataset.locVazio || 'Manter localização atual');
        if (idUnidade) texto = doGrupo.length ? 'Selecione o setor' : 'Esta unidade ainda não tem setores';

        selSetor.innerHTML = '';
        const vazio = new Option(texto, '', true, true);
        vazio.disabled = exige;
        selSetor.add(vazio);
        doGrupo.forEach((s) => selSetor.add(new Option(s.nome_setor, s.id_setor)));
        selSetor.required = exige;
        if (idSetor) selSetor.value = String(idSetor);
    }

    // Escolheu outra unidade: refaz a lista de setores
    document.addEventListener('change', (e) => {
        const selUnidade = e.target.closest && e.target.closest('select[data-loc-unidade]');
        if (selUnidade) preencherSetores(setorDe(selUnidade), selUnidade.value);
    });

    // Formulário limpo (form.reset ao fechar a janela): volta ao estado inicial
    document.addEventListener('reset', (e) => {
        setTimeout(() => {
            e.target.querySelectorAll('select[data-loc-unidade]').forEach((s) => preencherSetores(setorDe(s), s.value));
        }, 0);
    });

    // Janela de edição: marca a unidade e o setor atuais do equipamento da linha clicada
    document.addEventListener('show.bs.modal', (e) => {
        const gatilho = e.relatedTarget;
        if (!gatilho) return;
        const dados = (gatilho.closest('tr') || gatilho).dataset;

        e.target.querySelectorAll('select[data-loc-chave-unidade]').forEach((selUnidade) => {
            const selSetor = setorDe(selUnidade);
            const idUnidade = dados[selUnidade.dataset.locChaveUnidade] || '';
            const idSetor = dados[selUnidade.dataset.locChaveSetor] || '';

            // Só pré-seleciona se o par ainda existe (não foi excluído). Se a unidade ou o setor do
            // equipamento foram excluídos, os dois ficam em branco ("manter origem atual"), em vez de
            // marcar só a unidade e travar o salvamento pedindo um setor.
            const todos = JSON.parse(selSetor.dataset.setores || '[]');
            const valido = todos.some((s) => String(s.id_setor) === String(idSetor) && String(s.id_unidade) === String(idUnidade))
                && [...selUnidade.options].some((o) => o.value === String(idUnidade));

            selUnidade.value = valido ? idUnidade : '';
            preencherSetores(selSetor, selUnidade.value, valido ? idSetor : '');
        });
    });

    // Estado inicial de todos os pares da página
    document.querySelectorAll('select[data-loc-unidade]').forEach((s) => preencherSetores(setorDe(s), s.value));
})();
