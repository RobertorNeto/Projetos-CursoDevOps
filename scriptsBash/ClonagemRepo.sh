#!/bin/bash
#atividade para criar um repositorio novo para uma api com base em um template de um outro repositorio de api.

echo "Escolha o nome do novo projeto"
read nome_projeto

echo "Escolha a descrição do readme"
read descricao_readme

mkdir "${nome_projeto}"
cd "${nome_projeto}"

git clone https://github.com/RobertoNeto/Template.git
rm -rf .git

mv Template Api_do_"${nome_projeto}"
cd Api_do_"${nome_projeto}"
sed -i "s/{{descricao}}/${descricao_readme}/g" README.md

if command -v python3 > /dev/null 2>&1; then
  echo "Python3 já instalado"
else
  sudo apt install python3
  echo "Python3 instalando"
fi

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

echo "Digite a URL do repositório GitHub a ser substituído"
read url_projeto

git init
git remote set-url origin "${url_projeto}"
git add remote origin "${url_projeto}"
git add .

git commit -m "Primeiro Commit!"
git remote -v
git push -u origin main
