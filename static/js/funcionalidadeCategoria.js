async function adicionarCategoria() {
    const container = document.getElementById('container')

    container.innerHTML = `
    
    <h3>Adicione uma Nova Categoria</h3>
    <form action="/create_categoria" method="POST">
        <div class="w-100">
            <label for="createInput" class="form-label">Categoria</label>
            <div class="input-group">
                <span class="input-group-text border-icon"><i class="bi bi-hash"></i></span>
                <input type="text" id="createInput" class="form-control" name="nome_categoria" placeholder="Digite a Nova Categoria" required>
                <button type="submit" class="btn btn-primary w-100 text-black fw-semibold d-flex justify-content-center align-content-center py-2 mt-3 rounded-pill">Adicionar</button>
            </div>
        </div>
    </form>

    `
}

async function deletarCategoria(categorias){
    const container = document.getElementById('container')
    
    let opcoesHTML=``

    for (let cats of categorias){
        if (cats[2] != 1){
            opcoesHTML+=`<option value="${cats[0]}">${cats[1]}</option>`
        }
    }
    container.innerHTML = `
    
    <h3>Selecione a Categoria que quer excluir</h3>
    <form action="/delete_categoria" method="POST">
    <div class="input-group mb-3">
        <span class="input-group-text border-icon"><i class="bi bi-hash"></i></span>

        <select class="input-group mb-3 form-select border-icon" name="id_categoria" required>
            <option value="" disabled selected>Selecione a Categoria do Equipamento</option>
            ${opcoesHTML}
        </select>

        <button type="submit" class=" w-100 text-dark text-black fw-semibold">

        <a class=" btn btn-primary w-100 text-dark text-black text-block fw-semibold">Excluir</a>
        </button>
    </div>
    </form>

    `
}

async function modificarCategoria(categorias){
    const container = document.getElementById('container')
    
    let opcoesHTML=``

    for (let cats of categorias){
        if (cats[2] != 1){
            opcoesHTML+=`<option value="${cats[0]}">${cats[1]}</option>`
        }
    }
    container.innerHTML = `

                            <form id="form-createitem" action="/update_categoria" method="POST">
                             <h3>Selecione a Categoria que quer excluir</h3>
                            <select class="input-group mb-3 form-select border-icon" name="id_categoria" required>
                                <option value="" disabled selected>Selecione a Categoria do Equipamento</option>
                                ${opcoesHTML}
                            </select>         

                            <div class="w-100">
                                <label for="createInput" class="form-label">Marca</label>
                                <div class="input-group">
                                    <span class="input-group-text border-icon"><i class="bi bi-box-seam"></i></span>
                                    <input type="text" id="createInput" class="form-control" name="nome_categoria" placeholder="Digite o novo da categoria" required>
                                </div>
                            </div>

                            <div class="mb-2">
                                

                            </div>
                                
                                <button type="submit" class="btn btn-primary w-100 text-black fw-semibold d-flex justify-content-center align-content-center py-2">Editar</button>
                        </form>

    `
}