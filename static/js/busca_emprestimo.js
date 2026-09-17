async function carregarEmprestimos(idPeriferico){

    var controle = 0
    const modal = document.getElementById('modal-historico');
    const container = document.getElementById('lista-emprestimos');

    if (!modal || !container) return;

    modal.showModal();

    if (controle === 1){
        return;
    }


    const formData = new FormData();
    formData.append('id_periferico', idPeriferico);


    try {
        const resposta = await fetch('/verifica_1emprestimo', {
            method: 'POST',
            body: formData
        });

        const listaEmprestimos = await resposta.json()

        if (listaEmprestimos.length === 0) {
            container.innerHTML = '<p>Nenhum empréstimo realizado para esse item</p>'

            return;
        }else{

            listaEmprestimos.forEach(emprestimo => {

                const statusEmprestimo = emprestimo.devolvido === 1 ?'Devolvido' : 'Em uso'
                const corStatus = emprestimo.devolvido === 1 ? 'disponivel' : 'emuso' 
            
                container.innerHTML+=`
                <div class="card-historico" style="border-bottom: 1px solid #ccc; padding: 10px;"> 
                    <p><strong>Responsável:</strong> ${emprestimo.responsavel}</p>
                    <p><strong>Data de Saída:</strong> ${emprestimo.data_saida}</p>
                    <p><strong>Data de Devolução:</strong> ${emprestimo.data_devolucao}</p>
                    <p><strong>Telefone do Responsável:</strong> ${emprestimo.tel_responsavel}</p>
                    <p><strong>OBS:</strong> ${emprestimo.observacao}</p>
                    <p><strong>OBS:</strong> ${statusEmprestimo}</p>
                </div>
                `;
                controle = 1
        });

        }
    
    } catch (erro){
        console.error ("erro ao carregar emprestimos:", erro)
    }


}
async function fecharModal() {
    const modal = document.getElementById('modal-historico')
    const container = document.getElementById('lista-emprestimos')

    modal.close()
    container.innerHTML= ''

}