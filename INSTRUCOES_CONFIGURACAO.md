# Configuração local e implantação do FLF Controle

Este guia explica as alterações de configuração e como testar o projeto. A configuração não apaga nem reseta o banco de dados.

## 1. Antes de alterar qualquer coisa

1. Pare o servidor Flask.
2. Faça uma cópia da pasta atual do projeto, incluindo `database_controle.db`.
3. Se já tiver dados mais recentes no banco, mantenha o seu arquivo `database_controle.db`; não o substitua por uma cópia de um ZIP antigo.

## 2. Preparar o ambiente local

Na pasta que contém `app.py` e `requirements.txt`, crie um ambiente virtual e ative-o:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Se o PowerShell bloquear a ativação por política de execução, use diretamente `.\.venv\Scripts\python.exe` nos comandos abaixo, sem alterar a política do computador. Em seguida, crie o arquivo `.env` a partir do modelo:

```powershell
Copy-Item .env.example .env
```

Gere uma chave secreta aleatória:

```powershell
py -c "import secrets; print(secrets.token_hex(32))"
```

Copie a chave gerada e coloque-a após `FLASK_SECRET_KEY=` no `.env`. Não compartilhe esse valor nem o envie ao GitHub.

Para desenvolvimento local, o `.env` deve conter configurações semelhantes a estas:

```dotenv
APP_ENV=development
FLASK_SECRET_KEY=COLE_A_CHAVE_GERADA_AQUI
SESSION_COOKIE_SECURE=0
HOST=127.0.0.1
PORT=5000
```

Instale as dependências e inicie a aplicação:

```powershell
python -m pip install -r requirements.txt
python -m pip check
python -m py_compile app.py
python app.py
```

Em desenvolvimento, o servidor fica acessível apenas no próprio computador (`127.0.0.1`) e o aviso do servidor de desenvolvimento do Flask é esperado.

## 3. Preparar o servidor da empresa

Antes de usar dados reais, configure as variáveis no ambiente do servidor ou em um `.env` protegido. Exemplo quando a aplicação estiver atrás de HTTPS:

```dotenv
APP_ENV=production
FLASK_SECRET_KEY=UMA_CHAVE_ALEATORIA_LONGA_E_PRIVADA
SESSION_COOKIE_SECURE=1
HOST=127.0.0.1
PORT=8080
```

Gere uma chave real com o comando `secrets` acima; não use o texto de exemplo. Em `APP_ENV=production`, executar `py app.py` inicia a aplicação com Waitress em vez do servidor de desenvolvimento do Flask.

- `HOST=127.0.0.1` mantém o Waitress acessível somente localmente. Use este valor quando houver um proxy reverso (por exemplo, Nginx) no mesmo servidor encaminhando o HTTPS ao Waitress. Não mude para `0.0.0.0` sem planejar o acesso direto, HTTPS e regras de firewall com a TI.
- `SESSION_COOKIE_SECURE=1` deve ser usado quando o acesso estiver protegido por HTTPS. Se a aplicação estiver servindo por HTTP, o navegador não enviará esse cookie; não deixe isso como configuração de produção. Configure HTTPS antes da implantação real.
- Não publique o sistema na internet sem configurar HTTPS, firewall, atualização do servidor e política de backups.
- A aplicação usa SQLite. Mantenha `database_controle.db` em armazenamento persistente e faça backups automáticos testados. Não coloque o banco dentro de um contêiner descartável na etapa Docker.
- Para uma implantação mais robusta, configure o processo para iniciar automaticamente e reiniciar em falhas, conforme o sistema operacional do servidor.

## 4. Segurança e dados

- O arquivo `.env` contém segredo e não deve ser compartilhado nem versionado.
- Trocar `FLASK_SECRET_KEY` invalida as sessões já abertas; os usuários precisarão fazer login novamente.
- O `.gitignore` evita que segredos, caches e backups sejam adicionados por engano. O banco principal ainda é necessário para iniciar esta versão; não distribua um banco com dados reais. Para deixar de versioná-lo com segurança, primeiro é preciso garantir que a aplicação crie/migre o esquema em uma instalação limpa.
- Esta etapa não executa reset do banco. O patch de segurança não inclui `database_controle.db`.

## 5. O que ainda deve ser testado

Os comandos acima verificam a instalação das dependências, possíveis conflitos relatados pelo `pip`, e a sintaxe do `app.py`. Depois disso, teste login/logout, permissões, cadastro/edição de equipamentos, transferências, empréstimos, histórico, recuperação de senha e acesso a partir de outro computador. Teste também a restauração de um backup antes de usar dados reais.
