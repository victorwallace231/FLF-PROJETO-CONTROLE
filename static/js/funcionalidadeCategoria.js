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
    <button type="button" class="btn btn-primary w-100 text-black fw-semibold d-flex justify-content-center align-content-center py-2 mt-1 rounded-pill" onclick="voltar()">Voltar</button>
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

        <button type="submit" class="btn btn-primary w-100 text-black fw-semibold d-flex justify-content-center align-content-center py-2 mt-3 rounded-pill">Adicionar</button>
        <button type="button" class="btn btn-primary w-100 text-black fw-semibold d-flex justify-content-center align-content-center py-2 mt-1 rounded-pill" onclick="voltar()">Voltar</button>
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

        <button type="submit" class="btn btn-primary w-100 text-black fw-semibold d-flex justify-content-center align-content-center py-2 mt-3 rounded-pill">Adicionar</button>
        <button type="button" class="btn btn-primary w-100 text-black fw-semibold d-flex justify-content-center align-content-center py-2 mt-1 rounded-pill" onclick="voltar()">Voltar</button>
    </div>
    </form>

    `
}

async function voltar(){
    const container = document.getElementById('container')
    container.innerHTML = `              
        <h3 class="mb-3">Opções de Categorias</h3>
            <button type="button" class="btn btn-primary w-100 text-black text-dark fw-semibold d-flex justify-content-center align-content-center py-2 mb-3" onclick="adicionarCategoria()">Adicionar Categoria</button>
            <button type="button" class="btn btn-primary w-100 text-black text-dark fw-semibold d-flex justify-content-center align-content-center py-2 mb-3" onclick="deletarCategoria('{{ categorias }}')">Deletar Categoria</button>
            <button type="button" class="btn btn-primary w-100 text-black text-dark fw-semibold d-flex justify-content-center align-content-center py-2 mb-3" onclick="modificarCategoria()">Modificar Categoria</button>

    `
}