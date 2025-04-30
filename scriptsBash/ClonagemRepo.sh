#!/bin/bash

# Solicita o nome do novo projeto
echo "Escolha o nome do novo projeto"
read nome_projeto

# Solicita a descrição do README
echo "Escolha a descrição do readme"
read descricao_readme

# Cria o diretório do novo projeto
mkdir "${nome_projeto}"
cd "${nome_projeto}"

# Clona o repositório template
git clone https://github.com/RobertoNeto/Template.git
rm -rf .git

# Renomeia o diretório e faz a substituição da descrição no README.md
mv Template Api_do_"${nome_projeto}"
cd Api_do_"${nome_projeto}"
sed -i "s/{{descricao}}/${descricao_readme}/g" README.md

# Verifica se o Python3 está instalado
if command -v python3 > /dev/null 2>&1; then
  echo "Python3 já instalado"
else
  sudo apt install python3
  echo "Python3 instalando"
fi

# Cria ambiente virtual e instala dependências
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Solicita a URL do repositório GitHub a ser substituído
echo "Digite a URL do repositório GitHub a ser substituído"
read url_projeto

# Inicializa o repositório Git
git init
git remote set-url origin "${url_projeto}"
git add remote origin "${url_projeto}"
git add .

# Realiza o commit e push
git commit -m "Primeiro Commit!"
git remote -v
git push -u origin main
