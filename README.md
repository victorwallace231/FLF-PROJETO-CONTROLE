# 💻 FLF Controle

O FLF Controle é um sistema web que tem a finalidade de gerir e ter controle da entrada, saída e empréstimo dos periféricos da sala do N.T.I. Esse projeto foi criado pelos estagiarios de Desenvolvimento da Faculdade Luciano Feijão com o proposito principal sendo a aprendizagem dos estagiarios num projeto prático.

## Sobre o Projeto


### ✨ Funcionalidades
* **Autenticação:** Login de acesso para supervisores.
* **Gestão de Periféricos:** Consulta e verificação de status dos equipamentos.
* **Controle de Empréstimos:** Registro de saídas e devoluções no banco de dados.
* **Ícones por equipamento:** Cada item (mouse, passador de slide, adaptador HDMI...) usa um ícone do Bootstrap Icons, e novos ícones podem ser adicionados na tela de cadastro.
* **Localização por unidade e setor:** A origem e a localização atual dos equipamentos são relacionadas às tabelas `unidades` e `setores` por chave estrangeira; a tela de equipamentos permite filtrar por uma unidade, um setor ou ambos.
* **Avisos na tela:** Erros nos campos e pop-ups de sucesso/confirmação com Bootstrap 5.

Para saber mais detalhe temos a [Estrutura](https://github.com/victorwallace231/FLF-PROJETO-CONTROLE/blob/main/Structure.md) do projeto

## 🛠️ Tecnologias
* **Backend:** Python (Flask)
* **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5
* **Banco de Dados:** SQL (SQLite)

## 🚀 Como executar o projeto

### Pré-requisitos
* Python 3.14.7 (versão usada na preparação desta versão).
* As dependências declaradas em `requirements.txt`.

### Passo a passo

1. Crie um ambiente virtual (recomendado):
   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
2. Instale as dependências:
   ```powershell
   python -m pip install -r requirements.txt
   ```
3. Copie `.env.example` para `.env`, gere uma chave secreta e preencha `FLASK_SECRET_KEY`. Os passos completos estão em [`INSTRUCOES_CONFIGURACAO.md`](INSTRUCOES_CONFIGURACAO.md).
4. Inicie para desenvolvimento local:
   ```powershell
   py app.py
   ```

Para implantação na rede interna da empresa, leia `INSTRUCOES_CONFIGURACAO.md` antes de mudar `APP_ENV` para `production`. Não substitua um banco de dados que já contenha registros recentes.
