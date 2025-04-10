# API de Receitas

Este projeto é uma API feita em Flask com MySQL para gerenciar ingredientes e receitas. A API oferece os seguintes endpoints para CRUD (Criar, Ler, Atualizar e Deletar) de ingredientes e Receitas:

- **GET** `/ingredientes`: Retorna todos os ingredientes.
- **GET** `/ingredientes/<nome>`: Retorna um ingrediente específico pelo nome.
- **POST** `/ingredientes`: Adiciona um novo ingrediente.
- **PUT** `/ingredientes/<nome>`: Atualiza as informações de um ingrediente existente.
- **DELETE** `/ingredientes/<nome>`: Exclui um ingrediente.

# Como Rodar o Projeto

1. Clonando o Repositório

Primeiro, faça o clone deste repositório para sua máquina local:
         ```bash
              git clone https://github.com/usuario/API_receitas.git
              cd API_receitas

2. Instalar as dependências
   No diretório do projeto, instale as dependências usando o pip:
          ```bash
              pip install -r requirements.txt

3. Instale o MySQL e crie um banco de dados chamado api_receitas no MySQL:
           ```SQL
               CREATE DATABASE api_receitas;

5. Crie um arquivo .env para armazenar as credenciais de acesso ao banco de dados.
   Crie o arquivo na raiz do projeto e adicione as variáveis de ambiente:
   MYSQL_USER=seu_usuario
   MYSQL_PASSWORD=sua_senha
   MYSQL_HOST=localhost
   MYSQL_DB=api_receitas

6. Rodar a API localmente
  Com tudo configurado, você pode agora rodar a API localmente. No terminal, execute o comando:
            ```bash
                 python app.py




