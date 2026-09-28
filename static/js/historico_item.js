/* Histórico de empréstimos de um equipamento (janela #modalHistorico da tela de equipamentos) */
(() => {
    const janela = document.getElementById('modalHistorico');
    if (!janela) return;

    const lista = document.getElementById('lista-emprestimos');

    function linha(rotulo, valor) {
        const p = document.createElement('p');
        const forte = document.createElement('strong');
        forte.textContent = `${rotulo}: `;
        p.append(forte, document.createTextNode(valor || '—'));  // textContent: nada digitado vira HTML
        return p;
    }

    janela.addEventListener('show.bs.modal', async (e) => {
        const linhaTabela = e.relatedTarget && e.relatedTarget.closest('tr');
        if (!linhaTabela) return;

        lista.textContent = 'Carregando...';

        const dados = new FormData();
        dados.append('id_periferico', linhaTabela.dataset.id);

        try {
            const resposta = await fetch('/verifica_1emprestimo', { method: 'POST', body: dados });
            const emprestimos = await resposta.json();

            lista.textContent = '';
            if (emprestimos.length === 0) {
                lista.textContent = 'Nenhum empréstimo realizado para esse item.';
                return;
            }

            emprestimos.forEach((emp) => {
                const cartao = document.createElement('div');
                cartao.className = 'border-bottom pb-2 mb-2';
                cartao.append(
                    linha('Responsável', emp.responsavel),
                    linha('Data de saída', emp.data_saida),
                    linha('Data de devolução', emp.data_devolucao),
                    linha('Telefone', emp.tel_responsavel),
                    linha('Setor/Evento', emp.observacao),
                    linha('Status', emp.devolvido === 1 ? 'Devolvido' : 'Em uso'),
                );
                lista.append(cartao);
            });
        } catch (erro) {
            lista.textContent = '';
            window.mostrarToast('Não foi possível carregar o histórico. Tente novamente.', 'danger');
            console.error('Erro ao carregar empréstimos:', erro);
        }
    });

    janela.addEventListener('hidden.bs.modal', () => { lista.textContent = ''; });
})();
