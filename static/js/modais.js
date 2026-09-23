/* ==========================================================================
   JANELAS (MODAIS) REUTILIZÁVEIS
   Em vez de uma janela por linha da tabela (dezenas de <dialog> repetidos), existe UMA
   janela por ação. Ao abrir, ela lê os data-* da linha <tr> que foi clicada.

   Dentro da janela:
     data-campo="marca"            <input>/<select> recebe o valor; outros elementos recebem o texto
     data-campo-icone="icone"      <i> recebe a classe do ícone
     data-campo-status             <span> vira o badge do status da linha
     data-campo-radio="icone"      radio que combina com o valor fica marcado
   ========================================================================== */
document.addEventListener('show.bs.modal', (e) => {
    const janela = e.target;
    const gatilho = e.relatedTarget;
    if (!gatilho) return;

    const dados = (gatilho.closest('tr') || gatilho).dataset;

    janela.querySelectorAll('[data-campo]').forEach((el) => {
        const valor = dados[el.dataset.campo] || '';
        if (el.matches('input, select, textarea')) el.value = valor;
        else el.textContent = valor || '—';
    });

    janela.querySelectorAll('[data-campo-icone]').forEach((el) => {
        el.className = `bi ${dados[el.dataset.campoIcone] || ''}`;
    });

    janela.querySelectorAll('[data-campo-status]').forEach((el) => {
        el.className = `badge-status status-${dados.status}`;
        el.textContent = dados.statusTexto;
    });

    janela.querySelectorAll('input[type=radio][data-campo-radio]').forEach((radio) => {
        radio.checked = radio.value === dados[radio.dataset.campoRadio];
    });
});
