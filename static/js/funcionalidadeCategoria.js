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
    const cats = categorias
    container.innerHTML = `
    
    <h3>Adicione uma Nova Categoria</h3>
    <form action="/delete_categoria" method="POST">
    <div class="input-group mb-3">
        <span class="input-group-text border-icon"><i class="bi bi-hash"></i></span>

        <select class="input-group mb-3 form-select border-icon" name="id_categoria" required>
            <option value="" disabled selected>Selecione a Categoria do Equipamento</option>
    `
    for (cat in cats){
        container.innerHTML += $`
        <option value="${cat [0]}" disabled selected>Selecione a Categoria do Equipamento</option>
        ` 
    }

    container.innerHTML += `
        </select>
        
        <span class="input-group-text border-icon"><i class="bi bi-hash"></i></span>
        <input type="text" id="createInput" class="form-control" name="nome_categoria" placeholder="Digite a Nova Categoria" required>

        <button type="submit" class=" w-100 text-dark text-black fw-semibold">

        <a class=" btn btn-primary w-100 text-dark text-black text-block fw-semibold">Adicionar</a>
        </button>
    </div>
    </form>

    `
}

async function modificarCategoria(){
    const container = document.getElementById('container')

    container.innerHTML = `
    
    <h3>Adicione uma Nova Categoria</h3>
    <form action="" method="POST">
    <div class="input-group mb-3">
        <span class="input-group-text border-icon"><i class="bi bi-hash"></i></span>

        <select class="input-group mb-3 form-select border-icon" name="categoria" required>
            <option value="" disabled selected>Selecione a Categoria do Equipamento</option>
                {% for cat in categorias %}
                    <option value="{{ cat [0] }}" {% if categoria == cat [1] %} selected {% endif %}>{{ cat[1] }}</option>
                {% endfor %}
        </select>
        
        <span class="input-group-text border-icon"><i class="bi bi-hash"></i></span>
        <input type="text" id="createInput" class="form-control" name="nome_categoria" placeholder="Digite a Nova Categoria" required>

        <button type="submit" class=" w-100 text-dark text-black fw-semibold">

        <a class=" btn btn-primary w-100 text-dark text-black text-block fw-semibold">Adicionar</a>
        </button>
    </div>
    </form>

    `
}